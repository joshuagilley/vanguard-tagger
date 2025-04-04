import logging
import boto3
import json
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import joblib
import os
from io import BytesIO
import tempfile

# disable GPU 
tf.config.set_visible_devices([], 'GPU')

# Set up logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Set to INFO or DEBUG for more verbose logs

# AWS S3 bucket details
BUCKET_NAME = "the-digital-vanguard"
MODEL_S3_KEY = "models/tagging_model.h5"
MLB_S3_KEY = "models/mlb_labels.pkl"

# S3 client
s3 = boto3.client("s3")

def load_model_from_s3(bucket, key):
    """Download a TensorFlow model from S3 into a temporary file and load it."""
    logger.info(f"Loading model from S3: {bucket}/{key}")
    model_stream = BytesIO()
    s3.download_fileobj(bucket, key, model_stream)
    model_stream.seek(0)  # Reset stream position
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".h5") as temp_model_file:
        temp_model_file.write(model_stream.read())
        temp_model_path = temp_model_file.name
    
    model = tf.keras.models.load_model(temp_model_path)
    os.unlink(temp_model_path)  # Clean up temporary file
    logger.info("Model loaded successfully.")
    return model

def load_labels_from_s3(bucket, key):
    """Load a pickle file directly from S3 into memory."""
    logger.info(f"Loading labels from S3: {bucket}/{key}")
    label_stream = BytesIO()
    s3.download_fileobj(bucket, key, label_stream)
    label_stream.seek(0)
    return joblib.load(label_stream)

def get_embedding(text, embed):
    """Generate an embedding for the input text."""
    logger.debug(f"Generating embedding for text: {text[:50]}...")  # Log a snippet of the text
    return embed([text]).numpy()[0]

def generate_tags(text, tagging_model, mlb, embed):
    """Generate tags based on model predictions."""
    logger.info(f"Generating tags for text: {text[:50]}...")  # Log a snippet of the text
    input_embedding = get_embedding(text, embed)
    predictions = tagging_model.predict(np.array([input_embedding]))[0]
    
    # Set threshold to filter tags
    threshold = 0.001
    tag_indexes = np.where(predictions > threshold)[0]
    tags = [mlb.classes_[i] for i in tag_indexes]
    
    logger.debug(f"Predicted tags: {tags}")
    return tags

def chunk_text(text, max_length=512):
    """Chunk text into smaller pieces if it's too long."""
    logger.debug(f"Chunking text of length {len(text)} into smaller chunks.")
    text_chunks = []
    while len(text) > max_length:
        chunk = text[:max_length]
        text_chunks.append(chunk)
        text = text[max_length:]
    if text:
        text_chunks.append(text)  # Add any remaining part of the text
    
    return text_chunks

def lambda_handler(event, context):
    """AWS Lambda function handler."""
    try:
        # Log incoming event for debugging
        logger.info(f"Received event: {json.dumps(event)}")
        
        # Extract the 'body' from the event
        body = event.get("body", "")
        
        # If the body is a string, parse it to a dictionary (this happens when using Lambda Proxy Integration)
        if isinstance(body, str):
            body = json.loads(body)  # Convert JSON string to dict

        # Get 'text' from the body, default to an empty string if not present
        text = body.get("text", "")
        
        # If no text is provided, return a 400 error
        if not text:
            logger.warning("No text input provided.")
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Text input required"}),
                "headers": {
                    "Access-Control-Allow-Origin": "*",  # Allow all traffic
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",  # Allow the necessary HTTP methods
                }
            }
        
        # Load models within handler to avoid cold start issues
        embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
        tagging_model = load_model_from_s3(BUCKET_NAME, MODEL_S3_KEY)
        mlb = load_labels_from_s3(BUCKET_NAME, MLB_S3_KEY)
        
        # Chunk the text if it's too long
        chunks = chunk_text(text)
        all_tags = []

        # Process each chunk and collect tags
        for chunk in chunks:
            tags = generate_tags(chunk, tagging_model, mlb, embed)
            all_tags.extend(tags)

        # Remove duplicates from the tags and return the result
        all_tags = list(set(all_tags))

        # Return a successful response with the generated tags
        return {
            "statusCode": 200,
            "body": json.dumps({"tags": all_tags}),
            "headers": {
                "Access-Control-Allow-Origin": "*",  # Allow all traffic
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",  # Allow the necessary HTTP methods
            }
        }
    
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Access-Control-Allow-Origin": "*",  # Allow all traffic
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",  # Allow the necessary HTTP methods
            }
        }

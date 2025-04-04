# Use an official Python image as the base
FROM public.ecr.aws/lambda/python:3.10

# Set the working directory
COPY . /var/task

# Copy the application files
COPY . .

# Install dependencies
RUN pip3 install --no-cache-dir numpy tensorflow tensorflow_hub joblib scikit-learn

# Disable AVX2/FMA optimizations (prevents TensorFlow crash)
ENV TF_ENABLE_ONEDNN_OPTS=0

# Ensure that CUDA is disabled in the environment to prevent GPU usage in Lambda
ENV CUDA_VISIBLE_DEVICES=""

# Make sure the function is named correctly (assuming lambda_function.py exists and contains lambda_handler)
CMD ["lambda_function.lambda_handler"]
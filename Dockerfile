# Use an official Python image as the base
FROM public.ecr.aws/lambda/python:3.10

# Set the working directory
COPY . /var/task

# Copy the application files
COPY . .

# Install dependencies
RUN pip3 install --no-cache-dir fastapi numpy tensorflow tensorflow_hub pydantic pandas joblib scikit-learn

# Expose port 8000 for FastAPI app
EXPOSE 8000

# Make sure the function is named correctly (assuming lambda_function.py exists and contains lambda_handler)
CMD ["lambda_function.lambda_handler"]
import subprocess
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
# AWS ECR Details (Replace these with your values)
AWS_ACCOUNT_ID = os.getenv("AWS_ACCOUNT_ID")
AWS_REGION = os.getenv("AWS_REGION")
ECR_REPO_NAME = "my-lambda-tensorflow-repo"
LOCAL_IMAGE = "tag-generator-image"
LOCAL_IMAGE_TAG = "tag-generator-image:latest"
ECR_IMAGE_TAG = f"{AWS_ACCOUNT_ID}.dkr.ecr.{AWS_REGION}.amazonaws.com/{ECR_REPO_NAME}:latest"

def run_command(command):
    """Run a shell command and check for errors."""
    result = subprocess.run(command, shell=True, check=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
        exit(1)
    print(result.stdout)

def main():
    print("🚀 Starting ECR Deployment Workflow...")

    # Step 1: Authenticate with AWS ECR
    print("🔑 Authenticating with AWS ECR...")
    run_command(f"aws ecr get-login-password --region {AWS_REGION} | docker login --username AWS --password-stdin {AWS_ACCOUNT_ID}.dkr.ecr.{AWS_REGION}.amazonaws.com")

    # Step 2: Build the Docker image with specified platform (Amazon Linux) and provenance flag
    print("🔨 Building Docker image...")
    run_command(f"docker build -t {LOCAL_IMAGE_TAG} --platform linux/x86_64 --provenance=false .")

    # Step 3: Tag the Docker image for ECR
    print("🏷️ Tagging Docker image for ECR...")
    run_command(f"docker tag {LOCAL_IMAGE_TAG} {ECR_IMAGE_TAG}")

    # Step 4: Push the Docker image to ECR
    print("📤 Pushing Docker image to ECR...")
    run_command(f"docker push {ECR_IMAGE_TAG}")

    print("✅ Deployment to ECR completed successfully!")

if __name__ == "__main__":
    main()
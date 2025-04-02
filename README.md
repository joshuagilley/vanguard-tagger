# Tag Generator Lambda

This project is a serverless AWS Lambda function that generates tags from text input using a machine learning model.

## Setup & Usage

### Prerequisites

Ensure you have the following installed:

- [Docker](https://www.docker.com/get-started)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- [jq](https://stedolan.github.io/jq/) (for JSON processing in shell scripts)

### Clone the Repository

```sh
git clone https://github.com/yourusername/tag-generator-lambda.git
cd tag-generator-lambda
```

### Running Locally

You can test the Lambda function locally using the provided shell script.

```sh
./run_lambda_local.sh
```

This script will:

1. Build the Docker image.
2. Build the AWS SAM function.
3. Invoke the Lambda function locally with the body from event.json

### File Overview

- `Dockerfile` - Defines the container for the Lambda function.
- `event.json` - Sample input payload.
- `run_lambda_local.sh` - Shell script to automate local testing.
- `template.yaml` - AWS SAM template for deployment.

### Deploying to AWS

To deploy the Lambda function to AWS, use:

```sh
sam deploy --guided
```

Follow the prompts to configure deployment settings.

---

🚀 Happy coding!

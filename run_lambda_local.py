import subprocess
import sys
import json

def run_command(command):
    """Runs a shell command and exits on failure."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error running command: {command}\n{result.stderr}")
        sys.exit(1)
    print(result.stdout)

def main():
    """Main function to build and invoke the AWS Lambda function locally."""
    if len(sys.argv) < 2:
        print("Usage: python run_tagging.py \"Your text input here\"")
        sys.exit(1)

    text_input = sys.argv[1]

    # Construct JSON payload
    json_payload = json.dumps({"body": {"text": text_input}})
    
    print("🚀 Starting Lambda local test workflow...")

    # Build the Docker image
    print("🐳 Building Docker image...")
    run_command("docker build -t tag-generator-image:latest .")

    # Build AWS SAM function
    print("🔨 Building AWS SAM function...")
    run_command("sam build --use-container --build-image tag-generator-image:latest")

    # Invoke the Lambda function locally
    print("⚡ Invoking Lambda function locally...")
    invoke_command = f'echo \'{json_payload}\' | sam local invoke TaggingServiceFunction'
    run_command(invoke_command)

    print("✅ Workflow completed successfully!")

if __name__ == "__main__":
    main()
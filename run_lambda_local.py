import subprocess

def run_command(command, description):
    """Runs a shell command and prints status."""
    print(f"\n{description}...")
    result = subprocess.run(command, shell=True, check=True, text=True)
    print(f"✅ {description} completed!")
    return result

def main():
    print("🚀 Starting Lambda local test workflow...")
    
    # Build Docker image
    run_command("docker build -t tag-generator-image:latest .", "Building Docker image")
    
    # Build AWS SAM function
    run_command("sam build --use-container --build-image tag-generator-image:latest", "Building AWS SAM function")
    
    # Invoke Lambda function locally
    run_command("sam local invoke TaggingServiceFunction -e event.json", "Invoking Lambda function locally")
    
    print("✅ Workflow completed successfully!")

if __name__ == "__main__":
    main()
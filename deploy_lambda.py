import subprocess

def run_script(script_name, description):
    """Runs a Python script and checks for errors."""
    print(f"\n🚀 {description}...")
    result = subprocess.run(f"python {script_name}", shell=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Error: {script_name} failed. Aborting deployment.")
        exit(1)
    
    print(f"✅ {script_name} completed successfully!\n")

def main():
    print("🚀 Starting Lambda Deployment Workflow...")

    # Step 1: Run Local Lambda Test
    run_script("run_lambda_local.py", "Testing Lambda function locally")

    # Step 2: Push to ECR if Lambda test passes
    run_script("push_image_to_ecr.py", "Deploying image to AWS ECR")

    print("🎉 Deployment workflow completed successfully!")

if __name__ == "__main__":
    main()
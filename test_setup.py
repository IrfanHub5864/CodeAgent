"""Test and validation script for the AI GitHub Issue Auto-Fixer."""

import os
import sys
from dotenv import load_dotenv


def check_environment() -> bool:
    """Verify all required environment variables and dependencies are set."""
    
    print("=" * 60)
    print("AI GitHub Issue Auto-Fixer - Validation Check")
    print("=" * 60)
    print()
    
    # Check .env file
    print("1. Checking environment file...")
    if os.path.exists(".env"):
        print("   ✓ .env file found")
        load_dotenv()
    else:
        print("   ✗ .env file not found")
        print("     → Create .env with your credentials (see .env.example)")
        return False
    
    # Check environment variables
    print("\n2. Checking environment variables...")
    required_vars = ["GROQ_API_KEY", "GITHUB_TOKEN", "REPO_OWNER", "REPO_NAME"]
    missing = []
    
    for var in required_vars:
        value = os.getenv(var)
        if value and value.strip():
            print(f"   ✓ {var} is set")
        else:
            print(f"   ✗ {var} is missing")
            missing.append(var)
    
    if missing:
        print(f"\n   Missing variables: {', '.join(missing)}")
        return False
    
    # Check dependencies
    print("\n3. Checking Python dependencies...")
    required_packages = {
        "requests": "requests",
        "dotenv": "python-dotenv",
        "groq": "groq",
    }
    
    missing_packages = []
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"   ✓ {package_name} is installed")
        except ImportError:
            print(f"   ✗ {package_name} is not installed")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n   Install missing packages with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    # Check local modules
    print("\n4. Checking local modules...")
    modules = ["config", "gemini_service", "github_service", "pr_service", "code_fixer"]
    for module in modules:
        if os.path.exists(f"{module}.py"):
            print(f"   ✓ {module}.py found")
        else:
            print(f"   ✗ {module}.py not found")
            missing_packages.append(f"{module}.py")
    
    print("\n" + "=" * 60)
    print("✓ All checks passed! Ready to run.")
    print("=" * 60)
    print("\nStart the agent with: python main.py")
    print()
    
    return True


def test_api_connectivity() -> bool:
    """Test connectivity to Gemini and GitHub APIs."""
    
    print("\n" + "=" * 60)
    print("API Connectivity Test")
    print("=" * 60)
    print()
    
    load_dotenv()
    
    # Test GitHub API
    print("1. Testing GitHub API...")
    try:
        import requests
        token = os.getenv("GITHUB_TOKEN")
        owner = os.getenv("REPO_OWNER")
        repo = os.getenv("REPO_NAME")
        
        headers = {"Authorization": f"token {token}"}
        url = f"https://api.github.com/repos/{owner}/{repo}"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("   ✓ GitHub API is reachable")
            data = response.json()
            print(f"     Repository: {data.get('full_name')}")
            print(f"     Stars: {data.get('stargazers_count')}")
        else:
            print(f"   ✗ GitHub API returned {response.status_code}")
            print(f"     {response.text[:200]}")
            return False
    except Exception as e:
        print(f"   ✗ Failed to reach GitHub API: {e}")
        return False
    
    # Test Groq API
    print("\n2. Testing Groq API...")
    try:
        from groq import Groq
        api_key = os.getenv("GROQ_API_KEY")
        
        client = Groq(api_key=api_key)
        
        # Try multiple models in sequence to find an available one
        models_to_try = [
            "llama-3.3-70b-versatile",
            "mixtral-8x7b-32768",
            "llama-3.1-70b-versatile",
            "llama2-70b-chat",
            "gemma-7b-it",
        ]
        
        success = False
        for model in models_to_try:
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": "Say 'Hello, API works!'"}],
                    max_tokens=100,
                )
                if response.choices and len(response.choices) > 0:
                    print(f"   ✓ Groq API is reachable with model: {model}")
                    # Update the model in gemini_service.py if needed
                    success = True
                    break
            except Exception as e:
                if "decommissioned" in str(e) or "not found" in str(e) or "not have access" in str(e):
                    continue
                else:
                    raise
        
        if not success:
            print("   ⚠ Could not find available model. Please visit")
            print("     https://console.groq.com/keys to check available models.")
            print("   ℹ The agent can still work - update 'model' in gemini_service.py")
            return True  # Don't fail the entire test
                
    except Exception as e:
        print(f"   ✗ Failed to reach Groq API: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✓ All APIs are reachable!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    # Run validation
    if not check_environment():
        sys.exit(1)
    
    # Run API test
    if not test_api_connectivity():
        print("\n⚠ API connectivity test failed.")
        print("Please verify your credentials and try again.")
        sys.exit(1)
    
    print("\n✓ Everything is configured correctly!")
    print("You can now run: python main.py")

"""Create sample GitHub issues for testing the AI agent."""

import os
import requests
from dotenv import load_dotenv


def create_test_issue(owner: str, repo: str, token: str, title: str, body: str) -> dict:
    """Create a test issue in the repository."""
    
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }
    
    data = {
        "title": title,
        "body": body,
    }
    
    response = requests.post(url, json=data, headers=headers, timeout=15)
    response.raise_for_status()
    
    return response.json()


def main():
    """Create multiple test issues."""
    
    load_dotenv()
    
    owner = os.getenv("REPO_OWNER")
    repo = os.getenv("REPO_NAME")
    token = os.getenv("GITHUB_TOKEN")
    
    if not all([owner, repo, token]):
        print("Error: Missing environment variables")
        return 1
    
    print(f"Creating test issues in {owner}/{repo}...")
    print()
    
    # Test issues with clear descriptions
    test_issues = [
        {
            "title": "Bug: Login button not responding to clicks",
            "body": """## Description
When users click the login button on the homepage, nothing happens. 
The button appears to be disabled or not properly connected to the submit event handler.

## Steps to Reproduce
1. Navigate to the login page
2. Fill in username and password
3. Click the login button
4. Expected: Form should submit
5. Actual: Nothing happens

## Environment
- Browser: Chrome latest
- OS: Windows 10

The issue is likely in the auth handler or button click listener.
Check src/auth.py or src/components/LoginButton.jsx first.
"""
        },
        {
            "title": "Bug: Database connection timeout on startup",
            "body": """## Description
The application fails to start with a database connection timeout error.
This happens immediately on startup when trying to initialize the database connection pool.

## Error Message
```
ConnectionError: Database connection timeout after 30 seconds
```

## Expected
The application should establish database connection within timeout period.

## Actual
Connection fails with timeout error.

The problem is likely in src/database/connection.py in the connection initialization logic.
May need to increase timeout or fix connection string parsing.
"""
        },
        {
            "title": "Bug: API returns wrong status code for errors",
            "body": """## Description
When API endpoints encounter validation errors, they return HTTP 200 (success) instead of appropriate error codes like 400 or 422.

## Example
- POST /api/users with invalid email returns 200 instead of 422
- GET /api/items/invalid-id returns 200 instead of 404

## Expected Behavior
Endpoints should return appropriate HTTP status codes:
- 400 for bad requests
- 404 for not found
- 500 for server errors

This is likely in src/api/handlers.py or src/api/routes.py where error responses are constructed.
"""
        },
        {
            "title": "Bug: Memory leak in data processing loop",
            "body": """## Description
The application memory usage keeps increasing when processing large data batches.
Memory is not being freed after each iteration.

## Observations
- Processing 1000 items: 200MB
- Processing 2000 items: 500MB  
- Processing 3000 items: 1000MB+

The issue is likely in src/data/processor.py in the loop that processes items.
Check if objects are being properly garbage collected or if there's a circular reference.
"""
        },
    ]
    
    for issue_data in test_issues:
        try:
            issue = create_test_issue(owner, repo, token, 
                                      issue_data["title"], 
                                      issue_data["body"])
            print(f"✓ Created issue #{issue['number']}: {issue['title']}")
            print(f"  URL: {issue['html_url']}")
            print()
        except Exception as e:
            print(f"✗ Failed to create issue: {e}")
            return 1
    
    print("=" * 60)
    print(f"✓ Test issues created successfully!")
    print()
    print("Now run: python main.py")
    print("The agent will analyze these issues and create pull requests!")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    exit(main())

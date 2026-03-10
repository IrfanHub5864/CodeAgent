"""Create sample GitHub issues for testing the AI agent."""

import os
import requests
from dotenv import load_dotenv


def close_all_issues(owner: str, repo: str, token: str) -> None:
    """Close every open issue in the repository."""
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }

    params = {"state": "open", "per_page": 100}
    response = requests.get(url, headers=headers, params=params, timeout=15)
    response.raise_for_status()
    for issue in response.json():
        number = issue["number"]
        patch_url = f"{url}/{number}"
        requests.patch(patch_url, headers=headers, json={"state": "closed"}, timeout=15)
    print("All open issues have been closed.")


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

    # clear any existing issues before generating new ones
    close_all_issues(owner, repo, token)
    
    print(f"Creating test issues in {owner}/{repo}...")
    print()
    
    # Test issues with clear descriptions (only one to stay under rate limits)
    test_issues = [
        {
            "title": "Bug: Dashboard has XSS vulnerability and data loading errors",
            "body": """## Description
The dashboard component has multiple critical security and functional issues:
1. XSS vulnerability - uses dangerouslySetInnerHTML without sanitization
2. Missing await on fetch - data is promise instead of actual data
3. No null/error handling before rendering

## Steps to Reproduce
1. Go to /dashboard
2. Inject malicious HTML in description field
3. Expected: HTML escaped
4. Actual: Script executes

## Issues Found
- Missing await on response.json()
- No validation of data before rendering
- Unsafe use of dangerouslySetInnerHTML

The issue is in src/components/Dashboard.jsx in the fetchDashboardData and renderStats functions.
Fix the async/await, add data validation, and sanitize HTML properly.
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

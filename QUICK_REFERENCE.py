#!/usr/bin/env python3
"""Quick reference and usage examples for AI GitHub Issue Auto-Fixer."""

QUICK_START = """
╔════════════════════════════════════════════════════════════════╗
║       AI GitHub Issue Auto-Fixer - Quick Start Guide          ║
╚════════════════════════════════════════════════════════════════╝

STEP 1: Install Dependencies
─────────────────────────────
$ pip install -r requirements.txt

STEP 2: Get Your Credentials
─────────────────────────────
GitHub Token:
  • Go to: https://github.com/settings/tokens
  • Click "Generate new token (classic)"
  • Select scope: ✓ repo
  • Copy the token

Groq API Key:
  • Go to: https://console.groq.com/keys
  • Click "Create API Key"
  • Copy the key

STEP 3: Set Up Environment
──────────────────────────
Create .env file:

    GROQ_API_KEY=your_groq_api_key
    GITHUB_TOKEN=your_github_token
    REPO_OWNER=your_username_or_org
    REPO_NAME=your_repository_name

STEP 4: Validate Setup
──────────────────────
$ python test_setup.py

Expected output:
    ✓ All checks passed! Ready to run.
    ✓ All APIs are reachable!

STEP 5: Run the Agent
─────────────────────
$ python main.py

Watch it:
  1. Fetch all open issues
  2. Analyze each with Gemini
  3. Identify problematic files
  4. Generate code fixes
  5. Create pull requests
"""

WORKFLOW_DIAGRAM = """
┌─────────────────────────────────────────────────────────────┐
│               Issue Analysis & PR Creation Workflow          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  GitHub Issues  (open, not PRs)                           │
│       ↓                                                    │
│  [main.py]                                                │
│       ├─→ Get Issues (github_service.py)                 │
│       ├─→ Analyze Issue (gemini_service.py)              │
│       │   ├─→ Identify root cause                        │
│       │   └─→ Pinpoint problematic file                  │
│       │                                                  │
│       ├─→ Generate Fix (gemini_service.py)               │
│       │   └─→ Suggest concrete code changes              │
│       │                                                  │
│       ├─→ Extract Details (code_fixer.py)                │
│       │   ├─→ Find affected file path                    │
│       │   └─→ Extract code snippet                       │
│       │                                                  │
│       └─→ Create PR (pr_service.py)                      │
│           ├─→ Create fix branch                          │
│           ├─→ Fetch file from repo                       │
│           ├─→ Commit changes                             │
│           └─→ Create pull request                        │
│                                                          │
│  New PR on GitHub (Ready for Review)                    │
│                                                          │
└─────────────────────────────────────────────────────────────┘
"""

EXAMPLE_OUTPUT = """
Example Run Output:
───────────────────

Collecting open issues from myuser/myrepo...

Issue #42: Login button not responding on mobile
URL: https://github.com/myuser/myrepo/issues/42
────────────────────────────────────────────────────────────

Analyzing issue with Groq...
Groq analysis:
 The issue appears to be in the event handler for the login button.
 The mobile viewport may not trigger the click event properly.
 File(s): src/components/LoginButton.jsx

✓ Identified file: src/components/LoginButton.jsx
✓ Code snippet extracted from fix suggestion

Attempting to create pull request...
✓ Pull request created successfully!
  PR URL: https://github.com/myuser/myrepo/pull/123
  PR #123: Fix: Automated fix for issue #42

────────────────────────────────────────────────────────────
"""

TROUBLESHOOTING = """
╔════════════════════════════════════════════════════════════════╗
║                    Troubleshooting Guide                       ║
╚════════════════════════════════════════════════════════════════╝

PROBLEM: "Configuration error: The following environment variables must be set"
─────────────────────────────────────────────────────────────────────────────
SOLUTION:
  1. Make sure you created .env file (not .env.txt or .env.example)
  2. Check all 4 required variables are set:
     - GEMINI_API_KEY (not empty)
     - GITHUB_TOKEN (not empty)
     - REPO_OWNER (your username/org)
     - REPO_NAME (repository name)
  3. No quotes needed in .env file
  4. Restart your terminal after creating .env

PROBLEM: "No open issues were returned"
──────────────────────────────────────
SOLUTION:
  1. Verify your repository has open issues (not closed)
  2. Check REPO_OWNER spelling (case-sensitive)
  3. Check REPO_NAME spelling (case-sensitive)
  4. Verify GitHub token has access to your repo
  5. Try running: git ls-remote https://github.com/REPO_OWNER/REPO_NAME

PROBLEM: "GitHub API error (401): Bad credentials"
───────────────────────────────────────────────────
SOLUTION:
  1. GitHub token is invalid or expired
  2. Generate a new token from: https://github.com/settings/tokens
  3. Token needs 'repo' scope (full control)
  4. Update GITHUB_TOKEN in .env

PROBLEM: "Could not determine file path from analysis"
───────────────────────────────────────────────────────
SOLUTION:
  1. Issue description is too vague
  2. Try updating the issue with more details
  3. Mention the file name explicitly in the issue
  4. Example: "Bug is in src/utils/helpers.py when calling..."

PROBLEM: "Failed to create pull request"
────────────────────────────────────────
SOLUTION:
  1. GitHub token lacks 'repo' scope - regenerate it
  2. Branch might already exist - check your repo
  3. Repository might not allow PRs (check settings)
  4. Permission restricted - verify token access

PROBLEM: "Groq API request failed"
──────────────────────────────────
SOLUTION:
  1. API key is invalid - get new one from https://console.groq.com/keys
  2. API quota exceeded - wait a bit before retrying
  3. Rate limited - wait before running again
"""

COMMANDS = """
╔════════════════════════════════════════════════════════════════╗
║                    Command Reference                          ║
╚════════════════════════════════════════════════════════════════╝

Main Commands:
──────────────
python main.py              Run the agent (process all issues)
python test_setup.py        Validate setup and test APIs
python student_manager.py   Run demo code (standalone)

Useful One-Liners:
──────────────────
# Check if .env is set up
cat .env

# Install just the required packages
pip install requests python-dotenv groq

# Test GitHub API connection
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user

# List your repos
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user/repos
"""

if __name__ == "__main__":
    print(QUICK_START)
    print("\n")
    print(WORKFLOW_DIAGRAM)
    print("\n")
    print(EXAMPLE_OUTPUT)
    print("\n")
    print(TROUBLESHOOTING)
    print("\n")
    print(COMMANDS)
    print("""
For more details, see:
  • README.md - Full documentation
  • COMPLETION_SUMMARY.md - What was built
  • Individual module docstrings - Implementation details

Questions? Check the error messages - they're informative!
""")

"""GitHub pull request management and code commit operations."""

from typing import Dict, Optional, Tuple
import base64
import requests


def get_default_branch(owner: str, repo: str, token: str) -> str:
    """Get the default branch name for the repository.
    
    Returns:
        The default branch name (e.g., 'main', 'master')
    """
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        default_branch = data.get("default_branch", "main")
        return default_branch
    except Exception as e:
        print(f"Could not fetch default branch, trying fallback: {e}")
        
        # Fallback: try to detect branch by checking common names
        branches_to_try = ["main", "master", "develop", "development"]
        for branch in branches_to_try:
            try:
                ref_url = f"https://api.github.com/repos/{owner}/{repo}/git/ref/heads/{branch}"
                ref_response = requests.get(ref_url, headers=headers, timeout=15)
                if ref_response.status_code == 200:
                    return branch
            except:
                continue
        
        # If all else fails, return main
        return "main"


def get_file_content(
    owner: str,
    repo: str,
    file_path: str,
    token: str,
    branch: str = None,
) -> Tuple[str, str]:
    """Fetch file content and SHA from GitHub.
    
    Returns:
        Tuple of (content, sha) for the file, or ('', '') if file doesn't exist.
    """
    if branch is None:
        branch = get_default_branch(owner, repo, token)
    
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }
    params = {"ref": branch}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        
        if response.status_code == 404:
            # File doesn't exist - return empty sha
            return "", ""
        
        response.raise_for_status()
        
        data = response.json()
        content = base64.b64decode(data["content"]).decode("utf-8")
        sha = data["sha"]
        
        return content, sha
    except Exception as e:
        print(f"Warning: Could not fetch file {file_path}: {e}")
        return "", ""


def create_branch(
    owner: str,
    repo: str,
    token: str,
    branch_name: str,
    base_branch: str = None,
) -> bool:
    """Create a new branch in the repository.
    
    Returns:
        True if successful, False otherwise.
    """
    # If base_branch not specified, get the default branch
    if base_branch is None:
        try:
            base_branch = get_default_branch(owner, repo, token)
        except Exception as e:
            print(f"Could not get default branch: {e}")
            base_branch = "main"
    
    url = f"https://api.github.com/repos/{owner}/{repo}/git/refs"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }
    
    # Get the SHA of the base branch
    ref_url = f"https://api.github.com/repos/{owner}/{repo}/git/ref/heads/{base_branch}"
    try:
        ref_response = requests.get(ref_url, headers=headers, timeout=15)
        ref_response.raise_for_status()
        base_sha = ref_response.json()["object"]["sha"]
    except requests.exceptions.HTTPError as e:
        print(f"Failed to get base branch SHA: {e}")
        print(f"Attempted branch: {base_branch}")
        return False
    
    data = {
        "ref": f"refs/heads/{branch_name}",
        "sha": base_sha,
    }
    
    response = requests.post(url, json=data, headers=headers, timeout=15)
    
    # 201 = created, 422 = already exists (also acceptable)
    return response.status_code in [201, 422]


def update_file(
    owner: str,
    repo: str,
    file_path: str,
    new_content: str,
    token: str,
    branch: str,
    commit_message: str,
    file_sha: str,
) -> bool:
    """Update a file in the repository.
    
    Returns:
        True if successful.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }
    
    data = {
        "message": commit_message,
        "content": base64.b64encode(new_content.encode()).decode(),
        "sha": file_sha,
        "branch": branch,
    }
    
    response = requests.put(url, json=data, headers=headers, timeout=15)
    response.raise_for_status()
    
    return response.status_code == 200


def create_pull_request(
    owner: str,
    repo: str,
    token: str,
    head_branch: str,
    base_branch: str,
    title: str,
    body: str,
) -> Optional[Dict]:
    """Create a pull request in the repository.
    
    Returns:
        PR data dict if successful, None otherwise.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }
    
    data = {
        "title": title,
        "body": body,
        "head": head_branch,
        "base": base_branch,
    }
    
    response = requests.post(url, json=data, headers=headers, timeout=15)
    
    if response.status_code == 201:
        return response.json()
    elif response.status_code == 422:
        # PR already exists
        error = response.json()
        print(f"Pull request may already exist: {error}")
        return None
    else:
        response.raise_for_status()
        return None


def create_pr_with_fix(
    owner: str,
    repo: str,
    token: str,
    issue_number: int,
    file_path: str,
    file_changes: str,
    branch_name: str = None,
) -> Optional[Dict]:
    """Create a pull request with the proposed fix.
    
    Args:
        owner: Repository owner
        repo: Repository name
        token: GitHub API token
        issue_number: The GitHub issue number this PR fixes
        file_path: Path to the file to modify
        file_changes: New content for the file
        branch_name: Name of the branch to create (auto-generated if None)
    
    Returns:
        PR data dict if successful, None otherwise.
    """
    if branch_name is None:
        branch_name = f"fix/issue-{issue_number}"
    
    try:
        # Get the default branch first
        default_branch = get_default_branch(owner, repo, token)
        print(f"ℹ Using branch: {default_branch}")
        
        # Step 1: Create a new branch
        if not create_branch(owner, repo, token, branch_name, default_branch):
            print(f"⚠ Could not create branch {branch_name}")
            print(f"ℹ This might be because the repository is empty or sparse.")
            print(f"ℹ Analysis complete - manually create PR with the suggested fix.")
            return None
        
        # Step 2: Get the current file content and SHA
        content, sha = get_file_content(
            owner, repo, file_path, token, branch=branch_name
        )
        
        if not sha:
            print(f"⚠ File {file_path} does not exist in the repository")
            print(f"ℹ To apply the fix, create this file with the suggested code.")
            return None
        
        # Step 3: Update the file with the fix
        commit_msg = f"Fix for issue #{issue_number}: automated fix using AI agent"
        if not update_file(
            owner, repo, file_path, file_changes, token, 
            branch_name, commit_msg, sha
        ):
            print(f"Failed to update file {file_path}")
            return None
        
        # Step 4: Create the pull request
        pr_title = f"Fix: Automated fix for issue #{issue_number}"
        pr_body = (
            f"This PR addresses issue #{issue_number}.\n\n"
            f"**Changes made:**\n"
            f"- Modified `{file_path}`\n\n"
            f"Generated by AI agent for automated bug fixing."
        )
        
        pr = create_pull_request(
            owner, repo, token, branch_name, default_branch,
            pr_title, pr_body
        )
        
        return pr
        
    except Exception as exc:
        print(f"Error during PR creation process: {exc}")
        return None

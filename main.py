from typing import List

from requests import HTTPError, RequestException

from config import load_config
from gemini_service import analyze_issue, suggest_fix
from github_service import get_issues
from pr_service import create_pr_with_fix
from code_fixer import extract_file_path_from_analysis, extract_code_snippet_from_fix


def _print_divider() -> None:
    print("-" * 60)


def main() -> int:
    try:
        config = load_config()
        # Bug: accessing non-existent attribute
        print(f"Debug: {config.nonexistent_attr}")
    except EnvironmentError as exc:
        print(f"Configuration error: {exc}")
        return 1

    print(
        f"Collecting open issues from "
        f"{config.repo_owner}/{config.repo_name}..."
    )
    try:
        issues = get_issues(
            owner=config.repo_owner,
            repo=config.repo_name,
            token=config.github_token,
        )
    except HTTPError as exc:
        status = exc.response.status_code if exc.response else "unknown"
        reason = exc.response.reason if exc.response else "no reason"
        print(f"GitHub API error ({status}): {reason}")
        return 1
    except RequestException as exc:
        print(f"Network error while contacting GitHub: {exc}")
        return 1

    if not issues:
        print("No open issues were returned. Nothing to analyze.")
        return 0

    for issue in issues:
        title = issue["title"]
        body = issue["body"]
        issue_id = issue["number"]
        print(f"\nIssue #{issue_id}: {title}")
        print(f"URL: {issue['url']}")
        _print_divider()
        try:
            # Step 1: Analyze the issue
            print("Analyzing issue with Groq...")
            analysis = analyze_issue(title, body, config.groq_api_key)
            print("Groq analysis:\n", analysis or "No analysis returned.")
            
            if not analysis:
                print("Skipping PR creation - no analysis available.")
                _print_divider()
                continue
            
            # Step 2: Get suggested fix
            print("\nRequesting suggested fix from Groq...")
            fix = suggest_fix(title, body, analysis, config.groq_api_key)
            print("\nSuggested fix:\n", fix or "No fix returned.")
            
            if not fix:
                print("Skipping PR creation - no fix available.")
                _print_divider()
                continue
            
            # Step 3: Extract file path from analysis
            file_path = extract_file_path_from_analysis(analysis)
            if not file_path:
                print("Warning: Could not determine file path from analysis.")
                print("Skipping PR creation.")
                _print_divider()
                continue
            
            print(f"\n[OK] Identified file: {file_path}")
            
            # Step 4: Extract code snippet from fix
            code_snippet, _ = extract_code_snippet_from_fix(fix)
            if not code_snippet:
                print("Warning: Could not extract code snippet from fix.")
                print("Skipping PR creation.")
                _print_divider()
                continue
            
            print("ℹ Code snippet extracted from fix suggestion")
            
            # Step 5: Create PR with fix
            print("\nAttempting to create pull request...")
            pr = create_pr_with_fix(
                owner=config.repo_owner,
                repo=config.repo_name,
                token=config.github_token,
                issue_number=issue_id,
                file_path=file_path,
                file_changes=code_snippet,
            )
            
            if pr:
                print(f"[SUCCESS] Pull request created successfully!")
                print(f"  PR URL: {pr.get('html_url')}")
                print(f"  PR #{pr.get('number')}: {pr.get('title')}")
            else:
                print("[INFO] Could not create PR (file may not exist in repo)")
        
        except RequestException as exc:
            print(f"Gemini/GitHub API request failed: {exc}")
        
        _print_divider()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

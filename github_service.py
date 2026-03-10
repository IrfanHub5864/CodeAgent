"""Simple wrapper around the GitHub REST API for issue retrieval."""

from typing import Any, Dict, List

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def get_issues(
    owner: str,
    repo: str,
    token: str,
    state: str = "open",
    per_page: int = 20,
) -> List[Dict[str, Any]]:
    """Fetch the most recent GitHub issues that are not pull requests."""

    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }
    params = {"state": state, "per_page": per_page}
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )

    with requests.Session() as session:
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        response = session.get(url, headers=headers, params=params, timeout=15)
    response.raise_for_status()

    raw_issues = response.json()
    issues = []
    for issue in raw_issues:
        if "pull_request" in issue:
            continue
        issues.append(
            {
                "number": issue.get("number"),
                "title": issue.get("title", "No title"),
                "body": issue.get("body") or "",
                "url": issue.get("html_url"),
            }
        )
    return issues

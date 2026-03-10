"""Integration helpers for Groq API calls."""

from typing import List

from groq import Groq


def _call_groq(messages: List[dict], api_key: str) -> str:
    """Send a multi-message conversation to Groq and return the assistant text."""

    client = Groq(api_key=api_key)
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=2048,
        timeout=30,
    )
    
    if response.choices and len(response.choices) > 0:
        return response.choices[0].message.content.strip()
    
    return ""


def analyze_issue(title: str, description: str, api_key: str) -> str:
    """Ask Groq to analyze the issue and identify the likely buggy file."""

    system_prompt = (
        "You are a senior software engineer that specializes in debugging "
        "GitHub issues. Identify the root cause and name (or guess) the file "
        "that most likely contains the bug."
    )
    user_prompt = (
        f"Title: {title}\n\n"
        f"Description:\n{description or 'No description provided.'}\n\n"
        "Please analyze the bug, describe why it fails, and answer the "
        "following questions:\n"
        "1. What is the likely root cause?\n"
        "2. Which file or module should be inspected first? "
        "Prefix your answer with 'File(s):' if possible.\n"
        "3. What additional context or reproduction hints matter?"
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    return _call_groq(messages, api_key)


def suggest_fix(
    title: str, description: str, analysis: str, api_key: str
) -> str:
    """Prompt Groq to propose a concrete fix after the analysis."""

    system_prompt = (
        "You are a practical engineer who writes actionable bug fixes, "
        "including code snippets, steps, and file references."
    )
    user_prompt = (
        "Using the following GitHub issue and analysis, propose a suggested fix.\n\n"
        f"Issue title: {title}\n\n"
        f"Issue description:\n{description or 'No description provided.'}\n\n"
        f"Analysis context:\n{analysis}\n\n"
        "Please respond with:\n"
        "- A short summary of what must change.\n"
        "- Which file(s) to edit.\n"
        "- At least one concise code snippet or configuration change."
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    return _call_groq(messages, api_key)

"""Integration helpers for Groq API calls."""

from typing import List

from groq import Groq


def _call_groq(messages: List[dict], api_key: str) -> str:
    """Send a multi-message conversation to Groq and return the assistant text."""

    client = Groq(api_key=api_key)
    
    try:
        response = client.chat.completions.create(
            model="llama-3.2-1b-preview",
            messages=messages,
            max_tokens=1500,
            timeout=15,  # Reduced from 30 to 15 seconds
        )
        
        if response.choices and len(response.choices) > 0:
            return response.choices[0].message.content.strip()
        
        return ""
    except Exception as e:
        print(f"[ERROR] Groq API error: {str(e)}")
        print(f"[INFO] Please check your API key at https://console.groq.com")
        raise


def analyze_issue(title: str, description: str, api_key: str) -> str:
    """Ask Groq to analyze the issue and identify the likely buggy file."""

    system_prompt = (
        "You are a senior software engineer that specializes in debugging "
        "GitHub issues. Identify the root cause and name (or guess) the file "
        "that most likely contains the bug. Be concise."
    )
    user_prompt = (
        f"Title: {title}\n\n"
        f"Description:\n{description or 'No description provided.'}\n\n"
        "Analyze this bug briefly and answer:\n"
        "1. Root cause?\n"
        "2. Which file first?\n"
        "3. What context matters?"
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

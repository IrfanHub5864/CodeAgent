"""Code analysis and patching utilities for applying Gemini-suggested fixes."""

import re
from typing import Optional, Tuple


def extract_file_path_from_analysis(analysis: str) -> Optional[str]:
    """Extract the file path from Gemini's issue analysis.
    
    Looks for patterns like:
    - File(s): path/to/file.py
    - The file: path/to/file.py
    - in path/to/file.py
    """
    # Pattern 1: "File(s): path/to/file"
    match = re.search(r"File\(s\):\s*[`\"]?([^\s`\"]+)[`\"]?", analysis, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    # Pattern 2: "filename.py" or "path/to/file.py"
    match = re.search(r"(?:the file|file)\s*[`\"]?([a-zA-Z0-9_/.\\-]+\.(?:py|js|ts|java|rb|go|rs|cpp|c|h|cs))[`\"]?", analysis, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    # Pattern 3: Just a file path pattern
    match = re.search(r"([a-zA-Z0-9_/.\\-]+\.(?:py|js|ts|java|rb|go|rs|cpp|c|h|cs))", analysis)
    if match:
        return match.group(1).strip()
    
    return None


def extract_code_snippet_from_fix(fix: str) -> Optional[Tuple[str, str]]:
    """Extract code snippet and context from the fix suggestion.
    
    Returns:
        Tuple of (code_snippet, description) or (None, None) if not found.
    """
    # Look for code blocks with optional language specification
    code_pattern = r"```\w*\n(.*?)\n```"
    match = re.search(code_pattern, fix, re.DOTALL | re.IGNORECASE)
    
    if match:
        return match.group(1), fix
    
    # Fallback: look for any code block without language
    code_pattern = r"```\n(.*?)\n```"
    match = re.search(code_pattern, fix, re.DOTALL)
    
    if match:
        return match.group(1), fix
    
    return None, None


def apply_simple_replacement(
    original_content: str,
    old_code: str,
    new_code: str,
) -> Optional[str]:
    """Apply a simple code replacement.
    
    Args:
        original_content: The original file content
        old_code: The old code to find
        new_code: The new code to replace it with
    
    Returns:
        Updated content or None if replacement failed.
    """
    if old_code not in original_content:
        print(f"Warning: Could not find exact match for code snippet")
        return None
    
    return original_content.replace(old_code, new_code, 1)


def parse_fix_description(fix: str) -> dict:
    """Parse the fix description for key information.
    
    Returns dict with keys:
    - summary: Short summary of the fix
    - files: List of files to edit
    - changes: Description of changes
    """
    result = {
        "summary": "",
        "files": [],
        "changes": "",
    }
    
    # Extract summary (usually first line or paragraph)
    lines = fix.split("\n")
    result["summary"] = lines[0] if lines else ""
    
    # Look for files mentioned
    file_pattern = r"(?:file|edit|modify|change|update)\s+[`\"]?([a-zA-Z0-9_/.\\-]+\.[a-zA-Z0-9]+)"
    files = re.findall(file_pattern, fix, re.IGNORECASE)
    result["files"] = list(set(files))  # Remove duplicates
    
    # Extract the main changes text
    if "**Changes" in fix or "**Changes made" in fix:
        parts = fix.split("**Changes")
        if len(parts) > 1:
            result["changes"] = parts[1][:500]  # First 500 chars
    
    return result


def generate_improved_code(
    original_code: str,
    fix_suggestion: str,
    file_path: str,
) -> Optional[str]:
    """Generate improved code by integrating the suggestion.
    
    This attempts to be smart about applying fixes:
    1. First tries exact code block replacement
    2. Falls back to looking for similar patterns
    """
    code_snippet, _ = extract_code_snippet_from_fix(fix_suggestion)
    
    if not code_snippet:
        print("No code snippet found in fix suggestion")
        return None
    
    # Try exact replacement first
    result = apply_simple_replacement(original_code, code_snippet, code_snippet)
    if result:
        return result
    
    # If exact replacement fails, look for similar patterns
    # For now, we could enhance this with fuzzy matching or AST-based approaches
    print(f"Could not apply fix directly to {file_path}")
    return None

# AI-Powered GitHub Issue Auto-Fixer

An automated agent that reads GitHub issues, analyzes them with Groq AI, generates bug fixes, and creates pull requests.

## Features

✅ **Automated Issue Analysis** - Uses Groq to understand bugs  
✅ **Root Cause Detection** - Identifies which files contain the bugs  
✅ **Intelligent Fix Generation** - Suggests concrete code fixes  
✅ **Automated PR Creation** - Creates pull requests with fixes  
✅ **Error Handling** - Robust error handling and reporting  

## Prerequisites

- Python 3.8+
- GitHub repository with at least one open issue
- Groq API key
- GitHub personal access token (with `repo` scope)

## Setup

### 1. Clone or navigate to the project

```bash
cd c:/ai_gi
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the project root:

```bash
GROQ_API_KEY=your_groq_api_key_here
GITHUB_TOKEN=your_github_token_here
REPO_OWNER=your_username_or_org
REPO_NAME=your_repository_name
```

**How to get credentials:**

- **Groq API Key**: Get it from [Groq Console](https://console.groq.com/keys)
- **GitHub Token**: Generate from [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
  - Required scopes: `repo` (full control)

### 4. Run the agent

```bash
python main.py
```

## How It Works

1. **Fetch Issues** - Retrieves open GitHub issues from your repository
2. **Analyze** - Groq analyzes each issue to understand the bug
3. **Identify File** - Determines which file(s) contain the problematic code
4. **Generate Fix** - Groq suggests a concrete code fix
5. **Create PR** - Automatically creates a pull request with the fix

## Output Example

```
Collecting open issues from username/repo...

Issue #42: Button click not working
URL: https://github.com/username/repo/issues/42
------------------------------------------------------------
Analyzing issue with Groq...
Groq analysis:
 The issue is likely in the event handler...

✓ Identified file: src/components/Button.py
✓ Code snippet extracted from fix suggestion

Attempting to create pull request...
✓ Pull request created successfully!
  PR URL: https://github.com/username/repo/pull/123
  PR #123: Fix: Automated fix for issue #42
------------------------------------------------------------
```

## Project Structure

```
.
├── main.py              # Entry point and orchestration
├── config.py            # Configuration management
├── gemini_service.py    # Google Gemini API integration
├── github_service.py    # GitHub API integration for issue fetching
├── pr_service.py        # GitHub PR creation and file management
├── code_fixer.py        # Code analysis and patching utilities
├── student_manager.py   # Demo/sample code (standalone)
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables (create this)
```

## Advanced Usage

### Analyzing Specific Issues Only

Modify `main.py` to filter issues by label, milestone, or custom criteria.

### Enabling PR Auto-Merge

Add auto-merge logic after PR creation in `pr_service.py`.

### Supporting More Languages

Update `code_fixer.py` regex patterns to support additional programming languages.

## Troubleshooting

### No Issues Found
- Verify your repository has open issues
- Check GitHub token has correct permissions
- Ensure REPO_OWNER and REPO_NAME are correct

### Gemini API Errors
- Verify GROQ_API_KEY is valid and has quota available
- Check API response in error message for specific issues
- Ensure your IP isn't blocked by rate limits

### PR Creation Fails
- Verify GitHub token has `repo` scope
- Check file path is correctly identified from analysis
- Ensure branch doesn't already exist

### Code Snippet Not Applied
- The fix suggestion might not match exact code in the file
- Consider manual intervention for complex fixes
- Check if file encoding is UTF-8

## Customization Examples

### Use Different Groq Model
In `gemini_service.py`, change the model in `_call_groq`:
```python
model="llama-2-70b-chat"  # or other available models
```

### Filter Issues by Label
In `github_service.py`, add label filtering:
```python
params = {"state": state, "per_page": per_page, "labels": "bug"}
```

### Draft PRs Instead of Publishing
In `pr_service.py`, set `draft=True` when creating PR:
```python
data = {..., "draft": True}
```

## Limitations

- Works best with straightforward bugs
- Complex logic changes may require human review
- Requires clear issue descriptions for accurate analysis
- Branch names are auto-generated (fix/issue-N)
- No support for multi-file fixes yet

## Future Enhancements

- [ ] Multi-file fix support
- [ ] Automatic test execution
- [ ] PR auto-merge for simple fixes
- [ ] Slack/Discord notifications
- [ ] Support for commit signatures
- [ ] Custom instructions per repository
- [ ] Issue template parsing

## License

MIT

## Support

For issues or questions, create an issue in your repository or review the error logs for debugging hints.

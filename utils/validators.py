"""
Input Validation Functions
Ensures user inputs are valid before processing
"""

import re
from typing import Tuple


def validate_github_url(url: str) -> Tuple[bool, str, str]:
    """
    Validates a GitHub profile URL and extracts the username.
    
    Args:
        url: The URL or username to validate
        
    Returns:
        Tuple of (is_valid, username, error_message)
        
    Examples:
        >>> validate_github_url("https://github.com/octocat")
        (True, "octocat", "")
        
        >>> validate_github_url("octocat")
        (True, "octocat", "")
        
        >>> validate_github_url("")
        (False, "", "Please enter a GitHub URL or username")
    """
    
    # Handle empty input
    if not url or not url.strip():
        return False, "", "Please enter a GitHub URL or username"
    
    url = url.strip()
    
    # Pattern 1: Full GitHub URL
    # Matches: https://github.com/username or http://github.com/username
    github_url_pattern = r'^https?://github\.com/([a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,38})/?$'
    
    # Pattern 2: Just the username
    # GitHub username rules: alphanumeric, can contain hyphens (not at start/end)
    username_pattern = r'^[a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,38}$'
    
    # Try matching full URL first
    url_match = re.match(github_url_pattern, url)
    if url_match:
        username = url_match.group(1)
        return True, username, ""
    
    # Try matching just username
    username_match = re.match(username_pattern, url)
    if username_match:
        return True, url, ""
    
    # Invalid input
    return False, "", "Invalid GitHub URL or username. Please check and try again."


def is_valid_github_username(username: str) -> bool:
    """
    Quick check if a string is a valid GitHub username format.
    
    Args:
        username: The username to validate
        
    Returns:
        True if valid format, False otherwise
    """
    if not username:
        return False
        
    pattern = r'^[a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,38}$'
    return bool(re.match(pattern, username))
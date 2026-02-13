"""
Helper Functions
General-purpose utility functions used across the application
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any
import re


def calculate_days_between(start_date: str, end_date: str = None) -> int:
    """
    Calculate the number of days between two dates.
    
    Args:
        start_date: ISO format date string
        end_date: ISO format date string (defaults to today)
        
    Returns:
        Number of days between the dates
    """
    start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
    
    if end_date:
        end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
    else:
        end = datetime.now(start.tzinfo)
    
    return (end - start).days


def format_number(number: int) -> str:
    """
    Format large numbers for display (e.g., 1500 -> 1.5K)
    
    Args:
        number: The number to format
        
    Returns:
        Formatted string representation
    """
    if number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number / 1_000:.1f}K"
    else:
        return str(number)


def get_score_grade(score: float) -> str:
    """
    Convert a numerical score to a letter grade.
    
    Args:
        score: Score from 0-100
        
    Returns:
        Letter grade (A+, A, B+, etc.)
    """
    if score >= 95:
        return "A+"
    elif score >= 90:
        return "A"
    elif score >= 85:
        return "A-"
    elif score >= 80:
        return "B+"
    elif score >= 75:
        return "B"
    elif score >= 70:
        return "B-"
    elif score >= 65:
        return "C+"
    elif score >= 60:
        return "C"
    elif score >= 55:
        return "C-"
    elif score >= 50:
        return "D"
    else:
        return "F"


def get_score_color(score: float) -> str:
    """
    Get the appropriate color for a score value.
    
    Args:
        score: Score from 0-100
        
    Returns:
        Hex color code
    """
    if score >= 80:
        return "#00C853"  # Green
    elif score >= 60:
        return "#64DD17"  # Light Green
    elif score >= 40:
        return "#FFD600"  # Yellow
    elif score >= 20:
        return "#FF6D00"  # Orange
    else:
        return "#FF1744"  # Red


def extract_readme_sections(readme_content: str) -> Dict[str, bool]:
    """
    Analyze README content to identify which sections are present.
    
    Args:
        readme_content: The raw README text
        
    Returns:
        Dictionary with section presence flags
    """
    content_lower = readme_content.lower()
    
    sections = {
        "has_description": len(readme_content) > 100,
        "has_installation": any(keyword in content_lower for keyword in 
            ["installation", "install", "setup", "getting started", "quick start"]),
        "has_usage": any(keyword in content_lower for keyword in 
            ["usage", "how to use", "example", "examples", "demo"]),
        "has_screenshots": any(keyword in content_lower for keyword in 
            ["screenshot", "preview", "demo", "![", ".png", ".jpg", ".gif"]),
        "has_contributing": any(keyword in content_lower for keyword in 
            ["contributing", "contribute", "contributors", "contribution"]),
        "has_license": any(keyword in content_lower for keyword in 
            ["license", "mit", "apache", "gpl"]),
        "has_badges": "![" in readme_content and "].svg" in content_lower,
        "has_table_of_contents": any(keyword in content_lower for keyword in 
            ["table of contents", "contents", "## index"])
    }
    
    return sections


def calculate_commit_message_quality(messages: List[str]) -> float:
    """
    Evaluate the quality of commit messages.
    
    Good commit messages:
    - Are descriptive (not just "update" or "fix")
    - Have reasonable length
    - Follow conventions (optional)
    
    Args:
        messages: List of commit messages
        
    Returns:
        Quality score from 0-100
    """
    if not messages:
        return 0
    
    # Bad/generic commit messages
    bad_patterns = [
        r'^update$',
        r'^fix$',
        r'^wip$',
        r'^test$',
        r'^\.+$',
        r'^-+$',
        r'^asdf',
        r'^temp',
        r'^todo',
        r'^commit$',
        r'^changes$',
        r'^stuff$',
        r'^misc$'
    ]
    
    good_count = 0
    
    for message in messages:
        message_lower = message.lower().strip()
        
        # Skip empty messages
        if not message_lower:
            continue
        
        # Check if message matches bad patterns
        is_bad = any(re.match(pattern, message_lower) for pattern in bad_patterns)
        
        # Good messages should be at least 10 characters
        is_good_length = len(message) >= 10
        
        if not is_bad and is_good_length:
            good_count += 1
    
    # Calculate percentage of good commits
    if len(messages) > 0:
        return (good_count / len(messages)) * 100
    
    return 0


def get_language_diversity_score(languages: Dict[str, int]) -> float:
    """
    Calculate a diversity score based on programming languages used.
    
    Args:
        languages: Dict of language -> bytes of code
        
    Returns:
        Diversity score from 0-100
    """
    if not languages:
        return 0
    
    num_languages = len(languages)
    
    # Score based on number of languages
    # 1 language = 20, 2 = 40, 3 = 60, 4 = 80, 5+ = 100
    base_score = min(num_languages * 20, 100)
    
    return base_score
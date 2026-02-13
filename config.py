"""
Configuration file for GitHub Portfolio Analyzer
Contains all constants, weights, and settings
"""

 
# SCORING WEIGHTS (Must sum to 100)
# These weights determine how much each category affects
# the final portfolio score
 

SCORING_WEIGHTS = {
    "documentation": 30,    # READMEs, descriptions, wikis
    "consistency": 25,      # Commit frequency, activity streaks
    "code_quality": 25,     # Structure, organization, best practices
    "impact": 20            # Stars, forks, real-world relevance
}

 
# DOCUMENTATION SCORING CRITERIA
 

README_QUALITY_CRITERIA = {
    "has_readme": 10,           # Basic README exists
    "has_description": 10,      # Project description section
    "has_installation": 15,     # Installation instructions
    "has_usage": 15,            # Usage examples
    "has_screenshots": 10,      # Visual documentation
    "has_contributing": 10,     # Contributing guidelines
    "has_license": 10,          # License information
    "good_length": 20           # Adequate length (>500 chars)
}

# Minimum README length considered "good"
MIN_README_LENGTH = 500
 
# CONSISTENCY SCORING CRITERIA
 

CONSISTENCY_CRITERIA = {
    "days_active_last_year": 40,    # Activity spread
    "longest_streak": 30,            # Consecutive days
    "recent_activity": 30            # Activity in last 30 days
}

# Ideal number of active days per year for max score
IDEAL_ACTIVE_DAYS = 200

 
# CODE QUALITY CRITERIA
 

CODE_QUALITY_CRITERIA = {
    "has_gitignore": 15,            # Proper .gitignore
    "organized_structure": 25,       # Good folder structure
    "meaningful_commits": 30,        # Descriptive commit messages
    "multiple_languages": 15,        # Diverse tech stack
    "no_large_files": 15             # No binary/large files
}

 
# IMPACT CRITERIA
 

IMPACT_CRITERIA = {
    "total_stars": 30,              # Repository stars
    "total_forks": 25,              # Repository forks
    "followers": 20,                 # Profile followers
    "pinned_repos": 15,             # Showcased repositories
    "contributions_to_others": 10    # External contributions
}

 
# GRADE BOUNDARIES
 

GRADE_BOUNDARIES = {
    "A+": 95,
    "A": 90,
    "A-": 85,
    "B+": 80,
    "B": 75,
    "B-": 70,
    "C+": 65,
    "C": 60,
    "C-": 55,
    "D": 50,
    "F": 0
}


# API SETTINGS

GITHUB_API_BASE_URL = "https://api.github.com"
MAX_REPOS_TO_ANALYZE = 30
REQUEST_TIMEOUT = 30
 
# UI SETTINGS
 

SCORE_COLORS = {
    "excellent": "#00C853",    # Green (80-100)
    "good": "#64DD17",         # Light Green (60-79)
    "average": "#FFD600",      # Yellow (40-59)
    "poor": "#FF6D00",         # Orange (20-39)
    "critical": "#FF1744"      # Red (0-19)
}
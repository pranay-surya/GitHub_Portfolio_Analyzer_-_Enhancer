"""
GitHub Data Fetcher
Handles all interactions with the GitHub API
"""

import requests
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()


class GitHubFetcher:
    """
    Fetches and processes data from the GitHub API.
    
    This class handles:
    - User profile information
    - Repository data
    - Commit history
    - README contents
    - Contribution statistics
    """
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize the GitHub API client.
        
        Args:
            token: GitHub personal access token (optional but recommended)
        """
        self.base_url = "https://api.github.com"
        self.token = token or os.getenv("GITHUB_TOKEN")
        
        # Set up headers with authentication if token provided
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Portfolio-Analyzer"
        }
        
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
    
    def _make_request(self, endpoint: str) -> Optional[Dict]:
        """
        Make a request to the GitHub API.
        
        Args:
            endpoint: API endpoint (without base URL)
            
        Returns:
            JSON response as dictionary, or None if failed
        """
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
    
    def get_user_profile(self, username: str) -> Optional[Dict]:
        """
        Fetch basic user profile information.
        
        Args:
            username: GitHub username
            
        Returns:
            User profile data including:
            - name, bio, location, company
            - followers, following
            - public repos count
            - Account creation date
        """
        data = self._make_request(f"/users/{username}")
        
        if data:
            return {
                "username": data.get("login"),
                "name": data.get("name") or data.get("login"),
                "bio": data.get("bio") or "",
                "location": data.get("location") or "",
                "company": data.get("company") or "",
                "blog": data.get("blog") or "",
                "avatar_url": data.get("avatar_url"),
                "followers": data.get("followers", 0),
                "following": data.get("following", 0),
                "public_repos": data.get("public_repos", 0),
                "created_at": data.get("created_at"),
                "updated_at": data.get("updated_at"),
                "hireable": data.get("hireable", False),
                "twitter_username": data.get("twitter_username") or ""
            }
        
        return None
    
    def get_repositories(self, username: str, max_repos: int = 30) -> List[Dict]:
        """
        Fetch user's public repositories.
        
        Args:
            username: GitHub username
            max_repos: Maximum number of repos to fetch
            
        Returns:
            List of repository data dictionaries
        """
        repos = []
        page = 1
        per_page = min(max_repos, 100)  # GitHub max is 100 per page
        
        while len(repos) < max_repos:
            data = self._make_request(
                f"/users/{username}/repos?page={page}&per_page={per_page}&sort=updated"
            )
            
            if not data or len(data) == 0:
                break
            
            for repo in data:
                # Skip forks if they haven't been modified
                if repo.get("fork") and not repo.get("pushed_at"):
                    continue
                
                repos.append({
                    "name": repo.get("name"),
                    "full_name": repo.get("full_name"),
                    "description": repo.get("description") or "",
                    "language": repo.get("language") or "Unknown",
                    "stars": repo.get("stargazers_count", 0),
                    "forks": repo.get("forks_count", 0),
                    "watchers": repo.get("watchers_count", 0),
                    "open_issues": repo.get("open_issues_count", 0),
                    "is_fork": repo.get("fork", False),
                    "created_at": repo.get("created_at"),
                    "updated_at": repo.get("updated_at"),
                    "pushed_at": repo.get("pushed_at"),
                    "homepage": repo.get("homepage") or "",
                    "size": repo.get("size", 0),
                    "default_branch": repo.get("default_branch", "main"),
                    "has_wiki": repo.get("has_wiki", False),
                    "has_pages": repo.get("has_pages", False),
                    "topics": repo.get("topics", []),
                    "license": repo.get("license", {}).get("name") if repo.get("license") else None
                })
                
                if len(repos) >= max_repos:
                    break
            
            page += 1
        
        return repos
    
    def get_readme_content(self, username: str, repo_name: str) -> Optional[str]:
        """
        Fetch the README content for a repository.
        
        Args:
            username: Repository owner
            repo_name: Repository name
            
        Returns:
            README content as string, or None if not found
        """
        data = self._make_request(f"/repos/{username}/{repo_name}/readme")
        
        if data and "content" in data:
            try:
                # README content is base64 encoded
                content = base64.b64decode(data["content"]).decode("utf-8")
                return content
            except Exception:
                return None
        
        return None
    
    def get_repository_contents(self, username: str, repo_name: str) -> List[Dict]:
        """
        Fetch the root directory contents of a repository.
        Used to check for specific files like .gitignore, LICENSE, etc.
        
        Args:
            username: Repository owner
            repo_name: Repository name
            
        Returns:
            List of file/directory information
        """
        data = self._make_request(f"/repos/{username}/{repo_name}/contents")
        
        if data and isinstance(data, list):
            return [
                {
                    "name": item.get("name"),
                    "type": item.get("type"),  # "file" or "dir"
                    "size": item.get("size", 0)
                }
                for item in data
            ]
        
        return []
    
    def get_recent_commits(self, username: str, repo_name: str, limit: int = 30) -> List[Dict]:
        """
        Fetch recent commits for a repository.
        
        Args:
            username: Repository owner
            repo_name: Repository name
            limit: Maximum number of commits to fetch
            
        Returns:
            List of commit information
        """
        data = self._make_request(
            f"/repos/{username}/{repo_name}/commits?per_page={limit}"
        )
        
        if data and isinstance(data, list):
            return [
                {
                    "sha": commit.get("sha", "")[:7],
                    "message": commit.get("commit", {}).get("message", "").split("\n")[0],
                    "date": commit.get("commit", {}).get("author", {}).get("date"),
                    "author": commit.get("commit", {}).get("author", {}).get("name")
                }
                for commit in data
            ]
        
        return []
    
    def get_contribution_stats(self, username: str) -> Dict:
        """
        Get contribution statistics for a user.
        Note: GitHub doesn't have a direct API for this, so we approximate
        using events and repository data.
        
        Args:
            username: GitHub username
            
        Returns:
            Contribution statistics
        """
        # Get recent events (last 90 days max from API)
        events = self._make_request(f"/users/{username}/events?per_page=100")
        
        if not events:
            return {
                "total_events": 0,
                "push_events": 0,
                "pr_events": 0,
                "issue_events": 0,
                "unique_days": 0,
                "recent_activity": False
            }
        
        # Count event types
        push_events = 0
        pr_events = 0
        issue_events = 0
        unique_dates = set()
        
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_activity = False
        
        for event in events:
            event_type = event.get("type", "")
            event_date = event.get("created_at", "")
            
            if event_date:
                date_only = event_date.split("T")[0]
                unique_dates.add(date_only)
                
                # Check if within last 30 days
                try:
                    event_datetime = datetime.fromisoformat(event_date.replace("Z", "+00:00"))
                    if event_datetime.replace(tzinfo=None) > thirty_days_ago:
                        recent_activity = True
                except:
                    pass
            
            if event_type == "PushEvent":
                push_events += 1
            elif event_type == "PullRequestEvent":
                pr_events += 1
            elif event_type == "IssuesEvent":
                issue_events += 1
        
        return {
            "total_events": len(events),
            "push_events": push_events,
            "pr_events": pr_events,
            "issue_events": issue_events,
            "unique_days": len(unique_dates),
            "recent_activity": recent_activity
        }
    
    def get_languages(self, username: str, repo_name: str) -> Dict[str, int]:
        """
        Get languages used in a repository.
        
        Args:
            username: Repository owner
            repo_name: Repository name
            
        Returns:
            Dict of language -> bytes of code
        """
        data = self._make_request(f"/repos/{username}/{repo_name}/languages")
        return data if data else {}
    
    def fetch_all_data(self, username: str) -> Optional[Dict]:
        """
        Fetch all data needed for portfolio analysis.
        This is the main method that orchestrates all data fetching.
        
        Args:
            username: GitHub username
            
        Returns:
            Complete data package for analysis, or None if user not found
        """
        print(f"📡 Fetching data for: {username}")
        
        # Step 1: Get user profile
        profile = self.get_user_profile(username)
        if not profile:
            return None
        
        print(f"  ✓ Profile loaded: {profile['name']}")
        
        # Step 2: Get repositories
        repos = self.get_repositories(username)
        print(f"  ✓ Found {len(repos)} repositories")
        
        # Step 3: Analyze each repository
        analyzed_repos = []
        all_languages = {}
        total_commits = []
        
        for repo in repos[:15]:  # Limit detailed analysis to top 15 repos
            # Get README
            readme = self.get_readme_content(username, repo["name"])
            
            # Get repository structure
            contents = self.get_repository_contents(username, repo["name"])
            
            # Get recent commits
            commits = self.get_recent_commits(username, repo["name"])
            total_commits.extend(commits)
            
            # Get languages
            languages = self.get_languages(username, repo["name"])
            for lang, bytes_count in languages.items():
                all_languages[lang] = all_languages.get(lang, 0) + bytes_count
            
            analyzed_repos.append({
                **repo,
                "readme_content": readme,
                "has_readme": readme is not None and len(readme) > 0,
                "readme_length": len(readme) if readme else 0,
                "contents": contents,
                "commits": commits,
                "languages": languages
            })
        
        print(f"  ✓ Analyzed {len(analyzed_repos)} repositories in detail")
        
        # Step 4: Get contribution stats
        contribution_stats = self.get_contribution_stats(username)
        print(f"  ✓ Loaded contribution statistics")
        
        # Step 5: Compile all data
        return {
            "profile": profile,
            "repositories": analyzed_repos,
            "all_repos_basic": repos,  # All repos with basic info
            "all_languages": all_languages,
            "all_commits": total_commits,
            "contribution_stats": contribution_stats,
            "fetched_at": datetime.now().isoformat()
        }
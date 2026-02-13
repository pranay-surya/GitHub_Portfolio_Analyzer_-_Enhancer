"""
Consistency Analyzer
Evaluates commit frequency, activity patterns, and streaks
"""

from typing import Dict, List, Any
from datetime import datetime, timedelta
from collections import defaultdict


class ConsistencyAnalyzer:
    """
    Analyzes the consistency of contributions over time.
    
    Scoring criteria:
    - Commit frequency
    - Activity streaks
    - Recent activity (last 30 days)
    - Long-term engagement
    """
    
    def __init__(self):
        self.score = 0
        self.details = {}
        self.issues = []
        self.strengths = []
    
    def analyze(self, data: Dict) -> Dict:
        """
        Perform consistency analysis.
        
        Args:
            data: Complete GitHub data from fetcher
            
        Returns:
            Analysis results with score and details
        """
        commits = data.get("all_commits", [])
        contribution_stats = data.get("contribution_stats", {})
        repos = data.get("repositories", [])
        profile = data.get("profile", {})
        
    
        # METRIC 1: Activity Spread (30 points)
        # How many unique days has the user been active?
      
        unique_dates = set()
        
        for commit in commits:
            if commit.get("date"):
                date_only = commit["date"].split("T")[0]
                unique_dates.add(date_only)
        
        # Add dates from contribution stats
        unique_days = max(len(unique_dates), contribution_stats.get("unique_days", 0))
        
        # Score: 0-200 days maps to 0-100%, then scaled to 30 points
        activity_spread_percentage = min(unique_days / 200, 1) * 100
        activity_spread_score = (activity_spread_percentage / 100) * 30
         
        # METRIC 2: Longest Streak (25 points)
        # Calculate the longest consecutive days streak
        
        longest_streak = self._calculate_longest_streak(list(unique_dates))
        
        # Score: 7+ days streak = 100%, scaled to 25 points
        streak_percentage = min(longest_streak / 7, 1) * 100
        streak_score = (streak_percentage / 100) * 25
  
        # METRIC 3: Recent Activity (30 points)
        # Activity in the last 30 days
         
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_commits = 0
        
        for commit in commits:
            if commit.get("date"):
                try:
                    commit_date = datetime.fromisoformat(
                        commit["date"].replace("Z", "+00:00")
                    ).replace(tzinfo=None)
                    if commit_date > thirty_days_ago:
                        recent_commits += 1
                except:
                    pass
        
        # Also check for recent repo updates
        recent_repo_updates = 0
        for repo in repos:
            if repo.get("pushed_at"):
                try:
                    push_date = datetime.fromisoformat(
                        repo["pushed_at"].replace("Z", "+00:00")
                    ).replace(tzinfo=None)
                    if push_date > thirty_days_ago:
                        recent_repo_updates += 1
                except:
                    pass
        
        # Score based on recent activity
        has_recent_activity = recent_commits > 0 or recent_repo_updates > 0
        recent_activity_level = min(recent_commits / 10, 1)  # 10+ commits = 100%
        recent_activity_score = recent_activity_level * 30
        
       
        # METRIC 4: Account Age vs Activity (15 points)
        # Long-term engagement
   
        account_created = profile.get("created_at")
        account_age_days = 0
        
        if account_created:
            try:
                created_date = datetime.fromisoformat(
                    account_created.replace("Z", "+00:00")
                ).replace(tzinfo=None)
                account_age_days = (datetime.now() - created_date).days
            except:
                pass
        
        # Calculate activity density (activity per account age)
        if account_age_days > 0:
            activity_density = unique_days / min(account_age_days, 365)
        else:
            activity_density = 0
        
        # 30% activity density over account lifetime = excellent
        engagement_percentage = min(activity_density / 0.3, 1) * 100
        engagement_score = (engagement_percentage / 100) * 15
 
  
        self.score = round(
            activity_spread_score +
            streak_score +
            recent_activity_score +
            engagement_score
        )
 
        # IDENTIFY ISSUES & STRENGTHS
     
        
        # Issues
        if not has_recent_activity:
            self.issues.append("No activity detected in the last 30 days - profile appears inactive")
        
        if longest_streak < 3:
            self.issues.append("No significant coding streaks detected - shows inconsistent activity")
        
        if unique_days < 30:
            self.issues.append(f"Only {unique_days} active days recorded - limited activity history")
        
        # Strengths
        if recent_commits >= 10:
            self.strengths.append(f"Very active recently: {recent_commits} commits in last 30 days")
        elif has_recent_activity:
            self.strengths.append("Shows recent activity on the profile")
        
        if longest_streak >= 7:
            self.strengths.append(f"Impressive {longest_streak}-day coding streak demonstrates dedication")
        
        if unique_days >= 100:
            self.strengths.append(f"Strong activity history with {unique_days} active days")
        
        # Compile details
        self.details = {
            "unique_active_days": unique_days,
            "longest_streak": longest_streak,
            "recent_commits": recent_commits,
            "recent_repo_updates": recent_repo_updates,
            "account_age_days": account_age_days,
            "has_recent_activity": has_recent_activity,
            "component_scores": {
                "activity_spread": round(activity_spread_score, 1),
                "streak": round(streak_score, 1),
                "recent_activity": round(recent_activity_score, 1),
                "engagement": round(engagement_score, 1)
            }
        }
        
        return {
            "score": self.score,
            "details": self.details,
            "issues": self.issues,
            "strengths": self.strengths
        }
    
    def _calculate_longest_streak(self, dates: List[str]) -> int:
        """
        Calculate the longest consecutive days streak.
        
        Args:
            dates: List of date strings (YYYY-MM-DD format)
            
        Returns:
            Longest streak in days
        """
        if not dates:
            return 0
        
        # Convert to datetime objects and sort
        date_objects = []
        for date_str in dates:
            try:
                date_objects.append(datetime.strptime(date_str, "%Y-%m-%d"))
            except:
                pass
        
        if not date_objects:
            return 0
        
        date_objects.sort()
        
        # Find longest streak
        longest_streak = 1
        current_streak = 1
        
        for i in range(1, len(date_objects)):
            diff = (date_objects[i] - date_objects[i-1]).days
            
            if diff == 1:  # Consecutive day
                current_streak += 1
                longest_streak = max(longest_streak, current_streak)
            elif diff > 1:  # Gap in dates
                current_streak = 1
            # If diff == 0, same day, don't change streak
        
        return longest_streak
"""
Impact Analyzer
Evaluates the real-world impact and visibility of the portfolio
"""

from typing import Dict, List, Any


class ImpactAnalyzer:
    """
    Analyzes the impact and reach of a GitHub portfolio.
    
    Scoring criteria:
    - Stars and forks received
    - Followers count
    - Pinned/Featured repositories
    - External contributions
    - Project completeness signals
    """
    
    def __init__(self):
        self.score = 0
        self.details = {}
        self.issues = []
        self.strengths = []
    
    def analyze(self, data: Dict) -> Dict:
        """
        Perform impact analysis.
        
        Args:
            data: Complete GitHub data from fetcher
            
        Returns:
            Analysis results with score and details
        """
        repos = data.get("repositories", [])
        all_repos = data.get("all_repos_basic", repos)
        profile = data.get("profile", {})
        
        if not repos:
            return {
                "score": 0,
                "details": {"error": "No repositories found"},
                "issues": ["No repositories to analyze"],
                "strengths": []
            }
        
    
        # METRIC 1: Repository Stars (25 points)
        # Total stars across all repositories
         
        total_stars = sum(r.get("stars", 0) for r in all_repos)
        
        # Scoring: 0 stars = 0, 10 stars = 50%, 50+ stars = 100%
        if total_stars >= 50:
            stars_percentage = 100
        elif total_stars >= 10:
            stars_percentage = 50 + ((total_stars - 10) / 40) * 50
        else:
            stars_percentage = (total_stars / 10) * 50
        
        stars_score = (stars_percentage / 100) * 25
    
        # METRIC 2: Repository Forks (20 points)
        # Total forks indicate others find code useful
        
        total_forks = sum(r.get("forks", 0) for r in all_repos)
        
        # Scoring: 0 forks = 0, 5 forks = 50%, 20+ forks = 100%
        if total_forks >= 20:
            forks_percentage = 100
        elif total_forks >= 5:
            forks_percentage = 50 + ((total_forks - 5) / 15) * 50
        else:
            forks_percentage = (total_forks / 5) * 50
        
        forks_score = (forks_percentage / 100) * 20
        
        
        # METRIC 3: Profile Followers (15 points)
 
        followers = profile.get("followers", 0)
        
        # Scoring: 0 = 0%, 10 = 50%, 50+ = 100%
        if followers >= 50:
            followers_percentage = 100
        elif followers >= 10:
            followers_percentage = 50 + ((followers - 10) / 40) * 50
        else:
            followers_percentage = (followers / 10) * 50
        
        followers_score = (followers_percentage / 100) * 15
        
   
        # METRIC 4: Project Completeness (25 points)
        # Projects with homepage, description, topics = more complete
       
        complete_projects = 0
        
        for repo in repos:
            completeness = 0
            
            # Has description
            if repo.get("description"):
                completeness += 1
            
            # Has homepage/demo link
            if repo.get("homepage"):
                completeness += 1
            
            # Has topics
            if len(repo.get("topics", [])) > 0:
                completeness += 1
            
            # Has README
            if repo.get("has_readme"):
                completeness += 1
            
            # Consider complete if 3+ criteria met
            if completeness >= 3:
                complete_projects += 1
        
        completeness_percentage = (complete_projects / len(repos)) * 100 if repos else 0
        completeness_score = (completeness_percentage / 100) * 25
   
        # METRIC 5: Profile Completeness (15 points)
        # Bio, location, hireable status, etc.
   
        profile_completeness = 0
        
        if profile.get("bio"):
            profile_completeness += 25
        if profile.get("location"):
            profile_completeness += 15
        if profile.get("blog"):
            profile_completeness += 20
        if profile.get("company"):
            profile_completeness += 15
        if profile.get("hireable"):
            profile_completeness += 15
        if profile.get("twitter_username"):
            profile_completeness += 10
        
        profile_score = (profile_completeness / 100) * 15
        
      
        # CALCULATE FINAL SCORE
        
        self.score = round(
            stars_score +
            forks_score +
            followers_score +
            completeness_score +
            profile_score
        )
        
    
        # IDENTIFY ISSUES & STRENGTHS
       
        
        # Identify best repos
        best_repos = sorted(
            all_repos,
            key=lambda x: x.get("stars", 0) + x.get("forks", 0),
            reverse=True
        )[:3]
        
        # Issues
        if total_stars == 0:
            self.issues.append("No stars on any repository - consider promoting your best projects")
        
        if followers < 5:
            self.issues.append(f"Low follower count ({followers}) - engage with the community more")
        
        if not profile.get("bio"):
            self.issues.append("Profile is missing a bio - add a brief professional description")
        
        if completeness_percentage < 50:
            self.issues.append("Many projects appear incomplete - add descriptions, topics, and demo links")
        
        if not profile.get("hireable") and not profile.get("company"):
            self.issues.append("Set 'Available for hire' flag to signal recruiters you're open to opportunities")
        
        # Strengths
        if total_stars >= 10:
            self.strengths.append(f"Portfolio has received {total_stars} total stars - shows community recognition")
        
        if total_forks >= 5:
            self.strengths.append(f"{total_forks} forks indicate others find your code useful")
        
        if followers >= 20:
            self.strengths.append(f"Strong following of {followers} people")
        
        if completeness_percentage >= 70:
            self.strengths.append("Most projects are well-documented with descriptions and topics")
        
        if profile.get("bio") and profile.get("blog"):
            self.strengths.append("Complete profile with bio and portfolio link")
        
        # Compile details
        self.details = {
            "total_stars": total_stars,
            "total_forks": total_forks,
            "followers": followers,
            "following": profile.get("following", 0),
            "complete_projects": complete_projects,
            "total_repos": len(all_repos),
            "profile_completeness": profile_completeness,
            "best_repos": [
                {"name": r["name"], "stars": r.get("stars", 0), "forks": r.get("forks", 0)}
                for r in best_repos
            ],
            "component_scores": {
                "stars": round(stars_score, 1),
                "forks": round(forks_score, 1),
                "followers": round(followers_score, 1),
                "project_completeness": round(completeness_score, 1),
                "profile_completeness": round(profile_score, 1)
            }
        }
        
        return {
            "score": self.score,
            "details": self.details,
            "issues": self.issues,
            "strengths": self.strengths
        }
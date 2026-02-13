"""
Documentation Analyzer
Evaluates the quality of documentation across repositories
"""

from typing import Dict, List, Any
from utils.helpers import extract_readme_sections


class DocumentationAnalyzer:
    """
    Analyzes documentation quality across all repositories.
    
    Scoring criteria:
    - README presence and quality
    - Project descriptions
    - Code comments (inferred from README detail)
    - Additional documentation (wiki, contributing guide)
    """
    
    def __init__(self):
        self.score = 0
        self.details = {}
        self.issues = []
        self.strengths = []
    
    def analyze(self, data: Dict) -> Dict:
        """
        Perform documentation analysis.
        
        Args:
            data: Complete GitHub data from fetcher
            
        Returns:
            Analysis results with score and details
        """
        repos = data.get("repositories", [])
        
        if not repos:
            return {
                "score": 0,
                "details": {"error": "No repositories found"},
                "issues": ["No repositories to analyze"],
                "strengths": []
            }
        
  
        # METRIC 1: README Coverage (25 points)
     
        repos_with_readme = sum(1 for r in repos if r.get("has_readme"))
        readme_percentage = (repos_with_readme / len(repos)) * 100
        readme_coverage_score = min(readme_percentage, 100) * 0.25
         
        # METRIC 2: README Quality (40 points)
        
        quality_scores = []
        
        for repo in repos:
            if repo.get("readme_content"):
                sections = extract_readme_sections(repo["readme_content"])
                
                # Calculate quality score for this README
                quality = 0
                quality += 10 if sections.get("has_description") else 0
                quality += 20 if sections.get("has_installation") else 0
                quality += 20 if sections.get("has_usage") else 0
                quality += 15 if sections.get("has_screenshots") else 0
                quality += 10 if sections.get("has_contributing") else 0
                quality += 10 if sections.get("has_license") else 0
                quality += 10 if sections.get("has_badges") else 0
                quality += 5 if sections.get("has_table_of_contents") else 0
                
                quality_scores.append(quality)
        
        avg_readme_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        readme_quality_score = (avg_readme_quality / 100) * 40
        
         
        # METRIC 3: Repository Descriptions (20 points)
 
        repos_with_description = sum(1 for r in repos if r.get("description"))
        description_percentage = (repos_with_description / len(repos)) * 100
        description_score = (description_percentage / 100) * 20
        
  
        # METRIC 4: Topics/Tags Usage (15 points)
       
        repos_with_topics = sum(1 for r in repos if len(r.get("topics", [])) > 0)
        topics_percentage = (repos_with_topics / len(repos)) * 100
        topics_score = (topics_percentage / 100) * 15
        
      
        # CALCULATE FINAL SCORE
 
        self.score = round(
            readme_coverage_score +
            readme_quality_score +
            description_score +
            topics_score
        )
         
        # IDENTIFY ISSUES & STRENGTHS
        
        
        # Issues
        if readme_percentage < 50:
            self.issues.append(f"Only {repos_with_readme}/{len(repos)} repositories have READMEs")
        
        if avg_readme_quality < 50:
            self.issues.append("README files lack important sections (installation, usage, examples)")
        
        if description_percentage < 70:
            self.issues.append(f"{len(repos) - repos_with_description} repositories missing descriptions")
        
        if topics_percentage < 30:
            self.issues.append("Most repositories don't use topic tags for discoverability")
        
        # Strengths
        if readme_percentage >= 80:
            self.strengths.append(f"Excellent README coverage: {repos_with_readme}/{len(repos)} repos")
        
        if avg_readme_quality >= 70:
            self.strengths.append("READMEs include detailed documentation with multiple sections")
        
        if description_percentage >= 90:
            self.strengths.append("All repositories have clear descriptions")
        
        # Compile details
        self.details = {
            "readme_coverage": round(readme_percentage, 1),
            "readme_quality_avg": round(avg_readme_quality, 1),
            "description_coverage": round(description_percentage, 1),
            "topics_usage": round(topics_percentage, 1),
            "repos_analyzed": len(repos),
            "repos_with_readme": repos_with_readme,
            "component_scores": {
                "readme_coverage": round(readme_coverage_score, 1),
                "readme_quality": round(readme_quality_score, 1),
                "descriptions": round(description_score, 1),
                "topics": round(topics_score, 1)
            }
        }
        
        return {
            "score": self.score,
            "details": self.details,
            "issues": self.issues,
            "strengths": self.strengths
        }
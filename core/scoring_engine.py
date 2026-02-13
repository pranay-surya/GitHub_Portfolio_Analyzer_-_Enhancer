"""
Scoring Engine
Combines all analyzer scores into a final portfolio score
"""

from typing import Dict, List, Any
from config import SCORING_WEIGHTS
from .analyzers import (
    DocumentationAnalyzer,
    ConsistencyAnalyzer,
    CodeQualityAnalyzer,
    ImpactAnalyzer
)
from utils.helpers import get_score_grade, get_score_color


class ScoringEngine:
    """
    The main scoring engine that orchestrates all analyzers
    and calculates the final portfolio score.
    
    ┌─────────────────────────────────────────────────────────────┐
    │                    SCORING ALGORITHM                        │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │  Final Score = Σ (Category Score × Category Weight)        │
    │                                                             │
    │  Categories:                                                │
    │  ├── Documentation (30%) ─── README quality, descriptions  │
    │  ├── Consistency (25%) ──── Commit frequency, streaks      │
    │  ├── Code Quality (25%) ─── Structure, best practices      │
    │  └── Impact (20%) ───────── Stars, forks, followers        │
    │                                                             │
    │  Each category is scored 0-100, then weighted              │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘
    """
    
    def __init__(self):
        # Initialize all analyzers
        self.documentation_analyzer = DocumentationAnalyzer()
        self.consistency_analyzer = ConsistencyAnalyzer()
        self.code_quality_analyzer = CodeQualityAnalyzer()
        self.impact_analyzer = ImpactAnalyzer()
        
        # Store results
        self.results = {}
        self.final_score = 0
        self.grade = "F"
    
    def calculate_score(self, github_data: Dict) -> Dict:
        """
        Calculate the complete portfolio score.
        
        This is the main method that:
        1. Runs all analyzers
        2. Applies weights to each category
        3. Calculates the final weighted score
        4. Determines the letter grade
        
        Args:
            github_data: Complete data from GitHubFetcher
            
        Returns:
            Complete scoring results with breakdown
        """
        
        print("\n📊 Calculating Portfolio Score...")
        print("=" * 50)
        
        # ═══════════════════════════════════════════════════════════
        # STEP 1: Run Individual Analyzers
        # ═══════════════════════════════════════════════════════════
        
        # Documentation Analysis (30% weight)
        print("\n📝 Analyzing Documentation...")
        doc_results = self.documentation_analyzer.analyze(github_data)
        doc_score = doc_results["score"]
        doc_weighted = (doc_score / 100) * SCORING_WEIGHTS["documentation"]
        print(f"   Raw Score: {doc_score}/100")
        print(f"   Weighted Score: {doc_weighted:.1f}/{SCORING_WEIGHTS['documentation']}")
        
        # Consistency Analysis (25% weight)
        print("\n📅 Analyzing Consistency...")
        consistency_results = self.consistency_analyzer.analyze(github_data)
        consistency_score = consistency_results["score"]
        consistency_weighted = (consistency_score / 100) * SCORING_WEIGHTS["consistency"]
        print(f"   Raw Score: {consistency_score}/100")
        print(f"   Weighted Score: {consistency_weighted:.1f}/{SCORING_WEIGHTS['consistency']}")
        
        # Code Quality Analysis (25% weight)
        print("\n💻 Analyzing Code Quality...")
        quality_results = self.code_quality_analyzer.analyze(github_data)
        quality_score = quality_results["score"]
        quality_weighted = (quality_score / 100) * SCORING_WEIGHTS["code_quality"]
        print(f"   Raw Score: {quality_score}/100")
        print(f"   Weighted Score: {quality_weighted:.1f}/{SCORING_WEIGHTS['code_quality']}")
        
        # Impact Analysis (20% weight)
        print("\n🌟 Analyzing Impact...")
        impact_results = self.impact_analyzer.analyze(github_data)
        impact_score = impact_results["score"]
        impact_weighted = (impact_score / 100) * SCORING_WEIGHTS["impact"]
        print(f"   Raw Score: {impact_score}/100")
        print(f"   Weighted Score: {impact_weighted:.1f}/{SCORING_WEIGHTS['impact']}")
        
        # ═══════════════════════════════════════════════════════════
        # STEP 2: Calculate Final Weighted Score
        # ═══════════════════════════════════════════════════════════
        
        self.final_score = round(
            doc_weighted +
            consistency_weighted +
            quality_weighted +
            impact_weighted
        )
        
        # Ensure score is within bounds
        self.final_score = max(0, min(100, self.final_score))
        
        # ═══════════════════════════════════════════════════════════
        # STEP 3: Determine Grade
        # ═══════════════════════════════════════════════════════════
        
        self.grade = get_score_grade(self.final_score)
        
        print("\n" + "=" * 50)
        print(f"🎯 FINAL PORTFOLIO SCORE: {self.final_score}/100 ({self.grade})")
        print("=" * 50)
        
        # ═══════════════════════════════════════════════════════════
        # STEP 4: Compile All Results
        # ═══════════════════════════════════════════════════════════
        
        self.results = {
            "final_score": self.final_score,
            "grade": self.grade,
            "score_color": get_score_color(self.final_score),
            
            "category_scores": {
                "documentation": {
                    "raw_score": doc_score,
                    "weighted_score": round(doc_weighted, 1),
                    "weight": SCORING_WEIGHTS["documentation"],
                    "details": doc_results["details"],
                    "issues": doc_results["issues"],
                    "strengths": doc_results["strengths"]
                },
                "consistency": {
                    "raw_score": consistency_score,
                    "weighted_score": round(consistency_weighted, 1),
                    "weight": SCORING_WEIGHTS["consistency"],
                    "details": consistency_results["details"],
                    "issues": consistency_results["issues"],
                    "strengths": consistency_results["strengths"]
                },
                "code_quality": {
                    "raw_score": quality_score,
                    "weighted_score": round(quality_weighted, 1),
                    "weight": SCORING_WEIGHTS["code_quality"],
                    "details": quality_results["details"],
                    "issues": quality_results["issues"],
                    "strengths": quality_results["strengths"]
                },
                "impact": {
                    "raw_score": impact_score,
                    "weighted_score": round(impact_weighted, 1),
                    "weight": SCORING_WEIGHTS["impact"],
                    "details": impact_results["details"],
                    "issues": impact_results["issues"],
                    "strengths": impact_results["strengths"]
                }
            },
            
            # Summary statistics
            "summary": {
                "total_repos": len(github_data.get("repositories", [])),
                "total_stars": impact_results["details"].get("total_stars", 0),
                "total_forks": impact_results["details"].get("total_forks", 0),
                "top_languages": quality_results["details"].get("top_languages", []),
                "profile_name": github_data.get("profile", {}).get("name", ""),
                "profile_username": github_data.get("profile", {}).get("username", "")
            }
        }
        
        return self.results
    
    def get_score_breakdown_chart_data(self) -> Dict:
        """
        Get data formatted for visualization charts.
        
        Returns:
            Data suitable for Plotly charts
        """
        if not self.results:
            return {}
        
        categories = self.results["category_scores"]
        
        return {
            "labels": ["Documentation", "Consistency", "Code Quality", "Impact"],
            "raw_scores": [
                categories["documentation"]["raw_score"],
                categories["consistency"]["raw_score"],
                categories["code_quality"]["raw_score"],
                categories["impact"]["raw_score"]
            ],
            "weighted_scores": [
                categories["documentation"]["weighted_score"],
                categories["consistency"]["weighted_score"],
                categories["code_quality"]["weighted_score"],
                categories["impact"]["weighted_score"]
            ],
            "weights": [
                categories["documentation"]["weight"],
                categories["consistency"]["weight"],
                categories["code_quality"]["weight"],
                categories["impact"]["weight"]
            ]
        }
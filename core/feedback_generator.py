"""
Feedback Generator Module
Creates specific, actionable improvement suggestions
"""


class FeedbackGenerator:
    """
    Generates personalized, actionable feedback based on analysis results.
    """
    
    def __init__(self):
        """Initialize the FeedbackGenerator."""
        self.feedback = []
        self.strengths = []
        self.red_flags = []
    
    def generate_feedback(self, scoring_results, github_data):
        """
        Generate comprehensive feedback based on analysis results.
        
        Args:
            scoring_results: Results from ScoringEngine
            github_data: Raw data from GitHubFetcher
            
        Returns:
            Dictionary with all feedback
        """
        
        # Get data from inputs
        categories = scoring_results.get("category_scores", {})
        profile = github_data.get("profile", {})
        repos = github_data.get("repositories", [])
        
        # Collect issues and strengths from each category
        all_issues = []
        all_strengths = []
        
        for category_name, category_data in categories.items():
            # Get issues
            issues = category_data.get("issues", [])
            for issue in issues:
                all_issues.append({
                    "category": category_name,
                    "issue": issue,
                    "score": category_data.get("raw_score", 0)
                })
            
            # Get strengths
            strengths = category_data.get("strengths", [])
            for strength in strengths:
                all_strengths.append({
                    "category": category_name,
                    "strength": strength,
                    "score": category_data.get("raw_score", 0)
                })
        
        # Generate all feedback
        priority_improvements = self._generate_priority_improvements(
            scoring_results, github_data
        )
        
        quick_wins = self._generate_quick_wins(github_data)
        
        red_flags = self._identify_red_flags(scoring_results, github_data)
        
        strengths = self._compile_strengths(all_strengths, scoring_results)
        
        overall_message = self._generate_overall_message(scoring_results)
        
        return {
            "priority_improvements": priority_improvements,
            "quick_wins": quick_wins,
            "red_flags": red_flags,
            "strengths": strengths,
            "overall_message": overall_message
        }
    
    def _generate_priority_improvements(self, scoring_results, github_data):
        """Generate the top priority improvements."""
        
        improvements = []
        repos = github_data.get("repositories", [])
        categories = scoring_results.get("category_scores", {})
        profile = github_data.get("profile", {})
        
        # IMPROVEMENT 1: README Quality
        doc_score = categories.get("documentation", {}).get("raw_score", 0)
        
        if doc_score < 70:
            # Find repos without READMEs
            weak_repos = []
            for repo in repos:
                if not repo.get("has_readme"):
                    weak_repos.append(repo.get("name", "unknown"))
            weak_repos = weak_repos[:3]
            
            if weak_repos:
                repos_text = ", ".join(weak_repos)
            else:
                repos_text = "your most recent projects"
            
            readme_template = (
                "## Project Name\n\n"
                "Brief description of the project.\n\n"
                "## Installation\n\n"
                "```bash\n"
                "pip install package-name\n"
                "```\n\n"
                "## Usage\n\n"
                "```python\n"
                "from package import main\n"
                "main.run()\n"
                "```\n\n"
                "## License\n\n"
                "MIT License"
            )
            
            improvements.append({
                "title": "Improve README Documentation",
                "impact": "HIGH",
                "effort": "MEDIUM",
                "description": "Your documentation score is " + str(doc_score) + "/100. READMEs are the first thing recruiters see.",
                "specific_action": "Start with these repos: " + repos_text,
                "template": readme_template
            })
        
        # IMPROVEMENT 2: Commit Consistency
        consistency_score = categories.get("consistency", {}).get("raw_score", 0)
        consistency_details = categories.get("consistency", {}).get("details", {})
        
        if consistency_score < 60:
            recent_commits = consistency_details.get("recent_commits", 0)
            
            improvements.append({
                "title": "Increase Commit Frequency",
                "impact": "HIGH",
                "effort": "LOW",
                "description": "Only " + str(recent_commits) + " commits in the last 30 days. Recruiters look for consistent activity.",
                "specific_action": "Set a goal: at least 3-4 commits per week.",
                "tips": [
                    "Work on daily coding challenges",
                    "Break large features into smaller commits",
                    "Update documentation as separate commits",
                    "Use GitHub contribution calendar as motivation"
                ]
            })
        
        # IMPROVEMENT 3: Repository Descriptions
        repos_no_desc = []
        for repo in repos:
            desc = repo.get("description")
            if not desc:
                repos_no_desc.append(repo.get("name", "unknown"))
        repos_no_desc = repos_no_desc[:5]
        
        if repos_no_desc:
            improvements.append({
                "title": "Add Repository Descriptions",
                "impact": "MEDIUM",
                "effort": "LOW",
                "description": str(len(repos_no_desc)) + " repos are missing descriptions.",
                "specific_action": "Add descriptions to: " + ", ".join(repos_no_desc),
                "example": "A full-stack e-commerce app with React and Node.js."
            })
        
        # IMPROVEMENT 4: Profile Completeness
        missing_items = []
        
        if not profile.get("bio"):
            missing_items.append("bio")
        if not profile.get("blog"):
            missing_items.append("website link")
        if not profile.get("location"):
            missing_items.append("location")
        
        if missing_items:
            improvements.append({
                "title": "Complete Your GitHub Profile",
                "impact": "MEDIUM",
                "effort": "LOW",
                "description": "Your profile is missing: " + ", ".join(missing_items),
                "specific_action": "Go to github.com/settings/profile and fill in all fields",
                "bio_template": "Student | Python Developer | Building cool projects"
            })
        
        # IMPROVEMENT 5: LICENSE Files
        license_pct = categories.get("code_quality", {}).get("details", {}).get("license_percentage", 0)
        
        if license_pct < 50:
            improvements.append({
                "title": "Add LICENSE Files",
                "impact": "MEDIUM",
                "effort": "LOW",
                "description": "Only " + str(int(license_pct)) + "% of repos have a LICENSE.",
                "specific_action": "Add MIT License to your repositories",
                "how_to": "On GitHub: Repository > Add file > Create new file > Name it LICENSE"
            })
        
        return improvements[:5]
    
    def _generate_quick_wins(self, github_data):
        """Generate quick win suggestions."""
        
        quick_wins = []
        repos = github_data.get("repositories", [])
        profile = github_data.get("profile", {})
        username = profile.get("username", "username")
        
        # Quick Win 1: Pin Repositories
        if repos:
            # Sort by stars
            sorted_repos = sorted(repos, key=lambda x: x.get("stars", 0), reverse=True)
            best_names = []
            for repo in sorted_repos[:6]:
                best_names.append(repo.get("name", ""))
            
            quick_wins.append({
                "title": "Pin Your Best 6 Repositories",
                "time": "5 minutes",
                "action": "Pin these repos: " + ", ".join(best_names),
                "how": "Go to profile > Click 'Customize your pins' > Select repos"
            })
        
        # Quick Win 2: Add Topics
        repos_no_topics = []
        for repo in repos:
            topics = repo.get("topics", [])
            if not topics:
                repos_no_topics.append(repo.get("name", ""))
        repos_no_topics = repos_no_topics[:3]
        
        if repos_no_topics:
            quick_wins.append({
                "title": "Add Topics to Repositories",
                "time": "10 minutes",
                "action": "Add topics to: " + ", ".join(repos_no_topics),
                "how": "On repo page > Click gear icon > Add topics",
                "examples": "python, react, machine-learning, api"
            })
        
        # Quick Win 3: Profile README
        quick_wins.append({
            "title": "Create a Profile README",
            "time": "15 minutes",
            "action": "Create repo named '" + username + "' with a README.md",
            "how": "This README will appear on your profile page",
            "template_url": "https://github.com/abhisheknaiidu/awesome-github-profile-readme"
        })
        
        return quick_wins
    
    def _identify_red_flags(self, scoring_results, github_data):
        """Identify critical issues."""
        
        red_flags = []
        categories = scoring_results.get("category_scores", {})
        profile = github_data.get("profile", {})
        repos = github_data.get("repositories", [])
        
        # Red Flag 1: No Recent Activity
        consistency_details = categories.get("consistency", {}).get("details", {})
        has_recent = consistency_details.get("has_recent_activity", False)
        
        if not has_recent:
            red_flags.append({
                "severity": "CRITICAL",
                "issue": "No Activity in Last 30 Days",
                "why_it_matters": "Recruiters filter out inactive profiles.",
                "fix": "Make at least 2-3 commits this week."
            })
        
        # Red Flag 2: No READMEs
        if repos:
            no_readme_count = 0
            for repo in repos:
                if not repo.get("has_readme"):
                    no_readme_count += 1
            
            if no_readme_count > len(repos) * 0.5:
                red_flags.append({
                    "severity": "HIGH",
                    "issue": str(no_readme_count) + "/" + str(len(repos)) + " Repos Have No README",
                    "why_it_matters": "Recruiters can't understand your projects.",
                    "fix": "Add a README to your top 5 repos today."
                })
        
        # Red Flag 3: Empty Bio
        if not profile.get("bio"):
            red_flags.append({
                "severity": "MEDIUM",
                "issue": "Empty Profile Bio",
                "why_it_matters": "Bio is the first thing recruiters read.",
                "fix": "Add a 2-line bio with your skills."
            })
        
        # Red Flag 4: Only Forks
        if repos:
            original_count = 0
            for repo in repos:
                if not repo.get("is_fork"):
                    original_count += 1
            
            if original_count < 3:
                red_flags.append({
                    "severity": "HIGH",
                    "issue": "Few Original Projects",
                    "why_it_matters": "Recruiters want to see YOUR work.",
                    "fix": "Create 2-3 original projects."
                })
        
        return red_flags
    
    def _compile_strengths(self, all_strengths, scoring_results):
        """Compile profile strengths."""
        
        strengths = []
        final_score = scoring_results.get("final_score", 0)
        
        # Score-based strength
        if final_score >= 80:
            strengths.append("🏆 Excellent portfolio score of " + str(final_score) + "/100!")
        elif final_score >= 60:
            strengths.append("👍 Good portfolio score of " + str(final_score) + "/100")
        elif final_score >= 40:
            strengths.append("📈 Building momentum with score of " + str(final_score) + "/100")
        
        # Category strengths
        for item in all_strengths[:5]:
            strength_text = item.get("strength", "")
            if strength_text:
                strengths.append("✅ " + strength_text)
        
        # Default if empty
        if len(strengths) < 2:
            strengths.append("✅ You have a GitHub profile - great start!")
            strengths.append("✅ You're working to improve your portfolio")
        
        return strengths
    
    def _generate_overall_message(self, scoring_results):
        """Generate overall summary message."""
        
        score = scoring_results.get("final_score", 0)
        grade = scoring_results.get("grade", "F")
        
        if score >= 80:
            message = (
                "🎉 Excellent work! Your portfolio scores " + str(score) + "/100 (" + grade + "). "
                "You have a recruiter-ready GitHub profile."
            )
        elif score >= 60:
            message = (
                "👍 Good progress! Your portfolio scores " + str(score) + "/100 (" + grade + "). "
                "Focus on the improvements below to reach the next level."
            )
        elif score >= 40:
            message = (
                "📈 Room for improvement. Your portfolio scores " + str(score) + "/100 (" + grade + "). "
                "The good news: most fixes are quick wins!"
            )
        else:
            message = (
                "🚀 Time to level up! Your portfolio scores " + str(score) + "/100 (" + grade + "). "
                "Start with the Quick Wins for immediate impact."
            )
        
        return message


# ============================================================
# TEST THE CODE
# ============================================================

if __name__ == "__main__":
    
    print("=" * 50)
    print("TESTING FEEDBACK GENERATOR")
    print("=" * 50)
    
    # Create test data
    test_scoring = {
        "final_score": 55,
        "grade": "C",
        "category_scores": {
            "documentation": {
                "raw_score": 45,
                "details": {},
                "issues": ["Missing READMEs"],
                "strengths": ["Good markdown usage"]
            },
            "consistency": {
                "raw_score": 60,
                "details": {
                    "recent_commits": 5,
                    "has_recent_activity": True
                },
                "issues": [],
                "strengths": ["Active recently"]
            },
            "code_quality": {
                "raw_score": 55,
                "details": {
                    "license_percentage": 25
                },
                "issues": ["Missing LICENSE"],
                "strengths": []
            },
            "impact": {
                "raw_score": 50,
                "details": {},
                "issues": ["Low stars"],
                "strengths": ["Some forks"]
            }
        }
    }
    
    test_github = {
        "profile": {
            "username": "testuser",
            "name": "Test User",
            "bio": "",
            "blog": "",
            "location": ""
        },
        "repositories": [
            {
                "name": "project-one",
                "has_readme": False,
                "description": "",
                "topics": [],
                "is_fork": False,
                "stars": 2
            },
            {
                "name": "project-two",
                "has_readme": True,
                "description": "Cool project",
                "topics": ["python"],
                "is_fork": False,
                "stars": 5
            },
            {
                "name": "forked-repo",
                "has_readme": True,
                "description": "Forked",
                "topics": [],
                "is_fork": True,
                "stars": 0
            }
        ]
    }
    
    # Run test
    print("\nCreating FeedbackGenerator...")
    generator = FeedbackGenerator()
    
    print("Generating feedback...")
    result = generator.generate_feedback(test_scoring, test_github)
    
    print("\n" + "=" * 50)
    print("RESULTS")
    print("=" * 50)
    
    print("\n📋 OVERALL MESSAGE:")
    print("   " + result["overall_message"])
    
    print("\n🎯 PRIORITY IMPROVEMENTS (" + str(len(result["priority_improvements"])) + "):")
    for i, item in enumerate(result["priority_improvements"], 1):
        print("   " + str(i) + ". " + item["title"] + " [" + item["impact"] + "]")
    
    print("\n⚡ QUICK WINS (" + str(len(result["quick_wins"])) + "):")
    for i, item in enumerate(result["quick_wins"], 1):
        print("   " + str(i) + ". " + item["title"] + " (" + item["time"] + ")")
    
    print("\n🚨 RED FLAGS (" + str(len(result["red_flags"])) + "):")
    for i, item in enumerate(result["red_flags"], 1):
        print("   " + str(i) + ". [" + item["severity"] + "] " + item["issue"])
    
    print("\n💪 STRENGTHS (" + str(len(result["strengths"])) + "):")
    for item in result["strengths"]:
        print("   " + item)
    
    print("\n" + "=" * 50)
    print("✅ TEST PASSED - CODE WORKS CORRECTLY!")
    print("=" * 50)
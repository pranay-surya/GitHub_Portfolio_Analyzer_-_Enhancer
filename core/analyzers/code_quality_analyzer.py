"""Code Quality Analyzer"""


class CodeQualityAnalyzer:
    """Analyzes code quality indicators."""
    
    def __init__(self):
        self.score = 0
        self.details = {}
        self.issues = []
        self.strengths = []
    
    def analyze(self, data):
        """Perform code quality analysis."""
        repos = data.get("repositories", [])
        all_languages = data.get("all_languages", {})
        all_commits = data.get("all_commits", [])
        
        if not repos:
            return {
                "score": 0,
                "details": {},
                "issues": ["No repositories found"],
                "strengths": []
            }
        
        # Essential files
        repos_with_gitignore = 0
        repos_with_license = 0
        repos_with_structure = 0
        
        for repo in repos:
            contents = repo.get("contents", [])
            file_names = [c["name"].lower() for c in contents if c.get("type") == "file"]
            dir_names = [c["name"].lower() for c in contents if c.get("type") == "dir"]
            
            if ".gitignore" in file_names:
                repos_with_gitignore += 1
            
            if any(name.startswith("license") for name in file_names):
                repos_with_license += 1
            
            if any(d in dir_names for d in ["src", "lib", "app", "components"]):
                repos_with_structure += 1
        
        gitignore_pct = (repos_with_gitignore / len(repos)) * 100
        license_pct = (repos_with_license / len(repos)) * 100
        structure_pct = (repos_with_structure / len(repos)) * 100
        
        essential_score = (gitignore_pct / 100) * 15 + (license_pct / 100) * 10
        structure_score = (structure_pct / 100) * 25
        
        # Commit quality
        messages = [c.get("message", "") for c in all_commits if c.get("message")]
        commit_quality = self._analyze_commits(messages)
        commit_score = (commit_quality / 100) * 30
        
        # Language diversity
        num_languages = len(all_languages)
        diversity_score = min(num_languages * 4, 20)
        
        # Final score
        self.score = round(essential_score + structure_score + commit_score + diversity_score)
        
        # Sort languages
        sorted_langs = sorted(all_languages.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Issues
        if gitignore_pct < 50:
            self.issues.append(f"Only {repos_with_gitignore}/{len(repos)} repos have .gitignore")
        if license_pct < 30:
            self.issues.append("Most repos missing LICENSE files")
        if commit_quality < 50:
            self.issues.append("Commit messages need improvement")
        
        # Strengths
        if gitignore_pct >= 80:
            self.strengths.append("Good .gitignore usage")
        if license_pct >= 70:
            self.strengths.append("Good LICENSE coverage")
        if num_languages >= 4:
            self.strengths.append(f"Diverse tech stack: {num_languages} languages")
        
        self.details = {
            "repos_with_gitignore": repos_with_gitignore,
            "repos_with_license": repos_with_license,
            "gitignore_percentage": round(gitignore_pct, 1),
            "license_percentage": round(license_pct, 1),
            "structure_percentage": round(structure_pct, 1),
            "commit_message_quality": round(commit_quality, 1),
            "total_languages": num_languages,
            "top_languages": sorted_langs,
        }
        
        return {
            "score": self.score,
            "details": self.details,
            "issues": self.issues,
            "strengths": self.strengths
        }
    
    def _analyze_commits(self, messages):
        """Analyze commit message quality."""
        if not messages:
            return 0
        
        bad = ["update", "fix", "wip", "test", ".", "-", "asdf"]
        good_count = 0
        
        for msg in messages:
            msg_lower = msg.lower().strip()
            if not msg_lower:
                continue
            is_bad = any(msg_lower == b or msg_lower.startswith(b + " ") for b in bad)
            if not is_bad and len(msg) >= 10:
                good_count += 1
        
        return (good_count / len(messages)) * 100 if messages else 0
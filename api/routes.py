"""API Routes"""

from flask import Blueprint, jsonify, request
import os

from core.github_fetcher import GitHubFetcher
from core.scoring_engine import ScoringEngine
from core.feedback_generator import FeedbackGenerator
from utils.validators import validate_github_url

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyze a GitHub profile.
    
    Request JSON:
        {
            "username": "github-username-or-url",
            "token": "optional-github-token"
        }
    
    Returns:
        JSON with analysis results
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        username_input = data.get("username", "")
        token = data.get("token") or os.getenv("GITHUB_TOKEN")
        
        # Validate input
        is_valid, username, error = validate_github_url(username_input)
        
        if not is_valid:
            return jsonify({"error": error}), 400
        
        # Fetch GitHub data
        fetcher = GitHubFetcher(token=token)
        github_data = fetcher.fetch_all_data(username)
        
        if not github_data:
            return jsonify({"error": f"User not found: {username}"}), 404
        
        # Calculate score
        scoring_engine = ScoringEngine()
        results = scoring_engine.calculate_score(github_data)
        
        # Generate feedback
        feedback_gen = FeedbackGenerator()
        feedback = feedback_gen.generate_feedback(results, github_data)
        
        # Compile response
        response = {
            "success": True,
            "profile": github_data["profile"],
            "score": results["final_score"],
            "grade": results["grade"],
            "score_color": results["score_color"],
            "category_scores": results["category_scores"],
            "summary": results["summary"],
            "feedback": feedback
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "GitHub Portfolio Analyzer"})
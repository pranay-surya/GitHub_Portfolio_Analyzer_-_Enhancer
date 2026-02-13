"""
GitHub Portfolio Analyzer - Flask Application
=============================================

Run with:
    python app.py
    
Or for production:
    gunicorn app:app
"""

import os
import traceback
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import core modules
from core.github_fetcher import GitHubFetcher
from core.scoring_engine import ScoringEngine
from core.feedback_generator import FeedbackGenerator
from utils.validators import validate_github_url
from api.routes import api_bp

# ============================================================
# APP CONFIGURATION
# ============================================================

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Register API blueprint
app.register_blueprint(api_bp)


# ============================================================
# ROUTES
# ============================================================

@app.route('/')
def index():
    """Home page with search form."""
    return render_template('index.html')


@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    """Analyze a GitHub profile."""
    
    if request.method == 'GET':
        # Handle GET request with username parameter
        username = request.args.get('username', '')
        if not username:
            return redirect(url_for('index'))
    else:
        # Handle POST request
        username = request.form.get('username', '')
    
    if not username:
        flash('Please enter a GitHub username or URL', 'error')
        return redirect(url_for('index'))
    
    # Validate input
    is_valid, clean_username, error = validate_github_url(username)
    
    if not is_valid:
        return render_template('index.html', error=error)
    
    try:
        # Get GitHub token from environment
        token = os.getenv('GITHUB_TOKEN')
        
        # Fetch GitHub data
        fetcher = GitHubFetcher(token=token)
        github_data = fetcher.fetch_all_data(clean_username)
        
        if not github_data:
            return render_template('error.html', error=f"User not found: {clean_username}")
        
        # Calculate score
        scoring_engine = ScoringEngine()
        results = scoring_engine.calculate_score(github_data)
        
        # Generate feedback
        feedback_gen = FeedbackGenerator()
        feedback = feedback_gen.generate_feedback(results, github_data)
        
        # Debug: Print what we're sending to template
        print("\n" + "="*50)
        print("DEBUG: Data being sent to template:")
        print(f"Profile username: {github_data['profile'].get('username')}")
        print(f"Score: {results.get('final_score')}")
        print(f"Grade: {results.get('grade')}")
        print(f"Feedback keys: {feedback.keys()}")
        print(f"Overall message type: {type(feedback.get('overall_message'))}")
        if isinstance(feedback.get('overall_message'), dict):
            print(f"Overall message keys: {feedback['overall_message'].keys()}")
        print("="*50 + "\n")
        
        # Render results
        try:
            return render_template(
                'results.html',
                profile=github_data['profile'],
                score=results['final_score'],
                grade=results['grade'],
                score_color=results['score_color'],
                category_scores=results['category_scores'],
                summary=results['summary'],
                feedback=feedback
            )
        except Exception as template_error:
            print(f"\nTemplate rendering error: {template_error}")
            print(f"Traceback: {traceback.format_exc()}")
            
            # Try to identify the specific issue
            if 'is undefined' in str(template_error):
                print(f"Missing variable in template: {template_error}")
            
            # Return a simple results page
            return f"""
            <html>
            <head><title>Results for @{clean_username}</title></head>
            <body>
                <h1>Analysis Results for @{clean_username}</h1>
                <h2>Score: {results['final_score']}/100 ({results['grade']})</h2>
                <p>There was an error rendering the full results page.</p>
                <p>Error: {str(template_error)}</p>
                <a href="/">Try Another Profile</a>
            </body>
            </html>
            """
    
    except Exception as e:
        print(f"Error analyzing {clean_username}: {str(e)}")
        print(f"Full traceback: {traceback.format_exc()}")
        return render_template('error.html', error=str(e))


@app.route('/health')
def health():
    """Health check endpoint."""
    return {'status': 'healthy', 'service': 'GitHub Portfolio Analyzer'}


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return render_template('error.html', error="Page not found"), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors."""
    return render_template('error.html', error="Internal server error"), 500


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == '__main__':
    # Get port from environment or default to 5000
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║         GitHub Portfolio Analyzer - Flask                ║
    ╠══════════════════════════════════════════════════════════╣
    ║  🌐 Running on: http://127.0.0.1:{port}                    ║
    ║  🔧 Debug mode: {debug}                                    ║
    ║  📡 API endpoint: http://127.0.0.1:{port}/api/analyze      ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
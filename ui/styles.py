"""
Custom CSS styles for the Streamlit application
"""

def get_custom_css() -> str:
    """Return custom CSS for the application."""
    return """
    <style>
        /* Main container styling */
        .main {
            padding: 2rem;
        }
        
        /* Score card styling */
        .score-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            padding: 2rem;
            text-align: center;
            color: white;
            margin: 1rem 0;
            box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
        }
        
        .score-number {
            font-size: 4rem;
            font-weight: bold;
            margin: 0;
        }
        
        .score-grade {
            font-size: 2rem;
            margin: 0.5rem 0;
        }
        
        /* Category cards */
        .category-card {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 0.5rem 0;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            border-left: 5px solid;
        }
        
        .category-documentation {
            border-color: #3498db;
        }
        
        .category-consistency {
            border-color: #2ecc71;
        }
        
        .category-quality {
            border-color: #9b59b6;
        }
        
        .category-impact {
            border-color: #f39c12;
        }
        
        /* Improvement cards */
        .improvement-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
            border-left: 4px solid #e74c3c;
        }
        
        .quick-win-card {
            background: #e8f5e9;
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
            border-left: 4px solid #27ae60;
        }
        
        /* Red flag styling */
        .red-flag {
            background: #ffebee;
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
            border-left: 4px solid #c62828;
        }
        
        /* Strength styling */
        .strength-item {
            background: #e3f2fd;
            border-radius: 8px;
            padding: 0.8rem;
            margin: 0.3rem 0;
        }
        
        /* Progress bar styling */
        .stProgress > div > div > div > div {
            background-color: #667eea;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Custom metric styling */
        .metric-container {
            background: white;
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        
        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            color: #333;
        }
        
        .metric-label {
            color: #666;
            font-size: 0.9rem;
        }
        
        /* Impact badge styling */
        .impact-high {
            background: #ffcdd2;
            color: #c62828;
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        
        .impact-medium {
            background: #fff9c4;
            color: #f57f17;
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        
        .impact-low {
            background: #c8e6c9;
            color: #2e7d32;
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: bold;
        }
    </style>
    """
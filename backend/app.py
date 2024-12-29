from flask import Flask
from backend.config import DevelopmentConfig  # Or ProductionConfig for production

def create_app():
    """Create the Flask application."""
    app = Flask(__name__)
    
    # Apply the configuration
    app.config.from_object(DevelopmentConfig)  # Use DevelopmentConfig for local development
    
    return app

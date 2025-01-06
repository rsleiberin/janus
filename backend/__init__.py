import os
from flask import Flask
from backend.db import db  # Correct import for db
from backend.config import DevelopmentConfig  # Or ProductionConfig for production
from backend.models import *  # Centralized import for all models


def create_app():
    """Factory function to create and configure the Flask application."""
    print("Starting app creation...")  # Start of app creation
    app = Flask(__name__)

    # Print the created app instance
    print(f"Created app instance: {app}")
    
    # Correctly resolve the database file path
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, "instance", "image_processing.db")
    
    # Print out the database path for debugging purposes
    print(f"Database path resolved: {db_path}")

    # Apply configuration
    app.config.from_object(DevelopmentConfig)  # Use DevelopmentConfig for local development
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Print the URI for the database connection
    print(f"Database URI set: {app.config['SQLALCHEMY_DATABASE_URI']}")

    # Print the created db instance
    print(f"Created db instance: {db}")

    # Initialize the database
    try:
        print("Initializing the database...")
        db.init_app(app)
        print("db.init_app() completed successfully.")
    except Exception as e:
        print(f"Error during db initialization: {e}")
        raise  # Ensure that if initialization fails, it is reported

    # Import and register blueprints inside the function to avoid circular imports
    try:
        from backend.routes.status_routes import status_bp
        from backend.routes.file_routes import file_bp
        print("Blueprints imported successfully.")
    except ImportError as e:
        print(f"Error importing blueprints: {e}")
        raise  # Raise an error if blueprints cannot be imported

    try:
        app.register_blueprint(status_bp)
        app.register_blueprint(file_bp)
        print("Blueprints registered successfully.")
    except Exception as e:
        print(f"Error registering blueprints: {e}")
        raise  # Raise an error if blueprint registration fails

    print("App creation complete.")
    return app

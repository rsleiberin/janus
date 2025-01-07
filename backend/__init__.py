import os
from flask import Flask
from backend.db import db  # Correct import for db
from backend.config import DevelopmentConfig  # Or ProductionConfig for production
from backend.models import *  # Centralized import for all models
from backend.utils.logger import CentralizedLogger  # Import centralized logger

# Initialize logger for this module
logger = CentralizedLogger("backend_init")


def create_app():
    """Factory function to create and configure the Flask application."""
    logger.log_to_console("INFO", "Starting app creation...")
    app = Flask(__name__)

    # Log the created app instance
    logger.log_to_console("DEBUG", "Created Flask app instance", instance=str(app))

    # Correctly resolve the database file path
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, "instance", "image_processing.db")
    
    # Log the database path
    logger.log_to_console("DEBUG", "Resolved database path", path=db_path)

    # Apply configuration
    app.config.from_object(DevelopmentConfig)  # Use DevelopmentConfig for local development
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Log the URI for the database connection
    logger.log_to_console("DEBUG", "Database URI set", uri=app.config["SQLALCHEMY_DATABASE_URI"])

    # Log the created db instance
    logger.log_to_console("DEBUG", "Database instance created", instance=str(db))

    # Initialize the database
    try:
        logger.log_to_console("INFO", "Initializing the database...")
        db.init_app(app)
        logger.log_to_console("INFO", "db.init_app() completed successfully.")
    except Exception as e:
        logger.log_to_console("ERROR", "Error during database initialization", error=str(e))
        raise  # Ensure that if initialization fails, it is reported

    # Import and register blueprints inside the function to avoid circular imports
    try:
        from backend.routes.status_routes import status_bp
        from backend.routes.file_routes import file_bp
        logger.log_to_console("INFO", "Blueprints imported successfully.")
    except ImportError as e:
        logger.log_to_console("ERROR", "Error importing blueprints", error=str(e))
        raise  # Raise an error if blueprints cannot be imported

    try:
        app.register_blueprint(status_bp)
        app.register_blueprint(file_bp)
        logger.log_to_console("INFO", "Blueprints registered successfully.")
    except Exception as e:
        logger.log_to_console("ERROR", "Error registering blueprints", error=str(e))
        raise  # Raise an error if blueprint registration fails

    logger.log_to_console("INFO", "App creation complete.")
    return app

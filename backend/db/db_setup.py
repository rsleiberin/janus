import os
import logging
from flask import Flask
from backend.models import db  # The shared SQLAlchemy instance
from backend.config import DevelopmentConfig  # Or ProductionConfig for production

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_app():
    """Factory function to create and configure the Flask application."""
    app = Flask(__name__)

    # Apply configuration
    config = DevelopmentConfig()  # Explicitly instantiate the config class
    app.config.from_object(config)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    logger.debug(f"Using database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

    # Initialize the database
    db.init_app(app)
    return app

if __name__ == "__main__":
    app = create_app()

    # Verify the database file exists
    db_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "instance", "image_processing.db")
    )
    if os.path.exists(db_path):
        logger.debug(f"Database file created successfully at {db_path}")
        logger.debug(f"File size: {os.path.getsize(db_path)} bytes")
    else:
        logger.error("ERROR: Database file not created!")

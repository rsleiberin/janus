import os
from flask import Flask
from backend.db import db  # The shared SQLAlchemy instance
from backend.config import DevelopmentConfig  # Or ProductionConfig for production
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.db.errors import DatabaseConnectionError

logger = CentralizedLogger()

def create_app():
    """Factory function to create and configure the Flask application."""
    app = Flask(__name__)

    # Apply configuration
    config = DevelopmentConfig()  # Explicitly instantiate the config class
    app.config.from_object(config)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    logger.log_to_console(
        "DEBUG",
        f"Using database URI: {app.config['SQLALCHEMY_DATABASE_URI']}"
    )

    # Initialize the database
    try:
        db.init_app(app)
    except Exception as error:
        raise DatabaseConnectionError("Failed to initialize the database.") from error

    return app

if __name__ == "__main__":
    app = create_app()

    # Verify the database file exists
    db_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "instance", "image_processing.db")
    )
    if os.path.exists(db_path):
        logger.log_to_console(
            "DEBUG",
            f"Database file created successfully at {db_path}"
        )
        logger.log_to_console(
            "DEBUG",
            f"File size: {os.path.getsize(db_path)} bytes"
        )
    else:
        error_message = "ERROR: Database file not created!"
        logger.log_to_console("ERROR", error_message)
        logger.log_to_db(
            level="ERROR",
            message=error_message,
            module="db_setup",
            meta_data={"db_path": db_path}
        )

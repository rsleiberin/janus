import os
from flask import Flask
from backend.db import db  # The shared SQLAlchemy instance
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.exceptions import DatabaseConnectionError
from backend.app import create_app

logger = CentralizedLogger()

def create_app_with_db(config_name="development"):
    """
    Factory function to create and configure the Flask application with the database.

    Args:
        config_name (str): The configuration name to use ('development', 'testing', 'production').

    Returns:
        Flask: Configured Flask application.
    """
    logger.log_to_console("DEBUG", f"Creating app with config: {config_name}...")

    app = create_app(config_name)

    # Initialize the database
    try:
        with app.app_context():
            db.create_all()
            logger.log_to_console("DEBUG", "Database initialized successfully.")
    except Exception as error:
        logger.log_to_console("ERROR", "Failed to initialize the database.", details=str(error))
        raise DatabaseConnectionError("Failed to initialize the database.") from error

    return app

if __name__ == "__main__":
    app = create_app_with_db()

    # Verify the database file exists
    db_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "instance", "backend.db")
    )
    if os.path.exists(db_path):
        logger.log_to_console(
            "DEBUG", f"Database file created successfully at {db_path}"
        )
        logger.log_to_console("DEBUG", f"File size: {os.path.getsize(db_path)} bytes")
    else:
        error_message = "ERROR: Database file not created!"
        logger.log_to_console("ERROR", error_message)
        logger.log_to_db(
            level="ERROR",
            message=error_message,
            module="db_setup",
            meta_data={"db_path": db_path},
        )

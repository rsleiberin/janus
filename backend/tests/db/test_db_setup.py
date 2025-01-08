import pytest
from flask import Flask
from backend.db.db_setup import create_app
from backend.db import db
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.db.errors import DatabaseConnectionError

# Set up logger for tests
logger = CentralizedLogger("test_logger", log_level="DEBUG")

def test_create_app():
    """
    Tests that create_app returns a Flask application with the expected configuration.
    """
    logger.log_to_console("DEBUG", "Starting test_create_app...")

    try:
        app = create_app()
        assert isinstance(app, Flask), "create_app did not return a Flask instance."

        # Check that the config is loaded
        assert "SQLALCHEMY_DATABASE_URI" in app.config, "Missing SQLALCHEMY_DATABASE_URI in config."
        logger.log_to_console("DEBUG", "Database URI from config", db_uri=app.config["SQLALCHEMY_DATABASE_URI"])

        # Check that db is initialized
        with app.app_context():
            assert db.engine is not None, "Database engine was not initialized."

        logger.log_to_console("DEBUG", "test_create_app passed successfully.")
    except DatabaseConnectionError as e:
        logger.log_to_console("ERROR", "DatabaseConnectionError caught in test", details=str(e))
        pytest.fail(f"DatabaseConnectionError: {str(e)}")

import pytest
import logging
from flask import Flask
from sqlalchemy import create_engine
from backend import create_app
from backend.db import db  # SQLAlchemy instance

# Configure test logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
test_logger = logging.getLogger("test_logger")


@pytest.fixture(scope="session")
def app():
    test_logger.debug("[SESSION] Initializing Flask application for testing...")
    application = create_app()

    application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    application.config["JWT_SECRET_KEY"] = "test_secret_key"
    application.config["JWT_TOKEN_LOCATION"] = ["headers"]
    application.config["TESTING"] = True

    test_logger.debug("[SESSION] Using in-memory SQLite database for testing.")
    return application


@pytest.fixture(scope="function")
def client(app):
    """Provides a test client for the Flask app."""
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="function")
def function_db_setup(app):
    test_logger.debug("[FUNCTION] Preparing database state for test function...")
    with app.app_context():
        test_logger.debug("[FUNCTION] Creating database tables...")
        db.create_all()
    yield
    test_logger.debug("[FUNCTION] Cleaning up database after test function...")
    with app.app_context():
        db.session.remove()
        db.drop_all()
        test_logger.debug("[FUNCTION] Database cleaned up successfully.")

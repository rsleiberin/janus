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
    """
    Creates a Flask application for testing.
    Overrides the DB URI with in-memory SQLite to ensure isolated test environments.
    """
    test_logger.debug("[SESSION] Initializing Flask application for testing...")
    application = create_app()

    # Set in-memory SQLite for tests
    application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    application.config["JWT_SECRET_KEY"] = "test_secret_key"  # Add a test JWT key
    application.config["JWT_TOKEN_LOCATION"] = ["headers"]   # Add JWT configuration
    application.config["TESTING"] = True

    test_logger.debug("[SESSION] Using in-memory SQLite database for testing.")
    return application


@pytest.fixture(scope="session")
def session_db_setup(app):
    """
    Performs one-time database connection checks at the session scope.
    """
    test_logger.debug("[SESSION] Verifying database connectivity...")
    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI")

    if not db_uri:
        test_logger.error("[SESSION] No SQLALCHEMY_DATABASE_URI defined in app config.")
        pytest.exit("A valid database URI is required for tests.")

    test_logger.debug(f"[SESSION] Using database URI: {db_uri}")
    try:
        engine = create_engine(db_uri)
        connection = engine.connect()
        test_logger.debug("[SESSION] Successfully connected to the database.")
        connection.close()
    except Exception as e:
        test_logger.error(f"[SESSION] Database connection error: {e}")
        pytest.exit("Database connectivity check failed.")

    # Yield for the test session
    yield
    test_logger.debug("[SESSION] Database connection checks complete.")


@pytest.fixture(scope="function")
def function_db_setup(app, session_db_setup):
    """
    Prepares a clean database state for each test function.
    """
    test_logger.debug("[FUNCTION] Preparing database state for test function...")
    with app.app_context():
        test_logger.debug("[FUNCTION] Creating database tables...")
        db.create_all()

        # Add required seed data
        test_logger.debug("[FUNCTION] Database tables created successfully.")

    # Yield control to the test function
    yield

    test_logger.debug("[FUNCTION] Cleaning up database after test function...")
    with app.app_context():
        db.session.remove()
        db.drop_all()
        test_logger.debug("[FUNCTION] Database cleaned up successfully.")

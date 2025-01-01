# conftest.py

import pytest
import logging
from flask import Flask
from sqlalchemy import create_engine
from backend import create_app
from backend.db import db  # SQLAlchemy instance

# Configure console logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("test_logger")


@pytest.fixture(scope="session")
def app():
    """
    Creates a Flask application for testing.
    Overrides the DB URI with in-memory SQLite so file path issues are avoided.
    """
    logger.debug("[SESSION] Creating the Flask application for the test session...")
    application = create_app()

    # Override to in-memory DB for tests
    application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    logger.debug("[SESSION] Overriding DB URI to in-memory: sqlite:///:memory:")

    logger.debug("[SESSION] Flask application created.")
    return application


@pytest.fixture(scope="session")
def session_db_setup(app):
    """
    Performs a one-time check of the database connection at session scope.
    Does NOT create or drop tables; that happens at function scope.
    """
    logger.debug("[SESSION] Checking database connectivity...")
    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI")
    if not db_uri:
        logger.error("[SESSION] No SQLALCHEMY_DATABASE_URI found in app config.")
        pytest.exit("Cannot proceed without a valid database URI.")

    logger.debug(f"[SESSION] Database URI: {db_uri}")
    try:
        engine = create_engine(db_uri)
        connection = engine.connect()
        logger.debug("[SESSION] Database connection succeeded.")
        connection.close()
    except Exception as e:
        logger.error(f"[SESSION] Database connection failed: {e}")
        pytest.exit("Terminating test session due to DB connection error.")

    # Yield for the rest of the test session
    yield
    logger.debug("[SESSION] Session-level DB checks complete. No teardown needed here.")


@pytest.fixture(scope="function")
def function_db_setup(app, session_db_setup):
    """
    Creates tables before each test function and drops them afterwards.
    Ensures a fresh DB state for every test.
    """
    logger.debug("[FUNCTION] Entering function_db_setup fixture...")
    with app.app_context():
        logger.debug("[FUNCTION] App context active. Creating all tables...")
        db.create_all()
        logger.debug("[FUNCTION] Tables created successfully.")

    # Hand over control to the test function
    yield

    logger.debug("[FUNCTION] Test function completed. Dropping all tables...")
    with app.app_context():
        db.session.remove()
        db.drop_all()
        logger.debug("[FUNCTION] All tables dropped. DB is clean for the next test.")

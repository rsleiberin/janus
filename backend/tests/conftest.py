import pytest
import logging
from backend import create_app
from backend.db import db  # Correct import for db
from sqlalchemy import create_engine
from flask import Flask

# Setup console logging
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    handlers=[logging.StreamHandler()])  # Log only to console
logger = logging.getLogger("test_logger")

@pytest.fixture(scope="function")
def init_db():
    """Fixture to setup a clean test database for each test."""
    app = create_app()

    logger.debug("Creating app and setting up the database...")
    
    with app.app_context():
        # Verify if app context is properly set
        logger.debug(f"App context set: {app.app_context() is not None}")
        
        # Check if db is correctly initialized and if the tables exist
        logger.debug("Attempting to create all tables in the database.")
        try:
            db.create_all()  # Ensure tables are created within the app context
            logger.debug("Database initialized for testing.")
            print("Database initialized for testing.")
        except Exception as e:
            logger.error(f"Error during database setup: {e}")
            print(f"Error during database setup: {e}")
            raise  # Reraise exception to ensure the test fails

    yield
    
    # Cleanup after the test
    with app.app_context():
        try:
            logger.debug("Cleaning up the database...")
            print("Cleaning up the database...")
            db.session.remove()
            db.drop_all()  # Drop all tables after test
            logger.debug("Database cleaned up after test.")
            print("Database cleaned up after test.")
        except Exception as e:
            logger.error(f"Error during database cleanup: {e}")
            print(f"Error during database cleanup: {e}")
            raise  # Reraise exception to ensure the test fails

@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_db():
    """Fixture to setup and tear down the database once for the whole test session."""
    print("Setting up the database...")
    app = create_app()

    logger.debug("App created. Proceeding with database initialization.")
    print("App created. Proceeding with database initialization.")

    # Check database connection before creating tables
    try:
        # Use the database URI configured for the app
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        connection = engine.connect()
        logger.debug("Database connection successful.")
        print("Database connection successful.")
        connection.close()  # Close the connection after check
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        print(f"Database connection failed: {e}")
        return  # If the connection fails, we should stop further execution.

    # Set up the application context and log the process
    with app.app_context():  # Ensure that we are within the app context for db operations
        try:
            logger.debug("Attempting to create all tables...")
            print("Attempting to create all tables...")  # Added for more visibility
            db.create_all()  # Create all tables
            logger.debug("Database initialized for testing.")
            print("Database initialized for testing.")
        except Exception as e:
            logger.error(f"Error during database setup: {e}")
            print(f"Error during database setup: {e}")
            raise  # Reraise the exception to ensure the test fails

    yield

    # Cleanup: Drop all tables after tests have run
    with app.app_context():  # Ensure that we are within the app context for cleanup
        try:
            logger.debug("Cleaning up the database...")
            print("Cleaning up the database...")
            db.session.remove()
            db.drop_all()  # Remove all tables
            logger.debug("Database cleaned up after tests.")
            print("Database cleaned up after tests.")
        except Exception as e:
            logger.error(f"Error during database cleanup: {e}")
            print(f"Error during database cleanup: {e}")
            raise  # Reraise the exception to ensure the test fails

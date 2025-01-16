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
    """Initialize the Flask application for testing."""
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
    """Prepare the database state for each test function."""
    test_logger.debug("[FUNCTION] Preparing database state for test function...")
    with app.app_context():
        test_logger.debug("[FUNCTION] Dropping all tables...")
        db.drop_all()  # Ensure no residual tables from previous tests
        test_logger.debug("[FUNCTION] Creating database tables...")
        db.create_all()  # Fresh schema for the test
        test_logger.debug("[FUNCTION] Database tables created successfully.")
    yield
    test_logger.debug("[FUNCTION] Cleaning up database after test function...")
    with app.app_context():
        db.session.remove()
        db.drop_all()  # Ensure all tables are removed after the test
        test_logger.debug("[FUNCTION] Database cleaned up successfully.")



@pytest.fixture(scope="function")
def user_with_token(app, function_db_setup):
    """Creates a user and provides a valid JWT token for testing."""
    from backend.models import User
    from flask_jwt_extended import create_access_token
    from werkzeug.security import generate_password_hash

    with app.app_context():
        # Create a user with a hashed password and default role
        hashed_password = generate_password_hash("testpassword123")
        user = User(
            username="testuser",
            email="testuser@example.com",
            password_hash=hashed_password,
            role="user"  # Set a default role
        )
        db.session.add(user)
        db.session.commit()

        # Generate a JWT token for the created user
        token = create_access_token(identity={"id": user.id, "email": user.email})
        return user, token

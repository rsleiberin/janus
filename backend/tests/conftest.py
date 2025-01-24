"""
Pytest fixtures for initializing the Flask application and database.
"""

import os
import pytest
from backend import create_app, db

@pytest.fixture(scope="session")
def app():
    """
    Session-wide Flask application for testing.
    """
    os.environ["FLASK_ENV"] = "testing"
    app = create_app(testing=True)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """
    Provides a test client for the Flask application.
    """
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="function")
def function_db_setup(app):
    """
    Prepares a clean database state for each test function.
    """
    with app.app_context():
        db.drop_all()
        db.create_all()
    yield
    with app.app_context():
        db.session.remove()
        db.drop_all()

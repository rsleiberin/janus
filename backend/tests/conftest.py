import pytest
from backend import create_app, db
import sys
import os

# Dynamically add the 'backend' directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
print("PYTHONPATH:", sys.path)

@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_db():
    """Fixture to set up and tear down the database."""
    app = create_app()
    with app.app_context():
        db.create_all()  # Ensure tables are created
        print("Database initialized for testing.")
    yield

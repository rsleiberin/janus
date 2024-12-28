import pytest
from backend import create_app
from backend.models import db

@pytest.fixture
def client():
    """Fixture for setting up the Flask test client with app context."""
    app = create_app()

    # Set up the database in the test environment
    with app.app_context():
        db.create_all()  # Ensure tables are created
        yield app.test_client()  # Yield the test client

        # Clean up after tests
        db.drop_all()

def test_status_route(client):
    """Test the /status endpoint."""
    response = client.get('/status')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'
    assert 'connected' in response.json['database']

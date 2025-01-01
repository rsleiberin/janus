import pytest
import os
from backend import create_app
import sys
print("PYTHONPATH:", sys.path)

@pytest.fixture
def client():
    """Fixture for setting up the Flask test client."""
    app = create_app()
    with app.test_client() as client:
        yield client

def test_files_endpoint(client):
    """Test the /files endpoint."""
    response = client.get('/files')
    assert response.status_code == 200
    assert 'files' in response.json
    assert isinstance(response.json['files'], list)

    # Verify at least one file is listed
    assert any('README.md' in file for file in response.json['files'])

def test_files_content_endpoint_valid(client):
    """Test the /files/content endpoint with a valid file."""
    valid_file_path = "README.md"
    response = client.post(
        '/files/content',
        json={"path": valid_file_path}
    )
    assert response.status_code == 200
    assert 'content' in response.json
    assert isinstance(response.json['content'], str)

def test_files_content_endpoint_invalid(client):
    """Test the /files/content endpoint with an invalid file."""
    invalid_file_path = "non_existent_file.txt"
    response = client.post(
        '/files/content',
        json={"path": invalid_file_path}
    )
    assert response.status_code == 404
    assert 'error' in response.json
    assert response.json['error'] == "File not found"

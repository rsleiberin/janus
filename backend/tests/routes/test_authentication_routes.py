import pytest
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from backend.models import User, db

@pytest.fixture
def access_token(app):
    """Generate a valid JWT access token."""
    with app.app_context():
        return create_access_token(identity={"id": 1, "username": "testuser"})


def test_register_user_success(client, mocker, function_db_setup):
    mock_logger = mocker.patch("backend.routes.authentication_routes.logger.log_to_console")
    payload = {"username": "testuser", "email": "testuser@example.com", "password": "securepassword123", "role": "user"}
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 201
    assert response.get_json()["message"] == "User registered successfully."


def test_login_user_success(client, mocker, function_db_setup):
    mock_logger = mocker.patch("backend.routes.authentication_routes.logger.log_to_console")
    user = User(username="testuser", email="testuser@example.com", password_hash=generate_password_hash("securepassword123"), role="user")
    db.session.add(user)
    db.session.commit()
    
    # Debugging: Ensure user is added
    assert User.query.filter_by(email="testuser@example.com").first() is not None

    payload = {"email": "testuser@example.com", "password": "securepassword123"}
    response = client.post("/auth/login", json=payload)
    
    # Debugging: Log the response
    print(response.status_code)
    print(response.get_json())

    assert response.status_code == 200
    assert "access_token" in response.get_json()



def test_login_user_invalid_credentials(client, mocker, function_db_setup):
    mock_logger = mocker.patch("backend.routes.authentication_routes.logger.log_to_console")
    payload = {"email": "nonexistent@example.com", "password": "wrongpassword"}
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 401
    assert response.get_json()["error"] == "Authentication error."


def test_user_profile_success(client, mocker, access_token, function_db_setup):
    mock_logger = mocker.patch("backend.routes.authentication_routes.logger.log_to_console")
    user = User(id=1, username="testuser", email="testuser@example.com", password_hash=generate_password_hash("securepassword123"), role="user")
    db.session.add(user)
    db.session.commit()
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/auth/profile", headers=headers)
    assert response.status_code == 200
    assert response.get_json()["username"] == "testuser"


def test_user_profile_unauthorized(client):
    response = client.get("/auth/profile")
    assert response.status_code == 401

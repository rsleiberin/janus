import pytest
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from backend.models import User, db

@pytest.fixture
def user_with_token(app, function_db_setup):
    """Fixture to create a user and return a valid JWT token."""
    with app.app_context():
        # Cleanup existing test user
        User.query.filter_by(email="testuser@example.com").delete()
        db.session.commit()  # Ensure cleanup is applied

        # Create a new test user
        user = User(
            username="testuser",
            email="testuser@example.com",
            password_hash=generate_password_hash("password123"),
            role="user"
        )
        db.session.add(user)
        db.session.commit()

        # Generate access token
        token = create_access_token(identity={"id": user.id, "email": user.email})
        return user, token


def test_login_success(client, function_db_setup, user_with_token):
    """Test successful login."""
    payload = {"email": "testuser@example.com", "password": "password123"}
    response = client.post("/security/login", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_invalid_credentials(client, function_db_setup):
    """Test login with invalid credentials."""
    payload = {"email": "wrong@example.com", "password": "wrongpassword"}
    response = client.post("/security/login", json=payload)
    assert response.status_code == 401
    data = response.get_json()
    assert data["error_code"] == "AUTHENTICATION_ERROR"
    assert data["message"] == "Invalid credentials provided."


def test_access_protected_route_success(client, function_db_setup, user_with_token):
    """Test accessing a protected route with a valid token."""
    _, token = user_with_token
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/security/protected", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Welcome testuser@example.com!"


def test_access_protected_route_no_token(client, function_db_setup):
    """Test accessing a protected route without a token."""
    response = client.get("/security/protected")
    assert response.status_code == 401
    data = response.get_json()
    assert data["message"] == "Authentication failed. Please log in."  # Updated to match handler output
    assert data["error_code"] == "AUTHENTICATION_FAILED"




def test_access_protected_route_invalid_token(client, function_db_setup):
    """Test accessing a protected route with an invalid token."""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/security/protected", headers=headers)
    assert response.status_code == 401  # Ensure the status code matches the handler
    data = response.get_json()
    assert data["message"] == "Token is invalid or expired."
    assert data["error_code"] == "INVALID_TOKEN"

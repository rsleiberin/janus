import pytest
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from backend.models import User, db

@pytest.fixture
def user_with_token(app):
    """Fixture to create a user and return a valid JWT token."""
    with app.app_context():
        # Cleanup existing test user
        User.query.filter_by(email="testuser@example.com").delete()
        
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

def test_login_success(client, user_with_token):
    """Test successful login."""
    payload = {"email": "testuser@example.com", "password": "password123"}
    response = client.post("/security/login", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data
    assert "refresh_token" in data

def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    payload = {"email": "wrong@example.com", "password": "wrongpassword"}
    response = client.post("/security/login", json=payload)
    assert response.status_code == 401
    data = response.get_json()
    assert data["error"] == "Invalid email or password."

def test_access_protected_route_success(client, user_with_token):
    """Test accessing a protected route with a valid token."""
    _, token = user_with_token
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/security/protected", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Access granted."

def test_access_protected_route_no_token(client):
    """Test accessing a protected route without a token."""
    response = client.get("/security/protected")
    assert response.status_code == 401
    data = response.get_json()
    assert data["error"] == "Missing Authorization Header"

def test_access_protected_route_invalid_token(client):
    """Test accessing a protected route with an invalid token."""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/security/protected", headers=headers)
    assert response.status_code == 401
    data = response.get_json()
    assert data["error"] == "Token is invalid or expired."

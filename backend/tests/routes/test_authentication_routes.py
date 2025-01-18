import pytest
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash
from backend.models import User
from backend.db import db

def test_register_user_success(client, mocker, function_db_setup):
    mock_logger = mocker.patch("backend.routes.authentication_routes.logger.log_to_console")

    # Prepare request data without "role"
    data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "securepassword123"
    }

    response = client.post("/auth/register", json=data)
    assert response.status_code == 201
    assert response.get_json()["message"] == "User registered successfully."

    # Assert that logger was called
    mock_logger.assert_any_call("INFO", "User registered: testuser")


def test_login_user_success(client, mocker, function_db_setup):
    mock_logger = mocker.patch("backend.routes.authentication_routes.logger.log_to_console")

    # Create a user without "role"
    user = User(
        username="testuser",
        email="testuser@example.com",
        password_hash=generate_password_hash("securepassword123")
    )
    db.session.add(user)
    db.session.commit()

    # Login request
    data = {
        "email": "testuser@example.com",
        "password": "securepassword123"
    }
    response = client.post("/auth/login", json=data)
    assert response.status_code == 200
    assert "access_token" in response.get_json()

    # Assert logging
    mock_logger.assert_any_call("INFO", f"User logged in: {user.username}")


def test_login_user_invalid_credentials(client, mocker, function_db_setup):
    mock_logger = mocker.patch("backend.routes.authentication_routes.logger.log_to_console")

    # No user is created in DB, so login should fail
    data = {
        "email": "missing@example.com",
        "password": "invalid"
    }
    response = client.post("/auth/login", json=data)
    assert response.status_code == 401
    assert response.get_json()["error"] == "Authentication error."


def test_user_profile_success(client, mocker, function_db_setup):
    mock_logger = mocker.patch("backend.routes.authentication_routes.logger.log_to_console")

    # Create a user without "role"
    user = User(
        id=1,
        username="testuser",
        email="testuser@example.com",
        password_hash=generate_password_hash("securepassword123")
    )
    db.session.add(user)
    db.session.commit()

    # Create an access token for that user
    token = create_access_token(identity={"id": user.id, "username": user.username})

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/profile", headers=headers)

    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"

    # Assert logging
    mock_logger.assert_any_call("INFO", f"Profile accessed: {user.username}")


def test_user_profile_unauthorized(client, function_db_setup):
    # No token provided, should fail with 401
    response = client.get("/auth/profile")
    assert response.status_code == 401
    assert response.get_json()["error_code"] == "AUTHENTICATION_FAILED"

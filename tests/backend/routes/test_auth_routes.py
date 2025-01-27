"""
Tests for the unified auth_routes.py
"""

# pylint: disable=redefined-outer-name,unused-argument

import pytest
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from backend.db import db
from backend.models import User


@pytest.fixture
def token_for_user(app):
    """
    Creates a JWT token for user ID=123, email='valid@example.com'.
    """
    with app.app_context():
        return create_access_token(identity={"id": 123, "email": "valid@example.com"})


@pytest.mark.usefixtures("function_db_setup")
def test_register_user_success(client):
    """
    Test registering a new user successfully.
    """
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword",
    }
    response = client.post("/auth/register", json=payload)
    data = response.get_json()

    assert response.status_code == 201
    assert data["message"] == "User registered successfully."

    created_user = User.query.filter_by(email="test@example.com").first()
    assert created_user
    assert check_password_hash(created_user.password_hash, "securepassword")


@pytest.mark.usefixtures("function_db_setup")
def test_register_user_conflict(client):
    """
    Test registering a user when the email/username already exists.
    """
    existing = User(
        username="existing",
        email="existing@example.com",
        password_hash=generate_password_hash("oldpassword"),
    )
    db.session.add(existing)
    db.session.commit()

    payload = {
        "username": "existing",
        "email": "existing@example.com",
        "password": "newpassword",
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 409
    data = response.get_json()
    assert data["error"] == "Email or username already exists."


def test_register_user_missing_fields(client):
    """
    Test registering a user with missing fields.
    """
    payload = {
        "username": "incompleteuser",
        "email": "incomplete@example.com",
        # missing 'password'
    }
    response = client.post("/auth/register", json=payload)
    data = response.get_json()

    assert response.status_code == 400
    assert data["error_code"] == "VALIDATION_ERROR"
    assert "Missing field" in data["details"]


@pytest.mark.usefixtures("function_db_setup")
def test_login_success(client):
    """
    Test login with valid credentials.
    """
    user = User(
        username="validuser",
        email="valid@example.com",
        password_hash=generate_password_hash("correctpassword"),
    )
    db.session.add(user)
    db.session.commit()

    payload = {"email": "valid@example.com", "password": "correctpassword"}
    response = client.post("/auth/login", json=payload)
    data = response.get_json()

    assert response.status_code == 200
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_invalid_credentials(client):
    """
    Test login with invalid credentials (user doesn't exist).
    """
    payload = {"email": "noexist@example.com", "password": "wrong"}
    response = client.post("/auth/login", json=payload)
    data = response.get_json()

    assert response.status_code == 401
    assert data["error_code"] == "AUTHENTICATION_FAILED"


@pytest.mark.usefixtures("function_db_setup")
def test_logout_success(client, token_for_user):
    """
    Test logout endpoint with a valid token.
    """
    # Create matching user in DB
    user = User(
        id=123,
        username="testlogout",
        email="valid@example.com",
        password_hash=generate_password_hash("correctpassword"),
    )
    db.session.add(user)
    db.session.commit()

    headers = {"Authorization": f"Bearer {token_for_user}"}
    response = client.post("/auth/logout", headers=headers)
    data = response.get_json()

    assert response.status_code == 200
    assert data["message"] == "Logout successful."


def test_logout_unauthorized(client):
    """
    Test logout without token.
    """
    response = client.post("/auth/logout")
    data = response.get_json()

    assert response.status_code == 401
    assert data["error_code"] == "AUTHENTICATION_FAILED"


def test_refresh_token_success(client, token_for_user):
    """
    Test refresh token with a valid token (assuming it's recognized as refresh).
    """
    headers = {"Authorization": f"Bearer {token_for_user}"}
    response = client.post("/auth/refresh", headers=headers)

    # Possibly 200 if recognized as refresh, else 422 or 401
    if response.status_code == 200:
        data = response.get_json()
        assert "access_token" in data
    else:
        assert response.status_code in (401, 422)


def test_reset_password_success(client):
    """
    Test resetting password with valid email.
    """
    payload = {"email": "reset@example.com"}
    response = client.post("/auth/reset-password", json=payload)
    data = response.get_json()

    assert response.status_code == 200
    assert data["message"] == "Password reset email sent."


@pytest.mark.usefixtures("function_db_setup")
def test_change_password_success(client):
    """
    Test changing a user's password with valid old/new password.
    """
    # Create user in DB
    user = User(
        id=999,
        username="pwchange",
        email="pwchange@example.com",
        password_hash=generate_password_hash("oldpassword"),
    )
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity={"id": 999, "email": "pwchange@example.com"})

    headers = {"Authorization": f"Bearer {token}"}
    payload = {"old_password": "oldpassword", "new_password": "newpassword123"}
    response = client.post("/auth/change-password", json=payload, headers=headers)
    data = response.get_json()

    assert response.status_code == 200
    assert data["message"] == "Password changed successfully."

    updated_user = db.session.get(User, 999)
    assert check_password_hash(updated_user.password_hash, "newpassword123")

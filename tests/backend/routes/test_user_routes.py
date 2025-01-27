"""
Tests for user_routes.py
"""

# pylint: disable=redefined-outer-name,unused-argument

import pytest
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from backend.db import db
from backend.models import User


@pytest.fixture
def access_token(app):
    """
    Creates a JWT token for user id=1, username='testuser'.
    """
    with app.app_context():
        return create_access_token(identity={"id": 1, "username": "testuser"})


@pytest.mark.usefixtures("function_db_setup")
def test_get_user_profile_success(client, access_token):
    user = User(
        id=1,
        username="testuser",
        email="testuser@example.com",
        password_hash=generate_password_hash("secure123"),
    )
    db.session.add(user)
    db.session.commit()

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/user/profile", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"


@pytest.mark.usefixtures("function_db_setup")
def test_get_user_profile_not_found(client, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/user/profile", headers=headers)
    assert response.status_code == 404
    data = response.get_json()
    assert data["error_code"] == "USER_NOT_FOUND"


@pytest.mark.usefixtures("function_db_setup")
def test_update_user_profile_success(client, access_token):
    user = User(
        id=1,
        username="olduser",
        email="olduser@example.com",
        password_hash=generate_password_hash("pw123"),
    )
    db.session.add(user)
    db.session.commit()

    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {"username": "newuser"}
    response = client.put("/user/profile", json=payload, headers=headers)
    data = response.get_json()

    assert response.status_code == 200
    assert data["message"] == "User profile updated successfully."

    updated_user = db.session.get(User, 1)
    assert updated_user.username == "newuser"


@pytest.mark.usefixtures("function_db_setup")
def test_update_user_profile_invalid_data(client, access_token):
    user = User(
        id=1,
        username="testuser",
        email="testuser@example.com",
        password_hash=generate_password_hash("pass123"),
    )
    db.session.add(user)
    db.session.commit()

    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {}
    response = client.put("/user/profile", json=payload, headers=headers)
    data = response.get_json()

    assert response.status_code == 400
    assert data["error_code"] == "INVALID_USER_DATA"

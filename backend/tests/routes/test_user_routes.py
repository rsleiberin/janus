import pytest
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from backend.models import User, db


@pytest.fixture
def access_token(app):
    """Generate a valid JWT access token."""
    with app.app_context():
        return create_access_token(identity={"id": 1, "username": "testuser"})


def test_get_user_profile_success(client, mocker, access_token, function_db_setup):
    user = User(
        id=1,
        username="testuser",
        email="testuser@example.com",
        password_hash=generate_password_hash("securepassword123"),
    )
    db.session.add(user)
    db.session.commit()

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/user/profile", headers=headers)
    assert response.status_code == 200
    assert response.get_json()["username"] == "testuser"


def test_get_user_profile_not_found(client, mocker, access_token, function_db_setup):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/user/profile", headers=headers)
    assert response.status_code == 404
    assert response.get_json()["error_code"] == "USER_NOT_FOUND"


def test_update_user_profile_success(client, mocker, access_token, function_db_setup):
    user = User(
        id=1,
        username="testuser",
        email="testuser@example.com",
        password_hash=generate_password_hash("securepassword123"),
    )
    db.session.add(user)
    db.session.commit()

    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {"username": "updateduser"}
    response = client.put("/user/profile", headers=headers, json=payload)
    assert response.status_code == 200
    assert response.get_json()["message"] == "User profile updated successfully."

    updated_user = db.session.get(User, 1)
    assert updated_user.username == "updateduser"


def test_update_user_profile_invalid_data(client, access_token, function_db_setup):
    user = User(
        id=1,
        username="testuser",
        email="testuser@example.com",
        password_hash=generate_password_hash("securepassword123"),
    )
    db.session.add(user)
    db.session.commit()

    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {}  # Missing required fields
    response = client.put("/user/profile", headers=headers, json=payload)
    assert response.status_code == 400
    assert response.get_json()["error_code"] == "INVALID_USER_DATA"

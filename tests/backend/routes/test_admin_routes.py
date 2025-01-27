"""
Tests for admin_routes.py
"""

# pylint: disable=redefined-outer-name,unused-argument

import pytest
from flask_jwt_extended import create_access_token
from backend.db import db
from backend.models import User, Log
from backend.routes.admin_routes import logger
from werkzeug.security import generate_password_hash
from unittest.mock import call
from datetime import datetime


@pytest.fixture
def admin_access_token(app):
    """
    Generate a valid JWT access token for an 'admin' user (role in token only).
    """
    with app.app_context():
        return create_access_token(
            identity={"id": 1, "username": "admin", "role": "admin"}
        )


@pytest.fixture
def mock_logger(mocker):
    """Mocks the logger for admin_routes testing."""
    return mocker.patch.object(logger, "log_to_console")


@pytest.mark.usefixtures("function_db_setup")
def test_get_all_users_success(client, admin_access_token, mock_logger):
    """
    Test fetching all users as an admin.
    """
    admin_user = User(
        id=1,
        username="admin",
        email="admin@example.com",
        password_hash=generate_password_hash("adminpassword"),
    )
    regular_user = User(
        id=2,
        username="user",
        email="user@example.com",
        password_hash=generate_password_hash("userpassword"),
    )
    db.session.add_all([admin_user, regular_user])
    db.session.commit()

    headers = {"Authorization": f"Bearer {admin_access_token}"}
    response = client.get("/admin/users", headers=headers)

    assert response.status_code == 200
    users = response.get_json()
    assert len(users) == 2
    assert users[0]["username"] == "admin"
    assert users[1]["username"] == "user"

    expected_calls = [
        call(
            "INFO",
            "Admin user requested user list",
            user_id={"id": 1, "username": "admin", "role": "admin"},
        ),
        call("INFO", "Successfully fetched user list", count=2),
    ]
    mock_logger.assert_has_calls(expected_calls, any_order=False)


def test_get_all_users_unauthorized(client):
    """
    Test fetching all users without admin privileges.
    """
    response = client.get("/admin/users")
    assert response.status_code == 401
    data = response.get_json()
    assert data["error_code"] == "AUTHENTICATION_FAILED"


@pytest.mark.usefixtures("function_db_setup")
def test_delete_user_success(client, admin_access_token, mock_logger):
    """
    Test deleting a user as an admin.
    """
    admin_user = User(
        id=1,
        username="admin",
        email="admin@example.com",
        password_hash=generate_password_hash("adminpassword"),
    )
    regular_user = User(
        id=2,
        username="user",
        email="user@example.com",
        password_hash=generate_password_hash("userpassword"),
    )
    db.session.add_all([admin_user, regular_user])
    db.session.commit()

    headers = {"Authorization": f"Bearer {admin_access_token}"}
    response = client.delete("/admin/users/2", headers=headers)

    assert response.status_code == 200
    assert response.get_json()["message"] == "User deleted successfully."

    deleted_user = db.session.get(User, 2)
    assert deleted_user is None

    mock_logger.assert_any_call(
        "INFO",
        "Admin user requested user deletion",
        user_id={"id": 1, "username": "admin", "role": "admin"},
        target_user=2,
    )
    mock_logger.assert_any_call("INFO", "User deleted successfully", target_user=2)


@pytest.mark.usefixtures("function_db_setup")
def test_delete_user_not_found(client, admin_access_token, mock_logger):
    """
    Test deleting a non-existent user.
    """
    admin_user = User(
        id=1,
        username="admin",
        email="admin@example.com",
        password_hash=generate_password_hash("adminpassword"),
    )
    db.session.add(admin_user)
    db.session.commit()

    headers = {"Authorization": f"Bearer {admin_access_token}"}
    response = client.delete("/admin/users/999", headers=headers)

    assert response.status_code == 404
    data = response.get_json()
    assert data["error_code"] == "USER_NOT_FOUND"
    assert data["message"] == "User not found."

    mock_logger.assert_any_call(
        "INFO",
        "Admin user requested user deletion",
        user_id={"id": 1, "username": "admin", "role": "admin"},
        target_user=999,
    )
    mock_logger.assert_any_call(
        "WARNING", "User not found for deletion", target_user=999
    )


@pytest.mark.usefixtures("function_db_setup")
def test_get_logs_success(client, admin_access_token, mock_logger):
    """
    Test fetching logs as an admin.
    """
    log1 = Log(
        action="Test log 1",
        level="INFO",
        module="test",
        user_id=1,
        timestamp=datetime(2025, 1, 11, 0, 0, 0),
    )
    log2 = Log(
        action="Test log 2",
        level="ERROR",
        module="test",
        user_id=2,
        timestamp=datetime(2025, 1, 11, 1, 0, 0),
    )
    db.session.add_all([log1, log2])
    db.session.commit()

    headers = {"Authorization": f"Bearer {admin_access_token}"}
    response = client.get("/admin/logs", headers=headers)
    assert response.status_code == 200

    logs = response.get_json()
    assert len(logs) == 2
    # Check descending order by timestamp
    assert logs[0]["action"] == "Test log 2"
    assert logs[1]["action"] == "Test log 1"

    mock_logger.assert_any_call(
        "INFO",
        "Admin user requested logs",
        user_id={"id": 1, "username": "admin", "role": "admin"},
    )
    mock_logger.assert_any_call("INFO", "Successfully fetched logs", count=2)


def test_get_logs_unauthorized(client):
    """
    Test fetching logs without admin privileges.
    """
    response = client.get("/admin/logs")
    assert response.status_code == 401
    data = response.get_json()
    assert data["error_code"] == "AUTHENTICATION_FAILED"

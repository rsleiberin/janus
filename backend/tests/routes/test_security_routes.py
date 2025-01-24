# File: backend/tests/routes/test_security_routes.py

import pytest
from unittest.mock import MagicMock
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    from backend.app import create_app, db
    app = create_app('testing')  # Use 'testing' as the configuration name
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()


def test_login_valid_credentials(client, mocker):
    """Test login with valid credentials."""
    payload = {"email": "validuser@example.com", "password": "correctpassword"}

    # Mock logger
    mock_logger = mocker.patch("backend.utils.logger.CentralizedLogger.log_to_console")

    # Mock database user query
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.email = payload["email"]
    mock_user.password_hash = generate_password_hash("correctpassword")

    mock_filter_by = mocker.patch("backend.models.User.query.filter_by")
    mock_filter_by.return_value.first.return_value = mock_user

    # Send the request
    response = client.post("/security/login", json=payload, content_type="application/json")
    data = response.get_json()

    # Assert response
    assert response.status_code == 200
    assert "access_token" in data
    assert "refresh_token" in data

    # Assert logger calls
    mock_logger.assert_any_call("DEBUG", "Login endpoint hit.")
    mock_logger.assert_any_call("DEBUG", "Request payload received.", payload=payload)
    mock_logger.assert_any_call("DEBUG", f"Validating user with email: {payload['email']}")
    mock_logger.assert_any_call("DEBUG", f"User fetched: {mock_user.email}")
    mock_logger.assert_any_call("DEBUG", f"User authenticated: {mock_user.email}")
    mock_logger.assert_any_call("INFO", f"User {mock_user.email} logged in successfully.")


def test_login_invalid_credentials(client, mocker):
    """Test login with invalid credentials."""
    payload = {"email": "wrong@example.com", "password": "wrongpassword"}

    # Mock logger
    mock_logger = mocker.patch("backend.utils.logger.CentralizedLogger.log_to_console")

    # Mock database user query
    mock_filter_by = mocker.patch("backend.models.User.query.filter_by")
    mock_filter_by.return_value.first.return_value = None  # Simulate invalid user

    # Send the request
    response = client.post("/security/login", json=payload, content_type="application/json")
    data = response.get_json()

    # Assert response
    assert response.status_code == 401
    assert "msg" in data
    assert data["msg"] == "Invalid email or password."

    # Assert logger calls
    mock_logger.assert_any_call("DEBUG", "Login endpoint hit.")
    mock_logger.assert_any_call("DEBUG", "Request payload received.", payload=payload)
    mock_logger.assert_any_call("DEBUG", f"Validating user with email: {payload['email']}")
    mock_logger.assert_any_call("WARNING", "User not found.", email=payload["email"])

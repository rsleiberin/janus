# File: backend/tests/routes/test_security_routes.py

import pytest
from unittest.mock import MagicMock
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    from backend.app import create_app  # Adjust the import as per your app's factory
    app = create_app(testing=True)
    with app.test_client() as client:
        yield client

def test_login_valid_credentials(client, mocker):
    """Test login with valid credentials."""
    payload = {"email": "validuser@example.com", "password": "correctpassword"}

    # Mock logger
    mock_logger = mocker.patch("backend.routes.security_routes.logger.log_to_console")

    # Mock database user query
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.email = payload["email"]
    mock_user.password_hash = generate_password_hash("correctpassword")

    mock_filter_by = mocker.patch("backend.routes.security_routes.User.query.filter_by")
    mock_filter_by.return_value.first.return_value = mock_user

    # Send the request
    response = client.post("/security/login", json=payload, content_type="application/json")
    data = response.get_json()

    # Assert logger calls
    mock_logger.assert_any_call("DEBUG", "Login endpoint hit.")
    mock_logger.assert_any_call("DEBUG", "Request payload received.", payload=payload)
    mock_logger.assert_any_call("DEBUG", f"Validating user with email: {payload['email']}")
    mock_logger.assert_any_call("DEBUG", f"User fetched: {mock_user.email}")
    mock_logger.assert_any_call("DEBUG", f"User authenticated: {mock_user.email}")
    mock_logger.assert_any_call("INFO", f"User {mock_user.email} logged in successfully.")

    # Assert the query mock was called
    assert mock_filter_by.called, "Mock for filter_by was not called."

    # Assert the response contains access and refresh tokens
    assert "access_token" in data, "Missing 'access_token' in response."
    assert "refresh_token" in data, "Missing 'refresh_token' in response."
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"


def test_login_invalid_credentials(client, mocker):
    """Test login with invalid credentials."""
    payload = {"email": "wrong@example.com", "password": "wrongpassword"}

    # Mock logger
    mock_logger = mocker.patch("backend.routes.security_routes.logger.log_to_console")

    # Mock database user query
    mock_filter_by = mocker.patch("backend.routes.security_routes.User.query.filter_by")
    mock_filter_by.return_value.first.return_value = None  # Simulate invalid user

    response = client.post("/security/login", json=payload, content_type="application/json")
    data = response.get_json()

    # Assert logger calls
    mock_logger.assert_any_call("DEBUG", "Login endpoint hit.")
    mock_logger.assert_any_call("DEBUG", "Request payload received.", payload=payload)
    mock_logger.assert_any_call("DEBUG", f"Validating user with email: {payload['email']}")
    mock_logger.assert_any_call("WARNING", "User not found.", email=payload["email"])

    # Assert the query mock was called
    assert mock_filter_by.called, "Mock for filter_by was not called."

    # Assert the response structure
    assert response.status_code == 401, f"Expected status code 401, got {response.status_code}"
    assert "status" in data, "Missing 'status' in response."
    assert "error_code" in data, "Missing 'error_code' in response."
    assert "message" in data, "Missing 'message' in response."
    assert data["error_code"] == "AUTHENTICATION_FAILED"
    assert data["message"] == "Authentication failed. Please check your credentials."
    assert "details" in data, "Missing 'details' in response."
    assert data["details"] == "Invalid email or password."

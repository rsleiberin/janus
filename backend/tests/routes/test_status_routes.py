import pytest
from sqlalchemy.exc import OperationalError
from backend.utils.error_handling.routes.errors import DatabaseUnavailableError


def test_health_check_success(client, mocker):
    """
    Test the /status endpoint when the database is connected successfully.
    """
    # Mock the database session to simulate successful connection
    mock_session = mocker.patch("backend.db.session.execute")
    mock_session.return_value = None  # Simulate success

    # Perform the health check
    response = client.get("/status")
    data = response.get_json()

    # Assertions
    assert response.status_code == 200
    assert data["status"] == "ok"
    assert data["database"] == "connected"


def test_health_check_database_error(client, mocker):
    """
    Test the /status endpoint when the database connection fails.
    """
    # Mock the database session to simulate a connection failure
    mock_session = mocker.patch("backend.db.session.execute")
    mock_session.side_effect = OperationalError("Mocked database error", {}, None)

    # Perform the health check
    response = client.get("/status")
    data = response.get_json()

    # Assertions
    assert response.status_code == 500
    assert data is not None
    assert data["status"] == 500
    assert data["error_code"] == "DATABASE_UNAVAILABLE"
    assert data["message"] == "The database is not accessible at this time."
    assert "Database connection failed." in data["details"]



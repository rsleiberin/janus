"""
Tests for status_routes.py
"""

# pylint: disable=redefined-outer-name,unused-argument

import pytest
from sqlalchemy.exc import OperationalError
from unittest.mock import patch


@pytest.mark.usefixtures("function_db_setup")
def test_status_ok(client):
    """
    Test the /status endpoint for a healthy DB connection.
    """
    response = client.get("/status")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert data["database"] == "connected"


@pytest.mark.usefixtures("function_db_setup")
@patch("backend.db.db.session.execute", side_effect=OperationalError("Test", {}, None))
def test_status_db_unavailable(mock_execute, client):
    """
    Test the /status endpoint when the DB is not accessible.
    """
    response = client.get("/status")
    data = response.get_json()

    assert response.status_code == 500
    assert data["error_code"] == "DATABASE_CONNECTION_FAILED"
    assert "not accessible" in data["message"]


@pytest.mark.usefixtures("function_db_setup")
@patch("backend.db.db.session.execute", side_effect=Exception("Unhandled test error"))
def test_status_unhandled_error(mock_execute, client):
    """
    Test the /status endpoint when an unhandled exception occurs.
    """
    response = client.get("/status")
    data = response.get_json()

    assert response.status_code == 500
    assert data["error_code"] == "HEALTH_CHECK_ERROR"
    assert "error occurred during the health check" in data["message"]

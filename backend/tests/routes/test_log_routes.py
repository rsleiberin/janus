import pytest
from flask_jwt_extended import create_access_token
from backend.models import User


def test_get_logs_success(client, user_with_token):
    """Test successful retrieval of logs."""
    _, token = user_with_token
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/logs/", headers=headers)
    assert response.status_code == 200

    data = response.get_json()
    assert "logs" in data
    assert isinstance(data["logs"], list)
    assert len(data["logs"]) > 0


def test_get_logs_unauthorized(client):
    """Test retrieving logs without a valid token."""
    response = client.get("/logs/")
    assert response.status_code == 401

    data = response.get_json()
    assert data["error_code"] == "AUTHENTICATION_FAILED"
    assert data["message"] == "Authentication failed. Please log in."


def test_get_log_by_id_success(client, user_with_token):
    """Test successful retrieval of a specific log by ID."""
    _, token = user_with_token
    headers = {"Authorization": f"Bearer {token}"}

    log_id = 1  # Assuming log ID 1 exists for testing purposes
    response = client.get(f"/logs/{log_id}", headers=headers)
    assert response.status_code == 200

    data = response.get_json()
    assert "log" in data
    assert isinstance(data["log"], dict)
    assert data["log"]["id"] == log_id


def test_get_log_by_id_not_found(client, user_with_token):
    """Test retrieving a log by an ID that does not exist."""
    _, token = user_with_token
    headers = {"Authorization": f"Bearer {token}"}

    non_existent_log_id = 999
    response = client.get(f"/logs/{non_existent_log_id}", headers=headers)
    assert response.status_code == 404

    data = response.get_json()
    assert data["error_code"] == "LOG_NOT_FOUND"
    assert data["message"] == f"Log with ID {non_existent_log_id} not found."


def test_get_log_by_id_unauthorized(client):
    """Test retrieving a specific log without a valid token."""
    log_id = 1
    response = client.get(f"/logs/{log_id}")
    assert response.status_code == 401

    data = response.get_json()
    assert data["error_code"] == "AUTHENTICATION_FAILED"
    assert data["message"] == "Authentication failed. Please log in."

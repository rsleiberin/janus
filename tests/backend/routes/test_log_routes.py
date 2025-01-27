"""
Tests for log_routes.py
"""

# pylint: disable=redefined-outer-name,unused-argument

import pytest


@pytest.mark.usefixtures("function_db_setup")
def test_get_logs_success(client, user_with_token):
    """
    Test successful retrieval of logs (currently mock).
    """
    _, token = user_with_token
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/logs/", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert "logs" in data
    assert isinstance(data["logs"], list)


def test_get_logs_unauthorized(client):
    """
    Test retrieving logs without a valid token.
    """
    response = client.get("/logs/")
    assert response.status_code == 401
    data = response.get_json()
    assert data["error_code"] == "AUTHENTICATION_FAILED"


@pytest.mark.usefixtures("function_db_setup")
def test_get_log_by_id_success(client, user_with_token):
    """
    Test successful retrieval of a specific log by ID (mock logic).
    """
    _, token = user_with_token
    headers = {"Authorization": f"Bearer {token}"}
    log_id = 1  # The mock logic in log_routes checks if ID is [1,2]

    response = client.get(f"/logs/{log_id}", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert "log" in data
    assert data["log"]["id"] == log_id


@pytest.mark.usefixtures("function_db_setup")
def test_get_log_by_id_not_found(client, user_with_token):
    """
    Test retrieving a log by an ID that does not exist in mock logic.
    """
    _, token = user_with_token
    headers = {"Authorization": f"Bearer {token}"}
    non_existent = 999

    response = client.get(f"/logs/{non_existent}", headers=headers)
    assert response.status_code == 404
    data = response.get_json()
    assert data["error_code"] == "LOG_NOT_FOUND"


def test_get_log_by_id_unauthorized(client):
    """
    Test retrieving a specific log without a valid token.
    """
    response = client.get("/logs/1")
    assert response.status_code == 401
    data = response.get_json()
    assert data["error_code"] == "AUTHENTICATION_FAILED"

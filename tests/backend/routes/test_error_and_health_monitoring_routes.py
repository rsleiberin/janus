"""
Tests for error_and_health_monitoring_routes.py
"""

import json


def test_health_check(client):
    """
    Test the /health endpoint.
    """
    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "healthy"
    assert "details" in data


def test_simulate_error_custom(client):
    """
    Test the /simulate-error endpoint with a custom error_type.
    """
    response = client.post("/simulate-error", json={"error_type": "custom"})
    assert response.status_code == 500
    data = json.loads(response.data)
    assert data["error_code"] == "SIMULATED_ERROR"
    assert "simulated custom error" in data["details"]


def test_simulate_error_db(client):
    """
    Test the /simulate-error endpoint with 'db' error_type.
    """
    response = client.post("/simulate-error", json={"error_type": "db"})
    data = response.get_json()
    assert response.status_code == 500
    assert data["error_code"] == "ROUTE_ERROR"
    assert "Simulated DB health check failure." in data["details"]


def test_simulate_generic_error(client):
    """
    Test the /simulate-error endpoint with a generic error type.
    """
    response = client.post("/simulate-error", json={"error_type": "something-else"})
    data = response.get_json()
    assert response.status_code == 500
    assert data["error_code"] == "ROUTE_ERROR"
    assert "Simulated generic error." in data["details"]


def test_unhandled_exception(client):
    """
    Test the /simulate-unhandled-error endpoint for unhandled exceptions.
    """
    response = client.get("/simulate-unhandled-error")
    data = response.get_json()
    assert response.status_code == 500
    assert data["error_code"] == "ROUTE_ERROR"
    assert data["message"] == "An error occurred while processing the request."
    assert "Simulated unhandled exception for testing." in data["details"]

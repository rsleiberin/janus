# File: backend/tests/test_error_and_health_monitoring_routes.py

from flask import json
from backend.utils.logger import CentralizedLogger

logger = CentralizedLogger("test_error_and_health_monitoring_routes")


def test_health_check(client):
    """Test the /health endpoint for a successful health check."""
    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "healthy"
    assert "details" in data
    assert data["details"]["database"] == "Available"
    assert data["details"]["service"] == "Operational"


def test_simulate_error(client):
    """Test the /simulate-error endpoint with a custom error type."""
    response = client.post("/simulate-error", json={"error_type": "custom"})
    assert response.status_code == 500
    data = json.loads(response.data)
    assert data["error_code"] == "SIMULATED_ERROR"
    assert "This is a simulated custom error." in data["details"]


def test_simulate_error_db(client):
    """Test the /simulate-error endpoint with a db error type."""
    response = client.post("/simulate-error", json={"error_type": "db"})
    assert response.status_code == 500
    data = json.loads(response.data)
    assert data["error_code"] == "ROUTE_ERROR"
    assert "Simulated database health check failure." in data["details"]


def test_simulate_generic_error(client):
    """Test the /simulate-error endpoint with a generic error type."""
    response = client.post("/simulate-error", json={"error_type": "generic"})
    assert response.status_code == 500
    data = json.loads(response.data)
    assert data["error_code"] == "ROUTE_ERROR"
    assert "Simulated generic error." in data["details"]


def test_unhandled_exception(client):
    """Test the /simulate-unhandled-error endpoint for unhandled exceptions."""
    response = client.get("/simulate-unhandled-error")
    assert response.status_code == 500

    data = json.loads(response.data)
    assert data["error_code"] == "ROUTE_ERROR"
    assert "An error occurred while processing the request." == data["message"]
    assert "Simulated unhandled exception for testing." in data["details"]

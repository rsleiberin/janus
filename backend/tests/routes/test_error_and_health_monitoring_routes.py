import pytest
from flask import json
from backend.utils.logger import CentralizedLogger

logger = CentralizedLogger("test_error_and_health_monitoring_routes")


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "healthy"
    assert "details" in data


def test_simulate_error(client):
    response = client.post("/simulate-error", json={"error_type": "custom"})
    assert response.status_code == 500
    data = json.loads(response.data)
    assert data["error_code"] == "SIMULATED_ERROR"


def test_unhandled_exception(client):
    """Test that an unhandled exception is logged and returns a 500 error."""
    response = client.get("/health/simulate-unhandled-error")
    assert response.status_code == 500

    data = json.loads(response.data)
    assert data["error_code"] == "HEALTH_CHECK_FAILED"
    assert data["message"] == "The system health check encountered an issue."

from flask import json
from backend.utils.logger import CentralizedLogger

# Initialize a logger for the test
logger = CentralizedLogger("test_analytics_routes")


def test_create_analytics_entry(client, function_db_setup):
    """Test creating a new analytics entry."""
    logger.log_to_console("INFO", "Testing create analytics entry endpoint...")

    payload = {"data": {"key": "value"}, "research_topic": "Test Topic"}

    response = client.post("/analytics", json=payload)
    assert response.status_code == 201

    data = json.loads(response.data)
    assert "id" in data
    assert data["message"] == "Analytics entry created successfully."

    logger.log_to_console("INFO", "Create analytics entry endpoint passed.")


def test_fetch_all_analytics(client, function_db_setup):
    """Test fetching all analytics entries."""
    logger.log_to_console("INFO", "Testing fetch all analytics entries endpoint...")

    # Create sample data
    sample_payload = [
        {"data": {"key1": "value1"}, "research_topic": "Topic 1"},
        {"data": {"key2": "value2"}, "research_topic": "Topic 2"},
    ]
    for payload in sample_payload:
        client.post("/analytics", json=payload)

    # Fetch all entries
    response = client.get("/analytics")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert "analytics" in data
    assert len(data["analytics"]) == 2

    logger.log_to_console("INFO", "Fetch all analytics entries endpoint passed.")


def test_fetch_single_analytics(client, function_db_setup):
    """Test fetching a single analytics entry by ID."""
    logger.log_to_console("INFO", "Testing fetch single analytics entry endpoint...")

    # Create a sample entry
    payload = {"data": {"key": "value"}, "research_topic": "Test Topic"}
    response = client.post("/analytics", json=payload)
    entry_id = json.loads(response.data)["id"]

    # Fetch the created entry
    response = client.get(f"/analytics/{entry_id}")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data["data"] == {"key": "value"}
    assert data["research_topic"] == "Test Topic"

    logger.log_to_console("INFO", "Fetch single analytics entry endpoint passed.")


def test_delete_analytics_entry(client, function_db_setup):
    """Test deleting an analytics entry by ID."""
    logger.log_to_console("INFO", "Testing delete analytics entry endpoint...")

    # Create a sample entry
    payload = {"data": {"key": "value"}, "research_topic": "Test Topic"}
    response = client.post("/analytics", json=payload)
    entry_id = json.loads(response.data)["id"]

    # Delete the created entry
    response = client.delete(f"/analytics/{entry_id}")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data["message"] == "Analytics entry deleted successfully."

    # Verify the entry is no longer accessible
    response = client.get(f"/analytics/{entry_id}")
    assert response.status_code == 404

    logger.log_to_console("INFO", "Delete analytics entry endpoint passed.")

"""
Tests for analytics_routes.py
"""

import json
import pytest


@pytest.mark.usefixtures("function_db_setup")
def test_create_analytics_entry(client):
    """
    Test creating a new analytics entry.
    """
    payload = {"data": {"key": "value"}, "research_topic": "Test Topic"}
    response = client.post("/analytics", json=payload)
    data = json.loads(response.data)

    assert response.status_code == 201
    assert "id" in data
    assert data["message"] == "Analytics entry created successfully."


@pytest.mark.usefixtures("function_db_setup")
def test_fetch_all_analytics(client):
    """
    Test fetching all analytics entries.
    """
    sample_payloads = [
        {"data": {"key1": "value1"}, "research_topic": "Topic 1"},
        {"data": {"key2": "value2"}, "research_topic": "Topic 2"},
    ]
    for pl in sample_payloads:
        client.post("/analytics", json=pl)

    response = client.get("/analytics")
    assert response.status_code == 200
    data = response.get_json()
    assert "analytics" in data
    assert len(data["analytics"]) == 2


@pytest.mark.usefixtures("function_db_setup")
def test_fetch_single_analytics(client):
    """
    Test fetching a single analytics entry by ID.
    """
    payload = {"data": {"key": "value"}, "research_topic": "Test Topic"}
    create_resp = client.post("/analytics", json=payload)
    entry_id = create_resp.get_json()["id"]

    response = client.get(f"/analytics/{entry_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["data"] == {"key": "value"}
    assert data["research_topic"] == "Test Topic"


@pytest.mark.usefixtures("function_db_setup")
def test_delete_analytics_entry(client):
    """
    Test deleting an analytics entry by ID.
    """
    payload = {"data": {"key": "value"}, "research_topic": "Test Topic"}
    create_resp = client.post("/analytics", json=payload)
    entry_id = create_resp.get_json()["id"]

    response = client.delete(f"/analytics/{entry_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Analytics entry deleted successfully."

    fetch_resp = client.get(f"/analytics/{entry_id}")
    assert fetch_resp.status_code == 404

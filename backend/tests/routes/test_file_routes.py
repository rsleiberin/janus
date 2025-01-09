import pytest
from unittest.mock import patch

@pytest.mark.usefixtures("client")
def test_files_endpoint(client):
    """
    Test the /files endpoint.
    """
    with patch("os.walk") as mock_os_walk:
        mock_os_walk.return_value = [
            ("/home/tank/janus", ["subdir"], ["file1.txt", "file2.txt"])
        ]

        response = client.get("/files")
        data = response.get_json()

        assert response.status_code == 200
        assert "files" in data
        assert data["files"] == [
            "/home/tank/janus/file1.txt",
            "/home/tank/janus/file2.txt",
        ]

@pytest.mark.usefixtures("client")
@patch("os.path.abspath")
def test_files_content_endpoint_invalid_path(mock_abspath, client):
    """
    Test the /files/content endpoint with an invalid file path.
    """
    invalid_file_path = "../outside_path.txt"
    mock_abspath.return_value = "/home/tank/outside_path.txt"

    response = client.post(
        "/files/content", json={"path": invalid_file_path}
    )
    data = response.get_json()

    assert response.status_code == 403
    assert data["error_code"] == "FILE_ACCESS_DENIED"
    assert data["message"] == "Access denied to the requested file."

@pytest.mark.usefixtures("client")
@patch("builtins.open", side_effect=FileNotFoundError)
def test_files_content_endpoint_nonexistent_file(mock_open_func, client):
    """
    Test the /files/content endpoint with a non-existent file.
    """
    nonexistent_file_path = "non_existent_file.txt"

    response = client.post(
        "/files/content", json={"path": nonexistent_file_path}
    )
    data = response.get_json()

    assert response.status_code == 404
    assert data["error_code"] == "FILE_NOT_FOUND"
    assert data["message"] == "The requested file was not found."

@pytest.mark.usefixtures("client")
@patch("builtins.open", side_effect=Exception("Mock unexpected error"))
def test_files_content_endpoint_unexpected_error(mock_open_func, client):
    """
    Test the /files/content endpoint for unexpected errors.
    """
    file_path = "README.md"

    response = client.post(
        "/files/content", json={"path": file_path}
    )
    data = response.get_json()

    assert response.status_code == 500
    assert data["error_code"] == "UNKNOWN_ROUTE_ERROR"
    assert data["message"] == "An unknown error occurred in the route."

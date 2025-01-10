import pytest
from unittest.mock import patch

@pytest.mark.usefixtures("client")
def test_files_endpoint(client, mocker):
    with patch("os.walk") as mock_os_walk:
        mock_os_walk.return_value = [
            ("/home/tank/janus", ["subdir"], ["file1.txt", "file2.txt"])
        ]

        mock_logger = mocker.patch("backend.routes.file_routes.logger.log_to_console")

        response = client.get("/files")
        data = response.get_json()

        assert response.status_code == 200
        assert data["files"] == ["/home/tank/janus/file1.txt", "/home/tank/janus/file2.txt"]

        mock_logger.assert_called_once_with("INFO", "Listed all files in the directory.")

@pytest.mark.usefixtures("client")
@patch("os.path.abspath")
def test_files_content_endpoint_invalid_path(mock_abspath, client, mocker):
    invalid_file_path = "../outside_path.txt"
    mock_abspath.return_value = "/home/tank/outside_path.txt"

    mock_logger = mocker.patch("backend.routes.file_routes.logger.log_to_console")

    response = client.post("/files/content", json={"path": invalid_file_path})
    data = response.get_json()

    assert response.status_code == 403
    assert data["error_code"] == "FILE_ACCESS_DENIED"

    mock_logger.assert_called_once_with(
        "ERROR", "File access error", exc_info=mocker.ANY
    )

@pytest.mark.usefixtures("client")
@patch("builtins.open", side_effect=FileNotFoundError)
def test_files_content_endpoint_nonexistent_file(mock_open_func, client, mocker):
    nonexistent_file_path = "non_existent_file.txt"

    mock_logger = mocker.patch("backend.routes.file_routes.logger.log_to_console")

    response = client.post("/files/content", json={"path": nonexistent_file_path})
    data = response.get_json()

    assert response.status_code == 404
    assert data["error_code"] == "FILE_NOT_FOUND"

    mock_logger.assert_called_once_with("WARNING", f"File not found: {nonexistent_file_path}")

@pytest.mark.usefixtures("client")
@patch("builtins.open", side_effect=Exception("Mock unexpected error"))
def test_files_content_endpoint_unexpected_error(mock_open_func, client, mocker):
    file_path = "README.md"

    mock_logger = mocker.patch("backend.routes.file_routes.logger.log_to_console")

    response = client.post("/files/content", json={"path": file_path})
    data = response.get_json()

    assert response.status_code == 500
    assert data["error_code"] == "UNKNOWN_ROUTE_ERROR"

    mock_logger.assert_called_once_with(
        "ERROR", "Unexpected error reading file", exc_info=mocker.ANY
    )

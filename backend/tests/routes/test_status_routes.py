from sqlalchemy.exc import OperationalError


def test_health_check_success(client, mocker):
    """
    Test the /status endpoint when the database is connected successfully.
    """
    mock_session = mocker.patch("backend.db.session.execute")
    mock_session.return_value = None

    mock_logger = mocker.patch("backend.routes.status_routes.logger.log_to_console")

    response = client.get("/status")
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "ok"
    assert data["database"] == "connected"

    mock_logger.assert_called_once_with(
        "INFO", "Health check passed: Database connected."
    )


def test_health_check_database_error(client, mocker):
    """
    Test the /status endpoint when the database connection fails.
    """
    mock_session = mocker.patch("backend.db.session.execute")
    mock_session.side_effect = OperationalError("Mocked database error", {}, None)

    mock_logger = mocker.patch("backend.routes.status_routes.logger.log_to_console")

    response = client.get("/status")
    data = response.get_json()

    assert response.status_code == 500
    assert data["error_code"] == "DATABASE_UNAVAILABLE"
    assert data["message"] == "The database is not accessible at this time."

    mock_logger.assert_any_call(
        "ERROR", "Database connection failed.", exc_info=mocker.ANY
    )

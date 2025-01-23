import pytest
from backend.db import db
from unittest.mock import patch
from backend.models import Log
from backend.db.helpers.log_helpers import LogHelpers
from backend.utils.error_handling.exceptions import LogNotFoundError


@pytest.mark.usefixtures("function_db_setup")
def test_create_log():
    """
    Test creating a log entry.
    """
    with patch(
        "backend.utils.logger.CentralizedLogger.log_to_console"
    ) as mock_console_log:
        log = LogHelpers.create_log(
            action="Test Create",
            user_id=1,
            module="test_module",
            level="INFO",
            meta_data={"key": "value"},
        )
        assert log is not None, "Failed to create log."

        mock_console_log.assert_any_call(
            "INFO", f"Log entry created successfully with ID {log.id}.", meta_data={"key": "value"}
        )

@pytest.mark.usefixtures("function_db_setup")
def test_get_by_id():
    """
    Test retrieving a log by its ID.
    """
    log = LogHelpers.create_log(action="Test Fetch by ID", user_id=1)

    with patch("backend.utils.logger.CentralizedLogger.log_to_console") as mock_log:
        fetched_log = LogHelpers.get_by_id(log.id)
        mock_log.assert_called_with(
            "INFO",
            f"Retrieved log by ID: {log.id}.",
        )
        assert fetched_log.id == log.id, "Log ID mismatch."


@pytest.mark.usefixtures("function_db_setup")
def test_delete_log():
    """
    Test deleting a log.
    """
    log = LogHelpers.create_log(action="Test Delete", user_id=1)
    assert LogHelpers.delete_log(log.id), "Failed to delete log."

    # Test deletion of nonexistent log
    with pytest.raises(LogNotFoundError, match="Requested log entry was not found."):
        LogHelpers.delete_log(9999)


@pytest.mark.usefixtures("function_db_setup")
def test_get_by_user_id():
    """
    Test retrieving logs by user ID.
    """
    LogHelpers.create_log(action="Action 1", user_id=1)
    LogHelpers.create_log(action="Action 2", user_id=1)
    logs = LogHelpers.get_by_user_id(1)
    assert len(logs) == 2, "Expected 2 logs for user ID 1."
    assert logs[0].user_id == 1, "User ID mismatch."


@pytest.mark.usefixtures("function_db_setup")
def test_get_by_module():
    """
    Test retrieving logs by module.
    """
    LogHelpers.create_log(action="Action A", user_id=1, module="module1")
    LogHelpers.create_log(action="Action B", user_id=2, module="module1")
    logs = LogHelpers.get_by_module("module1")
    assert len(logs) == 2, "Expected 2 logs for module1."


@pytest.mark.usefixtures("function_db_setup")
def test_get_by_level():
    """
    Test retrieving logs by log level.
    """
    LogHelpers.create_log(action="Debug Log", user_id=1, level="DEBUG")
    LogHelpers.create_log(action="Info Log", user_id=2, level="INFO")
    logs = LogHelpers.get_by_level("DEBUG")
    assert len(logs) == 1, "Expected 1 debug log."


@pytest.mark.usefixtures("function_db_setup")
def test_get_recent_logs():
    """
    Test retrieving recent logs.
    """
    for i in range(5):
        LogHelpers.create_log(action=f"Recent {i}", user_id=1)
    recent_logs = LogHelpers.get_recent_logs(limit=3)
    assert len(recent_logs) == 3, "Expected 3 recent logs."

@pytest.mark.usefixtures("function_db_setup")
def test_count_logs(app):
    """
    Test counting logs.
    """
    with app.app_context():  # Ensure the app context is active
        # Explicitly clear all logs to start clean
        db.session.query(Log).delete()
        db.session.commit()

        # Verify database starts empty
        count_before = LogHelpers.count()
        assert count_before == 0, f"Expected log count to be 0, found {count_before}"

        # Create new logs
        LogHelpers.create_log(action="Log 1", user_id=1)
        LogHelpers.create_log(action="Log 2", user_id=2)

        # Verify count after creation
        count_after = LogHelpers.count()
        assert count_after == 2, f"Expected log count to be 2, found {count_after}"


@pytest.mark.usefixtures("function_db_setup")
def test_exists_logs():
    """
    Test checking if a log exists.
    """
    LogHelpers.create_log(action="Check Exists", user_id=1)
    assert LogHelpers.exists(action="Check Exists"), "Expected log to exist."
    assert not LogHelpers.exists(action="Nonexistent"), "Log should not exist."


@pytest.mark.usefixtures("function_db_setup")
def test_logs_with_metadata_key():
    """
    Test retrieving logs with a specific metadata key.
    """
    LogHelpers.create_log(
        action="Meta Key Test", user_id=1, meta_data={"key1": "value1"}
    )
    logs = LogHelpers.get_logs_with_metadata_key("key1")
    assert len(logs) == 1, "Expected 1 log with metadata key 'key1'."


@pytest.mark.usefixtures("function_db_setup")
def test_logs_with_metadata_value():
    """
    Test retrieving logs with a specific metadata key-value pair.
    """
    LogHelpers.create_log(
        action="Meta Value Test", user_id=1, meta_data={"key1": "value1"}
    )

    # Valid retrieval
    logs = LogHelpers.get_logs_with_metadata_value("key1", "value1")
    assert (
        len(logs) == 1
    ), f"Expected 1 log with metadata value 'value1', found {len(logs)}."

    # Invalid retrieval
    logs = LogHelpers.get_logs_with_metadata_value("key1", "nonexistent_value")
    assert len(logs) == 0, "Expected 0 logs for nonexistent metadata value."

import pytest
from backend.db import db
from backend.db.helpers.log_helpers import LogHelpers
from backend.models import Log
from backend.utils.logger import CentralizedLogger
from sqlalchemy.sql import text
from datetime import datetime

# Initialize the centralized logger for testing
logger = CentralizedLogger("test_logger")

@pytest.mark.usefixtures("function_db_setup")
def test_create_log():
    """
    Test creating a log entry in the database.
    """
    logger.log_to_console("DEBUG", "Starting test_create_log...")
    new_log = LogHelpers.create_log(
        action="Test Action",
        user_id=1,
        module="TestModule",
        level="INFO",
        meta_data={"key": "value"}
    )
    assert new_log is not None, "Log entry creation failed."
    assert new_log.action == "Test Action", "Log action mismatch."
    assert new_log.user_id == 1, "Log user_id mismatch."
    assert new_log.module == "TestModule", "Log module mismatch."
    assert new_log.level == "INFO", "Log level mismatch."
    assert new_log.meta_data == {"key": "value"}, "Log metadata mismatch."
    logger.log_to_console("DEBUG", "test_create_log passed successfully.")

@pytest.mark.usefixtures("function_db_setup")
def test_get_by_id():
    """
    Test retrieving a log entry by its ID.
    """
    logger.log_to_console("DEBUG", "Starting test_get_by_id...")
    created_log = LogHelpers.create_log(action="Lookup Action", user_id=1)
    fetched_log = LogHelpers.get_by_id(created_log.id)

    assert fetched_log is not None, "Fetched log is None."
    assert fetched_log.id == created_log.id, "Fetched ID does not match created log."
    assert fetched_log.action == "Lookup Action", "Fetched action mismatch."
    logger.log_to_console("DEBUG", "test_get_by_id passed successfully.")

@pytest.mark.usefixtures("function_db_setup")
def test_get_by_user_id():
    """
    Test retrieving log entries by user ID.
    """
    logger.log_to_console("DEBUG", "Starting test_get_by_user_id...")
    LogHelpers.create_log(action="Action 1", user_id=1)
    LogHelpers.create_log(action="Action 2", user_id=1)

    logs = LogHelpers.get_by_user_id(1)
    assert len(logs) == 2, f"Expected 2 logs, found {len(logs)}."
    logger.log_to_console("DEBUG", "test_get_by_user_id passed successfully.")

@pytest.mark.usefixtures("function_db_setup")
def test_get_by_module():
    """
    Test retrieving log entries by module name.
    """
    logger.log_to_console("DEBUG", "Starting test_get_by_module...")
    LogHelpers.create_log(action="Module Action 1", user_id=1, module="ModuleA")
    LogHelpers.create_log(action="Module Action 2", user_id=2, module="ModuleA")

    logs = LogHelpers.get_by_module("ModuleA")
    assert len(logs) == 2, f"Expected 2 logs, found {len(logs)}."
    logger.log_to_console("DEBUG", "test_get_by_module passed successfully.")

@pytest.mark.usefixtures("function_db_setup")
def test_get_by_level():
    """
    Test retrieving log entries by log level.
    """
    logger.log_to_console("DEBUG", "Starting test_get_by_level...")
    LogHelpers.create_log(action="Level Action 1", user_id=1, level="DEBUG")
    LogHelpers.create_log(action="Level Action 2", user_id=2, level="DEBUG")

    logs = LogHelpers.get_by_level("DEBUG")
    assert len(logs) == 2, f"Expected 2 logs, found {len(logs)}."
    logger.log_to_console("DEBUG", "test_get_by_level passed successfully.")

@pytest.mark.usefixtures("function_db_setup")
def test_get_recent_logs():
    """
    Test retrieving recent log entries.
    """
    logger.log_to_console("DEBUG", "Starting test_get_recent_logs...")
    for i in range(5):
        LogHelpers.create_log(action=f"Recent Log {i}", user_id=1)

    recent_logs = LogHelpers.get_recent_logs(limit=3)
    assert len(recent_logs) == 3, f"Expected 3 logs, found {len(recent_logs)}."
    logger.log_to_console("DEBUG", "test_get_recent_logs passed successfully.")

@pytest.mark.usefixtures("function_db_setup")
def test_delete_log():
    """
    Test deleting a log entry.
    """
    logger.log_to_console("DEBUG", "Starting test_delete_log...")
    created_log = LogHelpers.create_log(action="Delete Action", user_id=1)
    LogHelpers.delete_log(created_log.id)

    fetched_log = LogHelpers.get_by_id(created_log.id)
    assert fetched_log is None, "Log was not deleted."
    logger.log_to_console("DEBUG", "test_delete_log passed successfully.")

@pytest.mark.usefixtures("function_db_setup")
def test_count_logs():
    """
    Test the count helper to ensure it returns the correct number of logs.
    """
    logger.log_to_console("DEBUG", "Starting test_count_logs...")

    # Insert logs directly
    insert_query = text("""
        INSERT INTO logs (action, user_id, meta_data, level, timestamp, module)
        VALUES
        ('Action 1', 1, '{"key": "value1"}', 'INFO', :timestamp, NULL),
        ('Action 2', 1, '{"key": "value2"}', 'DEBUG', :timestamp, NULL)
    """)
    db.session.execute(insert_query, {"timestamp": datetime.utcnow()})
    db.session.commit()

    # Use the helper
    count = LogHelpers.count()
    assert count == 2, f"Expected 2 logs, found {count}."
    logger.log_to_console("DEBUG", "test_count_logs passed successfully.")

@pytest.mark.usefixtures("function_db_setup")
def test_exists_logs():
    """
    Test the exists helper to ensure it correctly identifies log presence.
    """
    logger.log_to_console("DEBUG", "Starting test_exists_logs...")

    # Insert a log directly
    insert_query = text("""
        INSERT INTO logs (action, user_id, meta_data, level, timestamp, module)
        VALUES
        ('Exists Test Action', 1, '{"key": "value"}', 'INFO', :timestamp, NULL)
    """)
    db.session.execute(insert_query, {"timestamp": datetime.utcnow()})
    db.session.commit()

    # Use the helper
    exists = LogHelpers.exists(action="Exists Test Action")
    assert exists, "Log with action 'Exists Test Action' should exist."
    logger.log_to_console("DEBUG", "test_exists_logs passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_logs_with_metadata_key():
    """
    Test retrieving logs with a specific metadata key.
    """
    logger.log_to_console("DEBUG", "Starting test_logs_with_metadata_key...")

    # Insert logs directly into the database
    insert_query = text("""
        INSERT INTO logs (action, user_id, meta_data, level, timestamp, module)
        VALUES
        ('Meta Action 1', 1, '{"key1": "value1"}', 'INFO', :timestamp, NULL),
        ('Meta Action 2', 1, '{"key2": "value2"}', 'INFO', :timestamp, NULL)
    """)
    db.session.execute(insert_query, {"timestamp": datetime.utcnow()})
    db.session.commit()

    # Use the helper method to retrieve logs with metadata key
    logs = LogHelpers.get_logs_with_metadata_key("key1")

    # Assertions
    assert len(logs) == 1, f"Expected 1 log, found {len(logs)}."
    assert logs[0].meta_data["key1"] == "value1", "Metadata key1 value mismatch."
    logger.log_to_console("DEBUG", "test_logs_with_metadata_key passed successfully.")

@staticmethod
def get_logs_with_metadata_value(key, value):
    """
    Retrieve logs with a specific metadata key-value pair.

    Args:
        key (str): The metadata key.
        value (str): The metadata value.

    Returns:
        list[Log]: A list of log entries matching the key-value pair.
    """
    try:
        logs = Log.query.filter(
            Log.meta_data.op("->>")(key) == value
        ).all()
        logger.log_to_console(
            "DEBUG",
            "Retrieved logs by metadata value",
            key=key,
            value=value,
            count=len(logs),
        )
        return logs
    except Exception as e:
        logger.log_to_console(
            "ERROR",
            "Failed to retrieve logs by metadata value",
            key=key,
            value=value,
            error=str(e),
        )
        return []

# test_log_helpers.py

import pytest
import logging
from backend.db import db
from backend.db.helpers.log_helpers import LogHelpers

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("test_logger")


@pytest.mark.usefixtures("function_db_setup")
def test_create_log():
    logger.debug("Starting test_create_log...")
    new_log = LogHelpers.create_log("Test Action", user_id=1, module="TestModule", level="INFO", meta_data={"key": "value"})
    assert new_log.id is not None, "Log entry was not assigned an ID."
    assert new_log.action == "Test Action", "Log action does not match expected."
    assert new_log.user_id == 1, "Log user_id does not match expected."
    assert new_log.module == "TestModule", "Log module does not match expected."
    assert new_log.level == "INFO", "Log level does not match expected."
    assert new_log.meta_data == {"key": "value"}, "Log metadata does not match expected."
    logger.debug("test_create_log passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_get_by_id():
    logger.debug("Starting test_get_by_id...")
    created_log = LogHelpers.create_log("Lookup Action", user_id=2)
    db.session.flush()

    fetched_log = LogHelpers.get_by_id(created_log.id)
    assert fetched_log is not None, "Fetched log is None."
    assert fetched_log.id == created_log.id, "Fetched ID does not match created log."
    logger.debug("test_get_by_id passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_get_by_user_id():
    logger.debug("Starting test_get_by_user_id...")
    user_id = 3
    LogHelpers.create_log("Action 1", user_id=user_id)
    LogHelpers.create_log("Action 2", user_id=user_id)

    logs_for_user = LogHelpers.get_by_user_id(user_id)
    assert len(logs_for_user) == 2, f"Expected 2 logs for user {user_id}, got {len(logs_for_user)}."
    logger.debug("test_get_by_user_id passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_get_by_module():
    logger.debug("Starting test_get_by_module...")
    LogHelpers.create_log("Module Action 1", user_id=4, module="ModuleA")
    LogHelpers.create_log("Module Action 2", user_id=5, module="ModuleA")

    logs_for_module = LogHelpers.get_by_module("ModuleA")
    assert len(logs_for_module) == 2, f"Expected 2 logs for module 'ModuleA', got {len(logs_for_module)}."
    logger.debug("test_get_by_module passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_get_by_level():
    logger.debug("Starting test_get_by_level...")
    LogHelpers.create_log("Level Action 1", user_id=6, level="DEBUG")
    LogHelpers.create_log("Level Action 2", user_id=7, level="DEBUG")

    logs_for_level = LogHelpers.get_by_level("DEBUG")
    assert len(logs_for_level) == 2, f"Expected 2 logs for level 'DEBUG', got {len(logs_for_level)}."
    logger.debug("test_get_by_level passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_get_recent_logs():
    logger.debug("Starting test_get_recent_logs...")

    # Create multiple logs
    for i in range(5):
        LogHelpers.create_log(f"Recent Log {i}", user_id=4)

    # Retrieve the 3 most recent
    recent_logs = LogHelpers.get_recent_logs(limit=3)
    assert len(recent_logs) == 3, f"Expected 3 recent logs, got {len(recent_logs)}."
    logger.debug("test_get_recent_logs passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_get_logs_with_metadata_key():
    logger.debug("Starting test_get_logs_with_metadata_key...")
    LogHelpers.create_log("Action 1", user_id=8, meta_data={"key1": "value1"})
    LogHelpers.create_log("Action 2", user_id=9, meta_data={"key2": "value2"})

    logs_with_key = LogHelpers.get_logs_with_metadata_key("key1")
    assert len(logs_with_key) == 1, f"Expected 1 log with key 'key1', got {len(logs_with_key)}."
    logger.debug("test_get_logs_with_metadata_key passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_get_logs_by_metadata_value():
    logger.debug("Starting test_get_logs_by_metadata_value...")
    LogHelpers.create_log("Action 1", user_id=10, meta_data={"key": "value"})
    LogHelpers.create_log("Action 2", user_id=11, meta_data={"key": "other_value"})

    logs_with_value = LogHelpers.get_logs_by_metadata_value("key", "value")
    assert len(logs_with_value) == 1, f"Expected 1 log with 'key=value', got {len(logs_with_value)}."
    logger.debug("test_get_logs_by_metadata_value passed successfully.")


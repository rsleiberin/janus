# test_log_helpers.py

import pytest
import logging
from backend.db import db
from backend.db.helpers.log_helpers import LogHelpers
from backend.models import Log

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("test_logger")


@pytest.mark.usefixtures("function_db_setup")
def test_create_log():
    logger.debug("Starting test_create_log...")
    new_log = LogHelpers.create_log("Test Action", user_id=1)
    assert new_log.id is not None, "Log entry was not assigned an ID."
    assert new_log.action == "Test Action", "Log action does not match expected."
    assert new_log.user_id == 1, "Log user_id does not match expected."
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
def test_delete_log():
    logger.debug("Starting test_delete_log...")
    log_entry = LogHelpers.create_log("Delete Action", user_id=5)
    log_id = log_entry.id

    LogHelpers.delete_log(log_id)

    deleted_log = LogHelpers.get_by_id(log_id)
    assert deleted_log is None, "Log entry still exists after delete_log was called."
    logger.debug("test_delete_log passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_count_logs():
    logger.debug("Starting test_count_logs...")
    LogHelpers.create_log("Count Log 1", user_id=6)
    LogHelpers.create_log("Count Log 2", user_id=6)

    total_logs = LogHelpers.count()
    assert total_logs == 2, f"Expected 2 logs in total, found {total_logs}."
    logger.debug("test_count_logs passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_exists_log():
    logger.debug("Starting test_exists_log...")
    new_log = LogHelpers.create_log("Exist Check", user_id=7)
    assert LogHelpers.exists(new_log.id) is True, "Expected the new log to exist."
    logger.debug("test_exists_log passed successfully.")

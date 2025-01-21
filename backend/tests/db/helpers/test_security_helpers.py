import pytest
from backend.db import db
from backend.db.helpers.security_helpers import SecurityHelpers
from backend.utils.logger import CentralizedLogger
from backend.models import Security

logger = CentralizedLogger("test_security_helpers")


@pytest.mark.usefixtures("function_db_setup")
def test_create_security_entry():
    user_id = 1
    action = "login_attempt"

    security_entry = SecurityHelpers.create_security_entry(user_id, action)
    assert security_entry.id is not None
    assert security_entry.user_id == user_id
    assert security_entry.action == action


@pytest.mark.usefixtures("function_db_setup")
def test_get_security_by_id():
    user_id = 1
    action = "login_attempt"

    security_entry = SecurityHelpers.create_security_entry(user_id, action)
    fetched_entry = SecurityHelpers.get_security_by_id(security_entry.id)
    assert fetched_entry.id == security_entry.id


@pytest.mark.usefixtures("function_db_setup")
def test_get_security_by_user():
    user_id = 1
    SecurityHelpers.create_security_entry(user_id, "login_attempt")
    SecurityHelpers.create_security_entry(user_id, "password_change")

    entries = SecurityHelpers.get_security_by_user(user_id)
    assert len(entries) == 2


@pytest.mark.usefixtures("function_db_setup")
def test_delete_security_entry():
    user_id = 1
    action = "login_attempt"

    security_entry = SecurityHelpers.create_security_entry(user_id, action)
    SecurityHelpers.delete_security_entry(security_entry.id)

    assert not SecurityHelpers.exists(security_entry.id)

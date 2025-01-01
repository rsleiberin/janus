# test_admin_helpers.py

import pytest
import logging
from backend.db import db
from backend.models import Admin  # Only import Admin for this test
from backend.db.helpers import AdminHelpers

# Configure console logging for test suite
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("test_logger")


@pytest.mark.usefixtures("function_db_setup")
def test_create_admin():
    """
    Tests the creation of an Admin record using AdminHelpers.create.
    Relies on function_db_setup to handle app context + DB reset.
    """
    logger.debug("Starting test_create_admin...")

    admin_data = {
        "user_id": 1,
        "admin_level": "superadmin"
    }

    # Create admin (AdminHelpers.create commits automatically)
    admin = AdminHelpers.create(admin_data)
    logger.debug("[CREATE_ADMIN] Admin created: %s", admin)

    # Assertions
    assert admin.id is not None, "Admin was not assigned an ID."
    assert admin.admin_level == "superadmin", "Admin level not set correctly."
    logger.debug("test_create_admin passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_get_by_id():
    """
    Tests retrieval of an Admin record by ID using AdminHelpers.get_by_id.
    """
    logger.debug("Starting test_get_by_id...")

    admin_data = {
        "user_id": 1,
        "admin_level": "superadmin"
    }

    # Create admin
    admin = AdminHelpers.create(admin_data)
    # Flush the session to ensure the new admin is written
    db.session.flush()

    # Fetch the newly created admin
    fetched_admin = AdminHelpers.get_by_id(admin.id)
    logger.debug("[GET_BY_ID] Fetched admin: %s", fetched_admin)

    # Assertions
    assert fetched_admin is not None, "Fetched admin is None, expected a valid record."
    assert fetched_admin.id == admin.id, "Fetched admin ID does not match created admin."
    logger.debug("test_get_by_id passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_update_admin():
    """
    Tests updating an Admin record using AdminHelpers.update.
    """
    logger.debug("Starting test_update_admin...")

    admin_data = {
        "user_id": 1,
        "admin_level": "superadmin"
    }
    updated_data = {"admin_level": "moderator"}

    # Create admin
    admin = AdminHelpers.create(admin_data)
    # Update the existing admin
    updated_admin = AdminHelpers.update(admin.id, updated_data)
    logger.debug("[UPDATE_ADMIN] Updated admin: %s", updated_admin)

    # Assertions
    assert updated_admin.admin_level == "moderator", "Admin level did not update correctly."
    logger.debug("test_update_admin passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_delete_admin():
    """
    Tests deleting an Admin record using AdminHelpers.delete.
    """
    logger.debug("Starting test_delete_admin...")

    admin_data = {
        "user_id": 1,
        "admin_level": "superadmin"
    }

    # Create admin
    admin = AdminHelpers.create(admin_data)
    logger.debug("[DELETE_ADMIN] Created admin: %s", admin)

    # Delete admin
    AdminHelpers.delete(admin.id)
    logger.debug("[DELETE_ADMIN] Admin deleted.")

    # Verify deletion
    deleted_admin = Admin.query.get(admin.id)
    logger.debug("[DELETE_ADMIN] Deleted admin: %s", deleted_admin)

    assert deleted_admin is None, "Admin record still present after deletion."
    logger.debug("test_delete_admin passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_count_admins():
    """
    Tests counting the total number of Admin records using AdminHelpers.count.
    """
    logger.debug("Starting test_count_admins...")

    admin_data_1 = {"user_id": 1, "admin_level": "superadmin"}
    admin_data_2 = {"user_id": 2, "admin_level": "moderator"}

    # Create two admins
    AdminHelpers.create(admin_data_1)
    AdminHelpers.create(admin_data_2)

    # Count them
    admin_count = AdminHelpers.count()
    logger.debug("[COUNT_ADMINS] Admin count: %d", admin_count)

    # Assertions
    assert admin_count == 2, f"Expected 2 admins, found {admin_count}"
    logger.debug("test_count_admins passed successfully.")


@pytest.mark.usefixtures("function_db_setup")
def test_exists_admin():
    """
    Tests checking the existence of an Admin record by ID using AdminHelpers.exists.
    """
    logger.debug("Starting test_exists_admin...")

    admin_data = {
        "user_id": 1,
        "admin_level": "superadmin"
    }

    # Create admin
    admin = AdminHelpers.create(admin_data)
    admin_exists = AdminHelpers.exists(admin.id)
    logger.debug("[EXISTS_ADMIN] Admin exists result: %s", admin_exists)

    # Assertions
    assert admin_exists is True, "Expected admin to exist, but got False."
    logger.debug("test_exists_admin passed successfully.")

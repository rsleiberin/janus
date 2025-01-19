import pytest
from unittest.mock import patch
from backend.db import db
from backend.models import Admin
from backend.db.helpers.admin_helpers import AdminHelpers


@pytest.mark.usefixtures("function_db_setup")
def test_create_admin():
    """
    Tests the creation of an Admin record using AdminHelpers.create
    and verifies the associated logging.
    """
    admin_data = {"user_id": 1, "admin_level": "superadmin"}

    with patch(
        "backend.utils.logger.CentralizedLogger.log_to_console"
    ) as mock_console_log, patch(
        "backend.utils.logger.CentralizedLogger.log_to_db"
    ) as mock_db_log:
        # Create admin
        admin = AdminHelpers.create(admin_data)

        # Verify admin creation
        assert admin is not None, "Admin creation failed."
        assert admin.user_id == admin_data["user_id"], "Admin user_id mismatch."
        assert admin.admin_level == admin_data["admin_level"], "Admin level mismatch."

        # Verify logging
        mock_console_log.assert_called_with(
            "INFO", "Admin created successfully.", admin_data=admin_data
        )
        mock_db_log.assert_called_with(
            "INFO",
            "Admin created.",
            module="admin_helpers",
            meta_data={"admin_data": admin_data},
        )


@pytest.mark.usefixtures("function_db_setup")
def test_get_by_id():
    """
    Tests retrieval of an Admin record by ID using AdminHelpers.get_by_id
    and verifies the associated logging.
    """
    admin_data = {"user_id": 1, "admin_level": "superadmin"}
    admin = AdminHelpers.create(admin_data)

    with patch(
        "backend.utils.logger.CentralizedLogger.log_to_console"
    ) as mock_console_log:
        fetched_admin = AdminHelpers.get_by_id(admin.id)

        # Verify admin retrieval
        assert fetched_admin is not None, "Admin not found by ID."
        assert fetched_admin.id == admin.id, "Admin ID mismatch."

        # Verify logging
        mock_console_log.assert_any_call("INFO", f"Fetched admin by ID: {admin.id}")


@pytest.mark.usefixtures("function_db_setup")
def test_delete_admin():
    """
    Tests deleting an Admin record using AdminHelpers.delete
    and verifies the associated logging.
    """
    admin_data = {"user_id": 1, "admin_level": "superadmin"}
    admin = AdminHelpers.create(admin_data)

    with patch(
        "backend.utils.logger.CentralizedLogger.log_to_console"
    ) as mock_console_log, patch(
        "backend.utils.logger.CentralizedLogger.log_to_db"
    ) as mock_db_log:
        AdminHelpers.delete(admin.id)

        # Verify deletion
        deleted_admin = db.session.get(Admin, admin.id)
        assert deleted_admin is None, "Admin was not deleted."

        # Verify logging
        mock_console_log.assert_called_with(
            "INFO", f"Admin {admin.id} deleted successfully."
        )
        mock_db_log.assert_called_with(
            "INFO",
            "Admin deleted.",
            module="admin_helpers",
            meta_data={"admin_id": admin.id},
        )


@pytest.mark.usefixtures("function_db_setup")
def test_exists_admin():
    """
    Tests checking the existence of an Admin record by ID using AdminHelpers.exists
    and verifies the associated logging.
    """
    admin_data = {"user_id": 1, "admin_level": "superadmin"}
    admin = AdminHelpers.create(admin_data)

    with patch(
        "backend.utils.logger.CentralizedLogger.log_to_console"
    ) as mock_console_log:
        admin_exists = AdminHelpers.exists(admin.id)

        # Verify existence check
        assert admin_exists is True, "Admin existence check failed."

        # Verify logging includes the result
        mock_console_log.assert_called_with(
            "INFO", f"Admin existence check for ID {admin.id}: {admin_exists}"
        )

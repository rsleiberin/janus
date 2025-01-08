from backend.db import db
from backend.models import Admin
from flask import current_app  # To get the current app context
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.db.errors import (
    AdminNotFoundError,
    AdminCreationError,
    AdminUpdateError,
    handle_database_error,
)

# Initialize the logger
logger = CentralizedLogger(name="admin_helpers")

class AdminHelpers:
    @staticmethod
    def create(admin_data):
        """Create a new admin record, linking it to a user."""
        try:
            admin = Admin(**admin_data)
            db.session.add(admin)
            db.session.commit()
            logger.log_to_console(
                "INFO",
                "Admin created successfully.",
                admin_data=admin_data
            )
            logger.log_to_db(
                "INFO",
                "Admin created.",
                module="admin_helpers",
                meta_data={"admin_data": admin_data}
            )
            return admin
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to create admin.", exception=e)
            logger.log_to_db("ERROR", "Admin creation failed.", module="admin_helpers", meta_data={"error": str(e)})
            raise AdminCreationError("Failed to create admin record.") from e

    @staticmethod
    def get_by_id(admin_id):
        """Get an admin by their ID."""
        try:
            with current_app.app_context():
                admin = db.session.get(Admin, admin_id)
                if not admin:
                    raise AdminNotFoundError(f"Admin with ID {admin_id} not found.")
                logger.log_to_console("INFO", f"Fetched admin by ID: {admin_id}")
                return admin
        except Exception as e:
            logger.log_to_console("ERROR", "Error fetching admin by ID.", exception=e)
            raise handle_database_error(e, module="admin_helpers", meta_data={"admin_id": admin_id})

    @staticmethod
    def get_by_user_id(user_id):
        """Get an admin by the associated user's ID."""
        try:
            admin = db.session.query(Admin).filter_by(user_id=user_id).first()
            if not admin:
                raise AdminNotFoundError(f"Admin for user ID {user_id} not found.")
            logger.log_to_console("INFO", f"Fetched admin by user ID: {user_id}")
            return admin
        except Exception as e:
            logger.log_to_console("ERROR", "Error fetching admin by user ID.", exception=e)
            raise handle_database_error(e, module="admin_helpers", meta_data={"user_id": user_id})

    @staticmethod
    def update(admin_id, updated_data):
        """Update an existing admin record."""
        try:
            admin = db.session.get(Admin, admin_id)
            if admin:
                for key, value in updated_data.items():
                    setattr(admin, key, value)
                db.session.commit()
                logger.log_to_console(
                    "INFO",
                    f"Admin {admin_id} updated successfully.",
                    updated_data=updated_data
                )
                logger.log_to_db(
                    "INFO",
                    "Admin updated.",
                    module="admin_helpers",
                    meta_data={"admin_id": admin_id, "updated_data": updated_data}
                )
                return admin
            else:
                raise AdminNotFoundError(f"Admin with ID {admin_id} not found.")
        except Exception as e:
            logger.log_to_console("ERROR", f"Failed to update admin {admin_id}.", exception=e)
            raise AdminUpdateError("Failed to update admin record.") from e

    @staticmethod
    def delete(admin_id):
        """Delete an admin by their ID."""
        try:
            admin = db.session.get(Admin, admin_id)
            if admin:
                db.session.delete(admin)
                db.session.commit()
                logger.log_to_console("INFO", f"Admin {admin_id} deleted successfully.")
                logger.log_to_db(
                    "INFO",
                    "Admin deleted.",
                    module="admin_helpers",
                    meta_data={"admin_id": admin_id}
                )
            else:
                raise AdminNotFoundError(f"Admin with ID {admin_id} not found.")
        except Exception as e:
            logger.log_to_console("ERROR", f"Failed to delete admin {admin_id}.", exception=e)
            raise handle_database_error(e, module="admin_helpers", meta_data={"admin_id": admin_id})

    @staticmethod
    def count():
        """Get the number of admins."""
        try:
            count = db.session.query(Admin).count()
            logger.log_to_console("INFO", f"Total number of admins: {count}")
            return count
        except Exception as e:
            logger.log_to_console("ERROR", "Error counting admins.", exception=e)
            raise handle_database_error(e, module="admin_helpers")

    @staticmethod
    def exists(admin_id):
        """Check if an admin with a specific ID exists."""
        try:
            exists = db.session.query(Admin).filter_by(id=admin_id).first() is not None
            logger.log_to_console("INFO", f"Admin existence check for ID {admin_id}: {exists}")
            return exists
        except Exception as e:
            logger.log_to_console("ERROR", "Error checking admin existence.", exception=e)
            raise handle_database_error(e, module="admin_helpers", meta_data={"admin_id": admin_id})

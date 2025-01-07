# admin_helpers.py

from backend.db import db
from backend.models import Admin
from flask import current_app  # To get the current app context
from backend.utils.logger import CentralizedLogger

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
            raise

    @staticmethod
    def get_by_id(admin_id):
        """Get an admin by their ID."""
        with current_app.app_context():
            logger.log_to_console("INFO", f"Fetching admin by ID: {admin_id}")
            return db.session.get(Admin, admin_id)

    @staticmethod
    def get_by_user_id(user_id):
        """Get an admin by the associated user's ID."""
        logger.log_to_console("INFO", f"Fetching admin by user ID: {user_id}")
        return db.session.query(Admin).filter_by(user_id=user_id).first()

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
                logger.log_to_console("WARNING", f"Admin {admin_id} not found for update.")
                logger.log_to_db(
                    "WARNING",
                    "Admin update attempted on non-existent record.",
                    module="admin_helpers",
                    meta_data={"admin_id": admin_id}
                )
                return None
        except Exception as e:
            logger.log_to_console("ERROR", f"Failed to update admin {admin_id}.", exception=e)
            logger.log_to_db(
                "ERROR",
                "Admin update failed.",
                module="admin_helpers",
                meta_data={"admin_id": admin_id, "error": str(e)}
            )
            raise

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
                logger.log_to_console("WARNING", f"Admin {admin_id} not found for deletion.")
                logger.log_to_db(
                    "WARNING",
                    "Admin deletion attempted on non-existent record.",
                    module="admin_helpers",
                    meta_data={"admin_id": admin_id}
                )
        except Exception as e:
            logger.log_to_console("ERROR", f"Failed to delete admin {admin_id}.", exception=e)
            logger.log_to_db(
                "ERROR",
                "Admin deletion failed.",
                module="admin_helpers",
                meta_data={"admin_id": admin_id, "error": str(e)}
            )
            raise

    @staticmethod
    def count():
        """Get the number of admins."""
        count = db.session.query(Admin).count()
        logger.log_to_console("INFO", f"Total number of admins: {count}")
        return count

    @staticmethod
    def exists(admin_id):
        """Check if an admin with a specific ID exists."""
        exists = db.session.query(Admin).filter_by(id=admin_id).first() is not None
        logger.log_to_console("INFO", f"Admin existence check for ID {admin_id}: {exists}")
        return exists

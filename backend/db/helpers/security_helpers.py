from backend.db import db
from backend.models import Security
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.db.errors import (
    SecurityEntryNotFoundError,
    SecurityEntryDeletionError,
    SecurityQueryError,
    SecurityActionCreationError,
    handle_database_error,
)

logger = CentralizedLogger("security_helpers")

class SecurityHelpers:
    @staticmethod
    def create_security_entry(user_id, action):
        """Create a new security entry for a user."""
        try:
            if not user_id or not action:
                raise SecurityActionCreationError("Invalid user ID or action.")

            security_entry = Security(user_id=user_id, action=action)
            db.session.add(security_entry)
            db.session.commit()
            logger.log_to_console("INFO", "Created security entry", user_id=user_id, action=action)
            return security_entry
        except SecurityActionCreationError as e:
            logger.log_to_console("ERROR", str(e), user_id=user_id, action=action)
            raise e  # Directly raise the original exception
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to create security entry", user_id=user_id, action=action, error=str(e))
            db.session.rollback()
            raise handle_database_error(e, module="security_helpers", meta_data={"user_id": user_id, "action": action})

    @staticmethod
    def get_security_by_id(security_id):
        """Get a security entry by its ID."""
        try:
            security_entry = db.session.get(Security, security_id)
            if not security_entry:
                raise SecurityEntryNotFoundError(f"Security entry with ID {security_id} not found.")
            logger.log_to_console("DEBUG", "Fetched security entry by ID", security_id=security_id, found=bool(security_entry))
            return security_entry
        except SecurityEntryNotFoundError as e:
            raise e
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to fetch security entry by ID", security_id=security_id, error=str(e))
            raise handle_database_error(e, module="security_helpers", meta_data={"security_id": security_id})

    @staticmethod
    def get_security_by_user(user_id):
        """Get all security entries for a specific user."""
        try:
            security_entries = db.session.query(Security).filter_by(user_id=user_id).all()
            logger.log_to_console("DEBUG", "Fetched security entries by user", user_id=user_id, count=len(security_entries))
            return security_entries
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to fetch security entries by user", user_id=user_id, error=str(e))
            raise SecurityQueryError(f"Failed to fetch security entries for user_id={user_id}") from e

    @staticmethod
    def get_recent_security_entries(limit=10):
        """Get the most recent security entries."""
        try:
            if not isinstance(limit, int) or limit <= 0:
                raise SecurityQueryError("Limit must be a positive integer.")
            security_entries = db.session.query(Security).order_by(Security.timestamp.desc()).limit(limit).all()
            logger.log_to_console("DEBUG", "Fetched recent security entries", limit=limit, count=len(security_entries))
            return security_entries
        except SecurityQueryError as e:
            logger.log_to_console("ERROR", str(e), limit=limit)
            raise e  # Directly raise the original exception
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to fetch recent security entries", limit=limit, error=str(e))
            raise handle_database_error(e, module="security_helpers", meta_data={"limit": limit})
    @staticmethod
    def delete_security_entry(security_id):
        """Delete a security entry by its ID."""
        try:
            security_entry = db.session.get(Security, security_id)
            if not security_entry:
                logger.log_to_console("WARNING", "Security entry not found for deletion", security_id=security_id)
                raise SecurityEntryNotFoundError(f"Security entry with ID {security_id} not found for deletion.")
            db.session.delete(security_entry)
            db.session.commit()
            logger.log_to_console("INFO", "Deleted security entry", security_id=security_id)
        except Exception as e:
            db.session.rollback()
            logger.log_to_console("ERROR", "Failed to delete security entry", security_id=security_id, error=str(e))
            raise SecurityEntryDeletionError(f"Failed to delete security entry with ID {security_id}") from e

    @staticmethod
    def count():
        """Get the total number of security entries."""
        try:
            total = db.session.query(Security).count()
            logger.log_to_console("DEBUG", "Counted security entries", total=total)
            return total
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to count security entries", error=str(e))
            raise SecurityQueryError("Failed to count security entries.") from e

    @staticmethod
    def exists(security_id):
        """Check if a security entry exists."""
        try:
            exists = db.session.query(Security).filter_by(id=security_id).first() is not None
            logger.log_to_console("DEBUG", "Checked if security entry exists", security_id=security_id, exists=exists)
            return exists
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to check if security entry exists", security_id=security_id, error=str(e))
            raise SecurityQueryError(f"Failed to check existence of security entry with ID {security_id}.") from e

from backend.db import db
from backend.models import Security
from backend.utils.logger import CentralizedLogger

logger = CentralizedLogger("security_helpers")

class SecurityHelpers:
    @staticmethod
    def create_security_entry(user_id, action):
        """Create a new security entry for a user."""
        try:
            security_entry = Security(user_id=user_id, action=action)
            db.session.add(security_entry)
            db.session.commit()
            logger.log_to_console("INFO", "Created security entry", user_id=user_id, action=action)
            return security_entry
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to create security entry", user_id=user_id, action=action, error=str(e))
            db.session.rollback()
            return None

    @staticmethod
    def get_security_by_id(security_id):
        """Get a security entry by its ID."""
        try:
            security_entry = db.session.get(Security, security_id)
            logger.log_to_console("DEBUG", "Fetched security entry by ID", security_id=security_id, found=bool(security_entry))
            return security_entry
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to fetch security entry by ID", security_id=security_id, error=str(e))
            return None

    @staticmethod
    def get_security_by_user(user_id):
        """Get all security entries for a specific user."""
        try:
            security_entries = db.session.query(Security).filter_by(user_id=user_id).all()
            logger.log_to_console("DEBUG", "Fetched security entries by user", user_id=user_id, count=len(security_entries))
            return security_entries
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to fetch security entries by user", user_id=user_id, error=str(e))
            return []

    @staticmethod
    def get_recent_security_entries(limit=10):
        """Get the most recent security entries."""
        try:
            security_entries = db.session.query(Security).order_by(Security.timestamp.desc()).limit(limit).all()
            logger.log_to_console("DEBUG", "Fetched recent security entries", limit=limit, count=len(security_entries))
            return security_entries
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to fetch recent security entries", limit=limit, error=str(e))
            return []

    @staticmethod
    def delete_security_entry(security_id):
        """Delete a security entry by its ID."""
        try:
            security_entry = db.session.get(Security, security_id)
            if security_entry:
                db.session.delete(security_entry)
                db.session.commit()
                logger.log_to_console("INFO", "Deleted security entry", security_id=security_id)
            else:
                logger.log_to_console("WARNING", "Security entry not found for deletion", security_id=security_id)
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to delete security entry", security_id=security_id, error=str(e))

    @staticmethod
    def count():
        """Get the total number of security entries."""
        try:
            total = db.session.query(Security).count()
            logger.log_to_console("DEBUG", "Counted security entries", total=total)
            return total
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to count security entries", error=str(e))
            return 0

    @staticmethod
    def exists(security_id):
        """Check if a security entry exists."""
        try:
            exists = db.session.query(Security).filter_by(id=security_id).first() is not None
            logger.log_to_console("DEBUG", "Checked if security entry exists", security_id=security_id, exists=exists)
            return exists
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to check if security entry exists", security_id=security_id, error=str(e))
            return False

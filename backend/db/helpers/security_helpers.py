from backend.db import db
from backend.models import Security
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.error_handling import handle_database_error
from typing import List

logger = CentralizedLogger("security_helpers")


class SecurityHelpers:
    @staticmethod
    def create_security_entry(user_id: int, action: str) -> Security:
        """
        Create a new security entry for a user.
        """
        if not user_id or not action:
            raise ValueError("User ID and action are required.")

        try:
            security_entry = Security(user_id=user_id, action=action)
            db.session.add(security_entry)
            db.session.commit()
            logger.log_to_console("INFO", f"Created security entry for user ID {user_id}.")
            return security_entry
        except Exception as e:
            db.session.rollback()
            raise handle_database_error(
                e, module="security_helpers", meta_data={"user_id": user_id, "action": action}
            )

    @staticmethod
    def get_security_by_id(security_id: int) -> Security:
        """
        Get a security entry by its ID.
        """
        try:
            security_entry = db.session.get(Security, security_id)
            if not security_entry:
                raise ValueError(f"Security entry with ID {security_id} not found.")
            logger.log_to_console("DEBUG", f"Retrieved security entry ID {security_id}.")
            return security_entry
        except Exception as e:
            raise handle_database_error(
                e, module="security_helpers", meta_data={"security_id": security_id}
            )

    @staticmethod
    def get_security_by_user(user_id: int) -> List[Security]:
        """
        Get all security entries for a specific user.
        """
        try:
            security_entries = db.session.query(Security).filter_by(user_id=user_id).all()
            logger.log_to_console(
                "DEBUG", f"Retrieved {len(security_entries)} security entries for user ID {user_id}."
            )
            return security_entries
        except Exception as e:
            raise handle_database_error(
                e, module="security_helpers", meta_data={"user_id": user_id}
            )

    @staticmethod
    def get_recent_security_entries(limit: int = 10) -> List[Security]:
        """
        Get the most recent security entries.
        """
        if not isinstance(limit, int) or limit <= 0:
            raise ValueError("Limit must be a positive integer.")

        try:
            security_entries = (
                db.session.query(Security)
                .order_by(Security.timestamp.desc())
                .limit(limit)
                .all()
            )
            logger.log_to_console("DEBUG", f"Retrieved {len(security_entries)} recent security entries.")
            return security_entries
        except Exception as e:
            raise handle_database_error(
                e, module="security_helpers", meta_data={"limit": limit}
            )

    @staticmethod
    def delete_security_entry(security_id: int) -> None:
        """
        Delete a security entry by its ID.
        """
        try:
            security_entry = db.session.get(Security, security_id)
            if not security_entry:
                raise ValueError(f"Security entry with ID {security_id} not found.")
            
            db.session.delete(security_entry)
            db.session.commit()
            logger.log_to_console("INFO", f"Deleted security entry ID {security_id}.")
        except Exception as e:
            db.session.rollback()
            raise handle_database_error(
                e, module="security_helpers", meta_data={"security_id": security_id}
            )

    @staticmethod
    def count() -> int:
        """
        Get the total number of security entries.
        """
        try:
            total = db.session.query(Security).count()
            logger.log_to_console("DEBUG", f"Total security entries: {total}.")
            return total
        except Exception as e:
            raise handle_database_error(e, module="security_helpers")

    @staticmethod
    def exists(security_id: int) -> bool:
        """
        Check if a security entry exists.
        """
        try:
            exists = db.session.query(Security).filter_by(id=security_id).first() is not None
            logger.log_to_console("DEBUG", f"Security entry ID {security_id} exists: {exists}.")
            return exists
        except Exception as e:
            raise handle_database_error(
                e, module="security_helpers", meta_data={"security_id": security_id}
            )

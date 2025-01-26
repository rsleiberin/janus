# File: backend/db/helpers/security_helpers.py
# pylint: disable=R1710,W0718

from typing import List
from backend.db.helpers.base_crud import BaseCrudHelper
from backend.models import Security
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.error_handling import handle_database_error

logger = CentralizedLogger("security_helpers")


class SecurityHelpers(BaseCrudHelper):
    """
    CRUD + specialized queries for Security model.
    """

    model = Security

    @staticmethod
    def get_security_by_user(user_id: int) -> List[Security]:
        """
        Get all security entries for a specific user.
        """
        try:
            entries = Security.query.filter_by(user_id=user_id).all()
            logger.log_to_console(
                "DEBUG", f"Fetched {len(entries)} security entries for user {user_id}."
            )
            return entries
        except Exception as err:
            handle_database_error(
                err, module="security_helpers", meta_data={"user_id": user_id}
            )

    @staticmethod
    def get_recent_security_entries(limit: int = 10) -> List[Security]:
        """
        Get the most recent security entries, sorted by created_at desc.
        """
        try:
            entries = (
                Security.query.order_by(Security.created_at.desc()).limit(limit).all()
            )
            logger.log_to_console(
                "DEBUG", f"Retrieved {len(entries)} recent security entries."
            )
            return entries
        except Exception as err:
            handle_database_error(
                err, module="security_helpers", meta_data={"limit": limit}
            )

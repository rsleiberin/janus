# File: backend/db/helpers/admin_helpers.py
# pylint: disable=R1710,W0718

from backend.db.helpers.base_crud import BaseCrudHelper
from backend.models import Admin
from backend.utils.logger import CentralizedLogger

logger = CentralizedLogger("admin_helpers")


class AdminHelpers(BaseCrudHelper):
    """
    CRUD + specialized methods for Admin model.
    """

    model = Admin

    @classmethod
    def custom_method(cls, admin_id: int):
        """
        Example specialized method if needed for Admin logic.
        """
        admin_record = cls.get_by_id(admin_id)
        logger.log_to_console("INFO", f"Custom admin method for Admin ID {admin_id}.")
        # Add domain-specific logic here
        return admin_record

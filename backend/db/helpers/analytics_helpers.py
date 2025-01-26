# File: backend/db/helpers/analytics_helpers.py
# pylint: disable=R1710,W0718

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from backend.db import db
from backend.db.helpers.base_crud import BaseCrudHelper
from backend.models import Analytics
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.error_handling import handle_database_error

logger = CentralizedLogger("analytics_helpers")


class AnalyticsHelpers(BaseCrudHelper):
    """
    CRUD + specialized queries for Analytics model.
    """

    model = Analytics

    @staticmethod
    def get_recent(limit=10, session: Session = None):
        """
        Retrieve the most recent analytics entries (by created_at).
        """
        session = session or db.session
        try:
            analytics_list = (
                session.query(Analytics)
                .order_by(Analytics.created_at.desc())
                .limit(limit)
                .all()
            )
            logger.log_to_console(
                "INFO",
                f"Retrieved {len(analytics_list)} recent Analytics entries.",
                limit=limit,
            )
            return analytics_list
        except SQLAlchemyError as err:
            handle_database_error(
                err, module="AnalyticsHelpers", meta_data={"limit": limit}
            )

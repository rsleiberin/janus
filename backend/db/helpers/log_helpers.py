# File: backend/db/helpers/log_helpers.py
# pylint: disable=R1710,W0718

from typing import List
from sqlalchemy import text
from backend.db.helpers.base_crud import BaseCrudHelper
from backend.models import Log
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.error_handling import handle_database_error

logger = CentralizedLogger("log_helpers")


class LogHelpers(BaseCrudHelper):
    """
    CRUD + specialized queries for Log model.
    """

    model = Log

    @staticmethod
    def get_recent_logs(limit: int = 10) -> List[Log]:
        """
        Retrieve the most recent logs, sorted by created_at desc.
        """
        try:
            logs = Log.query.order_by(Log.created_at.desc()).limit(limit).all()
            logger.log_to_console(
                "INFO", f"Retrieved {len(logs)} recent logs.", limit=limit
            )
            return logs
        except Exception as err:
            handle_database_error(err, module="log_helpers", meta_data={"limit": limit})

    @staticmethod
    def get_logs_with_metadata_key(key: str) -> List[Log]:
        """
        Retrieve logs containing a specific metadata key (using JSON extracts).
        """
        try:
            logs = Log.query.filter(
                text(f"json_extract(log_metadata, '$.{key}') IS NOT NULL")
            ).all()
            logger.log_to_console(
                "INFO", f"Retrieved {len(logs)} logs with metadata key: {key}."
            )
            return logs
        except Exception as err:
            handle_database_error(err, module="log_helpers", meta_data={"key": key})

    @staticmethod
    def get_logs_with_metadata_value(key: str, value: str) -> List[Log]:
        """
        Retrieve logs with a specific metadata key-value pair.
        """
        try:
            logs = (
                Log.query.filter(
                    text(f"json_extract(log_metadata, '$.{key}') = :value")
                )
                .params(value=value)
                .all()
            )
            logger.log_to_console(
                "INFO",
                f"Retrieved {len(logs)} logs with key={key} and value={value}.",
            )
            return logs
        except Exception as err:
            handle_database_error(
                err, module="log_helpers", meta_data={"key": key, "value": value}
            )

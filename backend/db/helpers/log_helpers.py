from datetime import datetime
from typing import List
from sqlalchemy import text
from backend.utils.logger import CentralizedLogger
from backend.db import db
from backend.models import Log
from backend.utils.error_handling.error_handling import handle_database_error
from backend.utils.error_handling.exceptions import LogNotFoundError

logger = CentralizedLogger("log_helpers")


class LogHelpers:
    @staticmethod
    def create_log(
        action: str,
        user_id: int,
        module: str = None,
        level: str = "INFO",
        meta_data: dict = None,
        log_to_db: bool = False,
    ) -> Log:
        """
        Create a new log entry.
        """
        try:
            new_log = Log(
                action=action,
                user_id=user_id,
                module=module,
                level=level,
                log_metadata=meta_data,
                timestamp=datetime.utcnow(),
            )
            db.session.add(new_log)
            db.session.commit()

            logger.log_to_console("INFO", f"Log entry created successfully with ID {new_log.id}.", meta_data=meta_data)
            if log_to_db:
                logger.log_to_db(
                    "INFO",
                    "Log entry created successfully.",
                    module="log_helpers",
                    meta_data={"log_id": new_log.id, "action": action, "user_id": user_id},
                )
            return new_log
        except Exception as e:
            db.session.rollback()
            logger.log_to_console("ERROR", "Failed to create log.", exception=e, meta_data=meta_data)
            if log_to_db:
                logger.log_to_db(
                    "ERROR",
                    "Failed to create log.",
                    module="log_helpers",
                    meta_data={"action": action, "user_id": user_id},
                )
            raise handle_database_error(e, module="log_helpers", meta_data=meta_data)

    @staticmethod
    def get_by_id(log_id: int) -> Log:
        """
        Retrieve a log entry by its ID.
        """
        try:
            log_entry = db.session.get(Log, log_id)
            if not log_entry:
                raise LogNotFoundError(f"Log with ID {log_id} not found.")
            logger.log_to_console("INFO", f"Retrieved log by ID: {log_id}.")
            return log_entry
        except Exception as e:
            raise handle_database_error(e, module="log_helpers", meta_data={"log_id": log_id})

    @staticmethod
    def get_by_user_id(user_id: int) -> List[Log]:
        """
        Retrieve all logs for a specific user.
        """
        try:
            logs = Log.query.filter_by(user_id=user_id).all()
            logger.log_to_console("INFO", f"Retrieved {len(logs)} logs for user ID {user_id}.")
            return logs
        except Exception as e:
            raise handle_database_error(e, module="log_helpers", meta_data={"user_id": user_id})

    @staticmethod
    def get_recent_logs(limit: int = 10) -> List[Log]:
        """
        Retrieve the most recent logs up to a specified limit.
        """
        try:
            logs = Log.query.order_by(Log.timestamp.desc()).limit(limit).all()
            logger.log_to_console("INFO", f"Retrieved {len(logs)} recent logs.", meta_data={"limit": limit})
            return logs
        except Exception as e:
            raise handle_database_error(e, module="log_helpers", meta_data={"limit": limit})

    @staticmethod
    def delete_log(log_id: int) -> bool:
        """
        Delete a log entry by its ID.
        """
        try:
            log_entry = db.session.get(Log, log_id)
            if not log_entry:
                raise LogNotFoundError(f"Log with ID {log_id} not found.")

            db.session.delete(log_entry)
            db.session.commit()
            logger.log_to_console("INFO", f"Deleted log with ID {log_id}.")
            return True
        except Exception as e:
            db.session.rollback()
            raise handle_database_error(e, module="log_helpers", meta_data={"log_id": log_id})

    @staticmethod
    def count() -> int:
        """
        Count the total number of logs.
        """
        try:
            total = Log.query.count()
            logger.log_to_console("INFO", f"Total logs count: {total}.")
            return total
        except Exception as e:
            raise handle_database_error(e, module="log_helpers")

    @staticmethod
    def get_logs_with_metadata_key(key: str) -> List[Log]:
        """
        Retrieve logs containing a specific metadata key.
        """
        try:
            logs = Log.query.filter(text(f"json_extract(log_metadata, '$.{key}') IS NOT NULL")).all()
            logger.log_to_console("INFO", f"Retrieved {len(logs)} logs with metadata key: {key}.")
            return logs
        except Exception as e:
            raise handle_database_error(e, module="log_helpers", meta_data={"key": key})

    @staticmethod
    def get_logs_with_metadata_value(key: str, value: str) -> List[Log]:
        """
        Retrieve logs with a specific metadata key-value pair.
        """
        try:
            logs = (
                Log.query.filter(text(f"json_extract(log_metadata, '$.{key}') = :value"))
                .params(value=value)
                .all()
            )
            logger.log_to_console(
                "INFO",
                f"Retrieved {len(logs)} logs with metadata key: {key} and value: {value}.",
            )
            return logs
        except Exception as e:
            raise handle_database_error(
                e, module="log_helpers", meta_data={"key": key, "value": value}
            )

    @staticmethod
    def get_by_module(module: str) -> List[Log]:
        """
        Retrieve logs by module.
        """
        try:
            logs = Log.query.filter_by(module=module).all()
            logger.log_to_console("INFO", f"Retrieved {len(logs)} logs for module: {module}.")
            return logs
        except Exception as e:
            raise handle_database_error(e, module="log_helpers", meta_data={"module": module})

    @staticmethod
    def get_by_level(level: str) -> List[Log]:
        """
        Retrieve logs by log level.
        """
        try:
            logs = Log.query.filter_by(level=level).all()
            logger.log_to_console("INFO", f"Retrieved {len(logs)} logs for level: {level}.")
            return logs
        except Exception as e:
            raise handle_database_error(e, module="log_helpers", meta_data={"level": level})

    @staticmethod
    def exists(action: str) -> bool:
        """
        Check if a log with a specific action exists.
        """
        try:
            exists = Log.query.filter_by(action=action).first() is not None
            logger.log_to_console("INFO", f"Log exists check for action '{action}': {exists}.")
            return exists
        except Exception as e:
            raise handle_database_error(e, module="log_helpers", meta_data={"action": action})

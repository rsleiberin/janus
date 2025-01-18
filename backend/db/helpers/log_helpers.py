from datetime import datetime
from backend.utils.logger import CentralizedLogger
from backend.db import db
from backend.models import Log
from sqlalchemy import text
from backend.utils.error_handling.db.errors import (
    LogNotFoundError,
    LogCreationError,
    LogDeletionError,
    LogQueryError,
    LogMetadataError,
    handle_database_error
)

logger = CentralizedLogger("log_helpers")

class LogHelpers:
    @staticmethod
    def create_log(action, user_id, module=None, level="INFO", meta_data=None):
        try:
            logger.log_to_console(
                level=level,
                message="Creating log entry",
                action=action,
                user_id=user_id,
                module=module,
                meta_data=meta_data
            )

            # Notice we now store the 'meta_data' argument in the 'log_metadata' column
            new_log = Log(
                action=action,
                user_id=user_id,
                module=module,
                level=level,
                log_metadata=meta_data,  # Updated to match the new Log model
                timestamp=datetime.utcnow()
            )

            db.session.add(new_log)
            db.session.commit()
            logger.log_to_console("DEBUG", f"Log entry created successfully with ID {new_log.id}.")

            return new_log
        except Exception as e:
            db.session.rollback()
            raise LogCreationError(f"Failed to create log entry: {str(e)}") from e

    @staticmethod
    def get_by_id(log_id):
        try:
            log_entry = db.session.get(Log, log_id)
            if not log_entry:
                raise LogNotFoundError(f"Log with ID {log_id} not found.")

            logger.log_to_console("DEBUG", "Retrieved log by ID", log_id=log_id)
            return log_entry
        except LogNotFoundError as e:
            logger.log_to_console("ERROR", str(e), module="log_helpers", meta_data={"log_id": log_id})
            raise e

    @staticmethod
    def get_by_user_id(user_id):
        try:
            logs = Log.query.filter_by(user_id=user_id).all()
            logger.log_to_console("DEBUG", "Retrieved logs by user ID", user_id=user_id, count=len(logs))
            return logs
        except Exception as e:
            raise LogQueryError(f"Failed to retrieve logs for user ID {user_id}: {str(e)}") from e

    @staticmethod
    def get_by_module(module):
        try:
            logs = Log.query.filter_by(module=module).all()
            logger.log_to_console("DEBUG", "Retrieved logs by module", module=module, count=len(logs))
            return logs
        except Exception as e:
            raise LogQueryError(f"Failed to retrieve logs for module {module}: {str(e)}") from e

    @staticmethod
    def get_by_level(level):
        try:
            logs = Log.query.filter_by(level=level).all()
            logger.log_to_console("DEBUG", "Retrieved logs by level", count=len(logs), log_level=level)
            return logs
        except Exception as e:
            raise LogQueryError(f"Failed to retrieve logs for level {level}: {str(e)}") from e

    @staticmethod
    def get_recent_logs(limit=10):
        try:
            logs = Log.query.order_by(Log.timestamp.desc()).limit(limit).all()
            logger.log_to_console("DEBUG", "Retrieved recent logs", count=len(logs))
            return logs
        except Exception as e:
            raise LogQueryError(f"Failed to retrieve recent logs: {str(e)}") from e

    @staticmethod
    def delete_log(log_id):
        try:
            log_entry = db.session.get(Log, log_id)
            if not log_entry:
                raise LogNotFoundError(f"Log with ID {log_id} not found.")

            db.session.delete(log_entry)
            db.session.commit()
            logger.log_to_console("INFO", "Log entry deleted", log_id=log_id)
            return True
        except LogNotFoundError as e:
            logger.log_to_console("WARNING", str(e))
            raise
        except Exception as e:
            db.session.rollback()
            raise LogDeletionError(f"Failed to delete log with ID {log_id}: {str(e)}") from e

    @staticmethod
    def count():
        try:
            log_count = Log.query.count()
            logger.log_to_console("DEBUG", "Counted logs", count=log_count)
            return log_count
        except Exception as e:
            raise LogQueryError(f"Failed to count logs: {str(e)}") from e

    @staticmethod
    def exists(**filters):
        try:
            exists_query = Log.query.filter_by(**filters).first() is not None
            logger.log_to_console(
                "DEBUG", "Checked log existence", filters=filters, exists=exists_query
            )
            return exists_query
        except Exception as e:
            raise LogQueryError(f"Failed to check log existence: {str(e)}") from e

    @staticmethod
    def get_logs_with_metadata_key(key):
        try:
            # Changed 'meta_data' to 'log_metadata'
            logs = Log.query.filter(text(f"json_extract(log_metadata, '$.{key}') IS NOT NULL")).all()
            logger.log_to_console("DEBUG", "Retrieved logs by metadata key", key=key, count=len(logs))
            return logs
        except Exception as e:
            raise LogMetadataError(f"Failed to retrieve logs by metadata key {key}: {str(e)}") from e

    @staticmethod
    def get_logs_with_metadata_value(key, value):
        try:
            # Changed 'meta_data' to 'log_metadata'
            logs = Log.query.filter(
                text(f"json_extract(log_metadata, '$.{key}') = :value")
            ).params(value=value).all()
            logger.log_to_console(
                "DEBUG",
                "Retrieved logs by metadata value",
                key=key,
                value=value,
                count=len(logs),
            )
            return logs
        except Exception as e:
            logger.log_to_console(
                "ERROR",
                "Failed to retrieve logs by metadata value",
                key=key,
                value=value,
                error=str(e),
            )
            return []

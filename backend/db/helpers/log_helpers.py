from datetime import datetime
from backend.utils.logger import CentralizedLogger
from backend.db import db
from backend.models import Log
from sqlalchemy import text

logger = CentralizedLogger("log_helpers")

class LogHelpers:
    @staticmethod
    def create_log(action, user_id, module=None, level="INFO", meta_data=None):
        """
        Create a new log entry for a user action and save it to the database.

        Args:
            action (str): The action to log.
            user_id (int): The ID of the user performing the action.
            module (str, optional): The module where the action occurred.
            level (str, optional): The log level (e.g., INFO, DEBUG).
            meta_data (dict, optional): Additional metadata for the log.

        Returns:
            Log: The created log entry or None if failed.
        """
        try:
            logger.log_to_console(
                level=level,
                message="Creating log entry",
                action=action,
                user_id=user_id,
                module=module,
                meta_data=meta_data
            )
            logger.log_to_console("DEBUG", "Preparing log entry for database insertion.")
            
            # Create log entry
            new_log = Log(
                action=action,
                user_id=user_id,
                module=module,
                level=level,
                meta_data=meta_data,
                timestamp=datetime.utcnow()
            )
            
            # Add to database
            db.session.add(new_log)
            db.session.commit()
            logger.log_to_console("DEBUG", f"Log entry created successfully with ID {new_log.id}.")
            
            return new_log
        except Exception as e:
            logger.log_to_console(
                "ERROR",
                "Failed to create log entry",
                error=str(e),
                action=action,
                user_id=user_id,
                module=module,
                meta_data=meta_data
            )
            db.session.rollback()
            return None


    @staticmethod
    def get_by_id(log_id):
        """
        Retrieve a log entry by its ID.

        Args:
            log_id (int): The ID of the log to retrieve.

        Returns:
            Log: The log entry if found, None otherwise.
        """
        try:
            log_entry = db.session.get(Log, log_id)
            logger.log_to_console("DEBUG", "Retrieved log by ID", log_id=log_id)
            return log_entry
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to retrieve log by ID", error=str(e))
            return None

    @staticmethod
    def get_by_user_id(user_id):
        """
        Retrieve all logs for a given user ID.

        Args:
            user_id (int): The user ID to filter logs by.

        Returns:
            list[Log]: A list of log entries for the user.
        """
        try:
            logs = Log.query.filter_by(user_id=user_id).all()
            logger.log_to_console("DEBUG", "Retrieved logs by user ID", user_id=user_id, count=len(logs))
            return logs
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to retrieve logs by user ID", error=str(e))
            return []

    @staticmethod
    def get_by_module(module):
        """
        Retrieve all logs for a given module.

        Args:
            module (str): The module to filter logs by.

        Returns:
            list[Log]: A list of log entries for the module.
        """
        try:
            logs = Log.query.filter_by(module=module).all()
            logger.log_to_console("DEBUG", "Retrieved logs by module", module=module, count=len(logs))
            return logs
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to retrieve logs by module", error=str(e))
            return []

    @staticmethod
    def get_by_level(level):
        """
        Retrieve all logs for a given log level.

        Args:
            level (str): The log level to filter logs by.

        Returns:
            list[Log]: A list of log entries for the level.
        """
        try:
            logs = Log.query.filter_by(level=level).all()
            logger.log_to_console("DEBUG", "Retrieved logs by level", count=len(logs), log_level=level)
            return logs
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to retrieve logs by level", error=str(e))
            return []

    @staticmethod
    def get_recent_logs(limit=10):
        """
        Retrieve the most recent log entries.

        Args:
            limit (int): The maximum number of log entries to retrieve.

        Returns:
            list[Log]: A list of the most recent log entries.
        """
        try:
            logs = Log.query.order_by(Log.timestamp.desc()).limit(limit).all()
            logger.log_to_console("DEBUG", "Retrieved recent logs", count=len(logs))
            return logs
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to retrieve recent logs", error=str(e))
            return []

    @staticmethod
    def delete_log(log_id):
        """
        Delete a log entry by its ID.

        Args:
            log_id (int): The ID of the log to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        try:
            log_entry = db.session.get(Log, log_id)
            if not log_entry:
                logger.log_to_console("WARNING", "Log entry not found for deletion", log_id=log_id)
                return False
            db.session.delete(log_entry)
            db.session.commit()
            logger.log_to_console("INFO", "Log entry deleted", log_id=log_id)
            return True
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to delete log entry", error=str(e))
            db.session.rollback()
            return False

    @staticmethod
    def count():
        """
        Count the total number of logs.

        Returns:
            int: The total count of logs.
        """
        try:
            log_count = Log.query.count()
            logger.log_to_console("DEBUG", "Counted logs", count=log_count)
            return log_count
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to count logs", error=str(e))
            return 0

    @staticmethod
    def exists(**filters):
        """
        Check if a log entry exists based on given filters.

        Args:
            **filters: Filters as key-value pairs for the query.

        Returns:
            bool: True if a log entry exists, False otherwise.
        """
        try:
            exists_query = Log.query.filter_by(**filters).first() is not None
            logger.log_to_console(
                "DEBUG", "Checked log existence", filters=filters, exists=exists_query
            )
            return exists_query
        except Exception as e:
            logger.log_to_console(
                "ERROR", "Failed to check log existence", filters=filters, error=str(e)
            )
            return False


    @staticmethod
    def get_logs_with_metadata_key(key):
        """
        Retrieve logs containing a specific metadata key.

        Args:
            key (str): The metadata key to filter logs by.

        Returns:
            list[Log]: A list of log entries containing the key.
        """
        try:
            # Use JSON functions for SQLite
            logs = Log.query.filter(text(f"json_extract(meta_data, '$.{key}') IS NOT NULL")).all()
            logger.log_to_console("DEBUG", "Retrieved logs by metadata key", key=key, count=len(logs))
            return logs
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to retrieve logs by metadata key", error=str(e))
            return []




    @staticmethod
    def get_logs_with_metadata_value(key, value):
        """
        Retrieve logs where a specific metadata key matches a value.

        Args:
            key (str): The metadata key to filter logs by.
            value (Any): The value of the metadata key to filter logs by.

        Returns:
            list[Log]: A list of log entries containing the key-value pair.
        """
        try:
            logs = Log.query.filter(Log.meta_data[key] == value).all()
            logger.log_to_console("DEBUG", "Retrieved logs by metadata value", key=key, value=value, count=len(logs))
            return logs
        except Exception as e:
            logger.log_to_console("ERROR", "Failed to retrieve logs by metadata value", error=str(e))
            return []

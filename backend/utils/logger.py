import logging
import json
from datetime import datetime
from backend.db import db
from backend.models import Log


class CentralizedLogger:
    def __init__(self, name="app"):
        self.logger = logging.getLogger(name)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def log_to_console(self, level, message, **kwargs):
        """
        Logs messages to the console with optional metadata.
        Args:
            level (str): Logging level (INFO, DEBUG, WARNING, ERROR, CRITICAL).
            message (str): The log message.
            kwargs: Additional context as key-value pairs.
        """
        formatted_message = self.format_message(message, **kwargs)
        log_method = getattr(self.logger, level.lower(), None)
        if log_method:
            log_method(formatted_message)
        else:
            self.logger.warning(f"Invalid log level '{level}': {formatted_message}")

    def log_to_db(self, level, message, module=None, user_id=None, meta_data=None):
        """
        Logs messages to the database.
        Args:
            level (str): Logging level.
            message (str): The log message.
            module (str, optional): Module name where the log originated.
            user_id (int, optional): ID of the user associated with the log.
            meta_data (dict, optional): Additional metadata.
        """
        try:
            log_entry = Log(
                action=message,
                level=level,
                module=module,
                user_id=user_id,
                timestamp=datetime.utcnow(),
                meta_data=meta_data,
            )
            db.session.add(log_entry)
            db.session.commit()
        except Exception as e:
            self.logger.error(f"Failed to log to database: {str(e)}")
            db.session.rollback()

    def format_message(self, message, **kwargs):
        """
        Formats messages to include additional context.
        Args:
            message (str): The base log message.
            kwargs: Additional context as key-value pairs.
        Returns:
            str: Formatted message with optional context.
        """
        if kwargs:
            return f"{message} | Context: {json.dumps(kwargs, default=str)}"
        return message


# Example usage
if __name__ == "__main__":
    logger = CentralizedLogger()

    # Console logging
    logger.log_to_console("INFO", "Application started", module="main")

    # Database logging
    logger.log_to_db(
        level="ERROR",
        message="Database connection failed",
        module="db_setup",
        user_id=1,
        meta_data={"details": "Connection timeout after 30 seconds"}
    )

# File: backend/utils/logger.py

import logging
import json
import os
from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError
from backend.db import db
from backend.models import Log


class CentralizedLogger:
    """
    A centralized logging utility for the application.

    Args:
        name (str): The logger's name.
        log_level (str, optional): Logging level (DEBUG, INFO, WARNING,
            ERROR, CRITICAL).
            If not provided, the value is read from the environment
            variable `LOG_LEVEL`.
    """

    VALID_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}

    def __init__(self, name="app", log_level=None):
        """
        Initializes the logger.

        Args:
            name (str): The logger's name.
            log_level (str, optional): Logging level (DEBUG, INFO, WARNING, ERROR,
                CRITICAL). If not provided, the value is read from the environment.
        """
        self.logger = logging.getLogger(name)

        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        log_level = log_level or os.getenv("LOG_LEVEL", "DEBUG").upper()
        if log_level not in self.VALID_LOG_LEVELS:
            log_level = "DEBUG"

        self.logger.setLevel(getattr(logging, log_level))

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
            self.logger.warning("Invalid log level '%s': %s", level, formatted_message)

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
                timestamp=datetime.now(timezone.utc),
                log_metadata=meta_data,
            )
            db.session.add(log_entry)
            db.session.commit()
        except SQLAlchemyError as e:
            self.logger.error("Failed to log to database: %s", str(e))
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
            context = json.dumps(kwargs, default=str)
            return f"{message} | Context: {context}"
        return message

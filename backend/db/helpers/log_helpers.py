from backend.db import db
from backend.models import Log
from sqlalchemy.sql.expression import func, cast
from sqlalchemy.types import String


class LogHelpers:
    @staticmethod
    def create_log(action, user_id, module=None, level=None, meta_data=None):
        """
        Create a new log entry for a user action.

        Args:
            action (str): The action to log.
            user_id (int): The ID of the user performing the action.
            module (str, optional): The module where the action occurred.
            level (str, optional): The log level (e.g., INFO, DEBUG).
            meta_data (dict, optional): Additional metadata for the log.
        """
        log = Log(action=action, user_id=user_id, module=module, level=level, meta_data=meta_data)
        db.session.add(log)
        db.session.commit()
        return log

    @staticmethod
    def get_by_id(log_id):
        """Get a log by its ID."""
        return db.session.get(Log, log_id)

    @staticmethod
    def get_by_user_id(user_id):
        """Get logs by the user ID."""
        return db.session.query(Log).filter_by(user_id=user_id).all()

    @staticmethod
    def get_by_module(module):
        """Get logs by the module."""
        return db.session.query(Log).filter_by(module=module).all()

    @staticmethod
    def get_by_level(level):
        """Get logs by the log level."""
        return db.session.query(Log).filter_by(level=level).all()

    @staticmethod
    def get_recent_logs(limit=10):
        """Get the most recent logs."""
        return db.session.query(Log).order_by(Log.timestamp.desc()).limit(limit).all()

    @staticmethod
    def delete_log(log_id):
        """Delete a log entry by its ID."""
        log = db.session.get(Log, log_id)
        if log:
            db.session.delete(log)
            db.session.commit()

    @staticmethod
    def count():
        """Get the total number of logs."""
        return db.session.query(Log).count()

    @staticmethod
    def exists(log_id):
        """Check if a log entry exists."""
        return db.session.query(Log).filter_by(id=log_id).first() is not None

    @staticmethod
    def get_logs_with_metadata_key(key):
        """Retrieve logs where the metadata contains a specific key."""
        return (
            db.session.query(Log)
            .filter(func.json_extract(Log.meta_data, f'$.{key}') != None)
            .all()
        )


    @staticmethod
    def get_logs_by_metadata_value(key, value):
        """Retrieve logs where the metadata contains a specific key-value pair."""
        return (
            db.session.query(Log)
            .filter(cast(func.json_extract(Log.meta_data, f'$.{key}'), String) == str(value))
            .all()
        )
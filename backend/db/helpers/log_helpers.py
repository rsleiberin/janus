# log_helpers.py

from backend.db import db
from backend.models import Log
from datetime import datetime

class LogHelpers:
    @staticmethod
    def create_log(action, user_id):
        """Create a new log entry for a user action."""
        log = Log(action=action, user_id=user_id)
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

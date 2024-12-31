# log_helpers.py
from backend.db import db
from backend.models import Log
from datetime import datetime

# Log Model Helpers
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
        return Log.query.get(log_id)

    @staticmethod
    def get_by_user_id(user_id):
        """Get logs by the user ID."""
        return Log.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_recent_logs(limit=10):
        """Get the most recent logs."""
        return Log.query.order_by(Log.timestamp.desc()).limit(limit).all()

    @staticmethod
    def delete_log(log_id):
        """Delete a log entry by its ID."""
        log = Log.query.get(log_id)
        if log:
            db.session.delete(log)
            db.session.commit()

    @staticmethod
    def count():
        """Get the total number of logs."""
        return Log.query.count()

    @staticmethod
    def exists(log_id):
        """Check if a log entry exists."""
        return Log.query.filter_by(id=log_id).first() is not None
# security_helpers.py
from backend.db import db
from backend.models import Security
from datetime import datetime

# Security Model Helpers
class SecurityHelpers:

    @staticmethod
    def create_security_entry(user_id, action):
        """Create a new security entry for a user."""
        security_entry = Security(user_id=user_id, action=action)
        db.session.add(security_entry)
        db.session.commit()
        return security_entry

    @staticmethod
    def get_security_by_id(security_id):
        """Get a security entry by its ID."""
        return Security.query.get(security_id)

    @staticmethod
    def get_security_by_user(user_id):
        """Get all security entries for a specific user."""
        return Security.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_recent_security_entries(limit=10):
        """Get the most recent security entries."""
        return Security.query.order_by(Security.timestamp.desc()).limit(limit).all()

    @staticmethod
    def delete_security_entry(security_id):
        """Delete a security entry by its ID."""
        security_entry = Security.query.get(security_id)
        if security_entry:
            db.session.delete(security_entry)
            db.session.commit()

    @staticmethod
    def count():
        """Get the total number of security entries."""
        return Security.query.count()

    @staticmethod
    def exists(security_id):
        """Check if a security entry exists."""
        return Security.query.filter_by(id=security_id).first() is not None
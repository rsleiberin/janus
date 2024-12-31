# analytics_helpers.py
from backend.db import db
from backend.models import Analytics
from datetime import datetime

# Analytics Model Helpers
class AnalyticsHelpers:

    @staticmethod
    def create_analytics(data):
        """Create new analytics entry with the provided data."""
        analytics = Analytics(data=data)
        db.session.add(analytics)
        db.session.commit()
        return analytics

    @staticmethod
    def get_by_id(analytics_id):
        """Get analytics by its ID."""
        return Analytics.query.get(analytics_id)

    @staticmethod
    def get_all_analytics():
        """Get all analytics entries."""
        return Analytics.query.all()

    @staticmethod
    def get_recent_analytics(limit=10):
        """Get the most recent analytics entries."""
        return Analytics.query.order_by(Analytics.created_at.desc()).limit(limit).all()

    @staticmethod
    def delete_analytics(analytics_id):
        """Delete an analytics entry by its ID."""
        analytics = Analytics.query.get(analytics_id)
        if analytics:
            db.session.delete(analytics)
            db.session.commit()

    @staticmethod
    def count():
        """Get the total number of analytics entries."""
        return Analytics.query.count()

    @staticmethod
    def exists(analytics_id):
        """Check if an analytics entry exists."""
        return Analytics.query.filter_by(id=analytics_id).first() is not None
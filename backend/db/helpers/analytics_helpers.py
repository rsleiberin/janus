from backend.db import db
from backend.models import Analytics
from sqlalchemy.orm import Session

# Analytics Model Helpers
class AnalyticsHelpers:

    @staticmethod
    def create_analytics(data, session: Session = None):
        """Create new analytics entry with the provided data."""
        session = session or db.session  # Use the provided session or fallback to db.session
        analytics = Analytics(data=data)
        session.add(analytics)
        session.commit()
        return analytics

    @staticmethod
    def get_by_id(session: Session, analytics_id: int):
        """Get analytics by its ID."""
        return session.get(Analytics, analytics_id)

    @staticmethod
    def get_all_analytics(session: Session = None):
        """Get all analytics entries."""
        session = session or db.session
        return session.query(Analytics).all()

    @staticmethod
    def get_recent_analytics(session: Session = None, limit=10):
        """Get the most recent analytics entries."""
        session = session or db.session
        return session.query(Analytics).order_by(Analytics.created_at.desc()).limit(limit).all()

    @staticmethod
    def delete_analytics(session: Session, analytics_id: int):
        """Delete an analytics entry by its ID."""
        analytics = session.get(Analytics, analytics_id)
        if analytics:
            session.delete(analytics)
            session.commit()

    @staticmethod
    def count(session: Session = None):
        """Get the total number of analytics entries."""
        session = session or db.session
        return session.query(Analytics).count()

    @staticmethod
    def exists(session: Session, analytics_id: int):
        """Check if an analytics entry exists."""
        return session.query(Analytics).filter_by(id=analytics_id).first() is not None

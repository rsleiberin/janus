# analytics_helpers.py
from backend.db import db
from backend.models import Analytics
from sqlalchemy.orm import Session
from backend.utils.logger import CentralizedLogger

logger = CentralizedLogger(name="analytics_helpers")


class AnalyticsHelpers:

    @staticmethod
    def create_analytics(data, session: Session = None):
        """Create new analytics entry with the provided data."""
        session = session or db.session
        analytics = Analytics(data=data)
        session.add(analytics)
        session.commit()
        logger.log_to_console("INFO", "Analytics entry created", data=data)
        logger.log_to_db(
            level="INFO",
            message="Analytics entry created",
            module="analytics_helpers",
            meta_data={"data": data}
        )
        return analytics

    @staticmethod
    def get_by_id(session: Session, analytics_id: int):
        """Get analytics by its ID."""
        analytics = session.get(Analytics, analytics_id)
        logger.log_to_console(
            "INFO",
            f"Retrieved analytics entry by ID: {analytics_id}",
            found=analytics is not None
        )
        logger.log_to_db(
            level="INFO",
            message=f"Retrieved analytics entry by ID: {analytics_id}",
            module="analytics_helpers",
            meta_data={"analytics_id": analytics_id, "found": analytics is not None}
        )
        return analytics

    @staticmethod
    def get_all_analytics(session: Session = None):
        """Get all analytics entries."""
        session = session or db.session
        analytics = session.query(Analytics).all()
        logger.log_to_console(
            "INFO",
            "Retrieved all analytics entries",
            count=len(analytics)
        )
        logger.log_to_db(
            level="INFO",
            message="Retrieved all analytics entries",
            module="analytics_helpers",
            meta_data={"count": len(analytics)}
        )
        return analytics

    @staticmethod
    def get_recent_analytics(session: Session = None, limit=10):
        """Get the most recent analytics entries."""
        session = session or db.session
        analytics = session.query(Analytics).order_by(Analytics.created_at.desc()).limit(limit).all()
        logger.log_to_console(
            "INFO",
            f"Retrieved recent analytics entries (limit {limit})",
            count=len(analytics)
        )
        logger.log_to_db(
            level="INFO",
            message=f"Retrieved recent analytics entries (limit {limit})",
            module="analytics_helpers",
            meta_data={"limit": limit, "count": len(analytics)}
        )
        return analytics

    @staticmethod
    def delete_analytics(session: Session, analytics_id: int):
        """Delete an analytics entry by its ID."""
        analytics = session.get(Analytics, analytics_id)
        if analytics:
            session.delete(analytics)
            session.commit()
            logger.log_to_console("INFO", f"Deleted analytics entry with ID: {analytics_id}")
            logger.log_to_db(
                level="INFO",
                message=f"Deleted analytics entry with ID: {analytics_id}",
                module="analytics_helpers",
                meta_data={"analytics_id": analytics_id}
            )
        else:
            logger.log_to_console("WARNING", f"Analytics entry not found for ID: {analytics_id}")
            logger.log_to_db(
                level="WARNING",
                message=f"Analytics entry not found for ID: {analytics_id}",
                module="analytics_helpers",
                meta_data={"analytics_id": analytics_id}
            )

    @staticmethod
    def count(session: Session = None):
        """Get the total number of analytics entries."""
        session = session or db.session
        total = session.query(Analytics).count()
        logger.log_to_console("INFO", "Total analytics entries count retrieved", count=total)
        logger.log_to_db(
            level="INFO",
            message="Total analytics entries count retrieved",
            module="analytics_helpers",
            meta_data={"count": total}
        )
        return total

    @staticmethod
    def exists(session: Session, analytics_id: int):
        """Check if an analytics entry exists."""
        exists = session.query(Analytics).filter_by(id=analytics_id).first() is not None
        logger.log_to_console(
            "INFO",
            f"Analytics entry existence check for ID: {analytics_id}",
            exists=exists
        )
        logger.log_to_db(
            level="INFO",
            message=f"Analytics entry existence check for ID: {analytics_id}",
            module="analytics_helpers",
            meta_data={"analytics_id": analytics_id, "exists": exists}
        )
        return exists

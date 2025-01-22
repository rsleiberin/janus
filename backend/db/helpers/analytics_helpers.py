# File: backend/db/helpers/analytics_helpers.py

from backend.db import db
from backend.models import Analytics
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.error_handling import handle_database_error
from backend.utils.error_handling.exceptions import FileHandlerError  # Ensure this is correctly imported if used

# Initialize the logger
logger = CentralizedLogger(name="analytics_helpers")


class AnalyticsHelpers:
    @staticmethod
    def create_analytics(data, session: Session = None):
        """Create a new analytics entry with the provided data."""
        session = session or db.session
        try:
            analytics = Analytics(data=data)
            session.add(analytics)
            session.commit()
            logger.log_to_console("INFO", "Analytics entry created", meta_data={"data": data})
            logger.log_to_db(
                level="INFO",
                message="Analytics entry created",
                module="analytics_helpers",
                meta_data={"data": data},
            )
            return analytics
        except SQLAlchemyError as e:
            logger.log_to_console("ERROR", "Failed to create analytics entry", exc_info=e)
            raise handle_database_error(e, module="analytics_helpers", meta_data={"data": data})

    @staticmethod
    def get_by_id(session: Session, analytics_id: int):
        """Get analytics by its ID."""
        try:
            analytics = session.get(Analytics, analytics_id)
            if not analytics:
                raise ValueError(f"Analytics entry with ID {analytics_id} not found.")
            logger.log_to_console(
                "INFO", f"Retrieved analytics entry by ID: {analytics_id}", meta_data={"found": True}
            )
            return analytics
        except SQLAlchemyError as e:
            logger.log_to_console(
                "ERROR", f"Failed to retrieve analytics entry with ID: {analytics_id}", exc_info=e
            )
            raise handle_database_error(e, module="analytics_helpers", meta_data={"analytics_id": analytics_id})

    @staticmethod
    def get_all_analytics(session: Session = None):
        """Get all analytics entries."""
        session = session or db.session
        try:
            analytics = session.query(Analytics).all()
            logger.log_to_console("INFO", "Retrieved all analytics entries", meta_data={"count": len(analytics)})
            return analytics
        except SQLAlchemyError as e:
            logger.log_to_console("ERROR", "Failed to retrieve all analytics entries", exc_info=e)
            raise handle_database_error(e, module="analytics_helpers")

    @staticmethod
    def get_recent_analytics(session: Session = None, limit=10):
        """Get the most recent analytics entries."""
        session = session or db.session
        try:
            analytics = (
                session.query(Analytics)
                .order_by(Analytics.created_at.desc())
                .limit(limit)
                .all()
            )
            logger.log_to_console(
                "INFO", f"Retrieved recent analytics entries (limit {limit})", meta_data={"count": len(analytics)}
            )
            return analytics
        except SQLAlchemyError as e:
            logger.log_to_console(
                "ERROR", f"Failed to retrieve recent analytics entries (limit {limit})", exc_info=e
            )
            raise handle_database_error(e, module="analytics_helpers", meta_data={"limit": limit})

    @staticmethod
    def delete_analytics(session: Session, analytics_id: int):
        """Delete an analytics entry by its ID."""
        try:
            analytics = session.get(Analytics, analytics_id)
            if not analytics:
                raise ValueError(f"Analytics entry with ID {analytics_id} not found.")
            session.delete(analytics)
            session.commit()
            logger.log_to_console("INFO", f"Deleted analytics entry with ID: {analytics_id}")
        except ValueError as e:
            logger.log_to_console("WARNING", str(e))
            raise
        except SQLAlchemyError as e:
            logger.log_to_console(
                "ERROR", f"Failed to delete analytics entry with ID: {analytics_id}", exc_info=e
            )
            raise handle_database_error(e, module="analytics_helpers", meta_data={"analytics_id": analytics_id})

    @staticmethod
    def count(session: Session = None):
        """Get the total number of analytics entries."""
        session = session or db.session
        try:
            total = session.query(Analytics).count()
            logger.log_to_console("INFO", "Total analytics entries count retrieved", meta_data={"count": total})
            return total
        except SQLAlchemyError as e:
            logger.log_to_console("ERROR", "Failed to count analytics entries", exc_info=e)
            raise handle_database_error(e, module="analytics_helpers")

    @staticmethod
    def exists(session: Session, analytics_id: int):
        """Check if an analytics entry exists."""
        try:
            exists = (
                session.query(Analytics).filter_by(id=analytics_id).first() is not None
            )
            logger.log_to_console(
                "INFO", f"Analytics entry existence check for ID: {analytics_id}", meta_data={"exists": exists}
            )
            return exists
        except SQLAlchemyError as e:
            logger.log_to_console(
                "ERROR", f"Failed to check existence of analytics entry with ID: {analytics_id}", exc_info=e
            )
            raise handle_database_error(e, module="analytics_helpers", meta_data={"analytics_id": analytics_id})

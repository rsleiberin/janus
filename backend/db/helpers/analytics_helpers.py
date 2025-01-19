from backend.db import db
from backend.models import Analytics
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.db.errors import (
    AnalyticsCreationError,
    AnalyticsNotFoundError,
    AnalyticsDeletionError,
    AnalyticsQueryError,
    handle_database_error,
)

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
            logger.log_to_console("INFO", "Analytics entry created", data=data)
            logger.log_to_db(
                level="INFO",
                message="Analytics entry created",
                module="analytics_helpers",
                meta_data={"data": data},
            )
            return analytics
        except SQLAlchemyError as e:
            logger.log_to_console(
                "ERROR", "Failed to create analytics entry", exception=e
            )
            logger.log_to_db(
                "ERROR",
                "Analytics creation failed",
                module="analytics_helpers",
                meta_data={"data": data, "error": str(e)},
            )
            raise AnalyticsCreationError(
                f"Failed to create analytics entry: {str(e)}"
            ) from e

    @staticmethod
    def get_by_id(session: Session, analytics_id: int):
        """Get analytics by its ID."""
        try:
            analytics = session.get(Analytics, analytics_id)
            if not analytics:
                raise AnalyticsNotFoundError(
                    f"Analytics entry with ID {analytics_id} not found."
                )
            logger.log_to_console(
                "INFO", f"Retrieved analytics entry by ID: {analytics_id}", found=True
            )
            logger.log_to_db(
                level="INFO",
                message=f"Retrieved analytics entry by ID: {analytics_id}",
                module="analytics_helpers",
                meta_data={"analytics_id": analytics_id, "found": True},
            )
            return analytics
        except SQLAlchemyError as e:
            logger.log_to_console(
                "ERROR",
                f"Failed to retrieve analytics entry with ID: {analytics_id}",
                exception=e,
            )
            handle_database_error(
                e, module="analytics_helpers", meta_data={"analytics_id": analytics_id}
            )

    @staticmethod
    def get_all_analytics(session: Session = None):
        """Get all analytics entries."""
        session = session or db.session
        try:
            analytics = session.query(Analytics).all()
            logger.log_to_console(
                "INFO", "Retrieved all analytics entries", count=len(analytics)
            )
            logger.log_to_db(
                level="INFO",
                message="Retrieved all analytics entries",
                module="analytics_helpers",
                meta_data={"count": len(analytics)},
            )
            return analytics
        except SQLAlchemyError as e:
            logger.log_to_console(
                "ERROR", "Failed to retrieve all analytics entries", exception=e
            )
            raise AnalyticsQueryError(
                "Failed to retrieve all analytics entries."
            ) from e

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
                "INFO",
                f"Retrieved recent analytics entries (limit {limit})",
                count=len(analytics),
            )
            logger.log_to_db(
                level="INFO",
                message=f"Retrieved recent analytics entries (limit {limit})",
                module="analytics_helpers",
                meta_data={"limit": limit, "count": len(analytics)},
            )
            return analytics
        except SQLAlchemyError as e:
            logger.log_to_console(
                "ERROR",
                f"Failed to retrieve recent analytics entries (limit {limit})",
                exception=e,
            )
            raise AnalyticsQueryError(
                f"Failed to retrieve recent analytics entries (limit {limit})."
            ) from e

    @staticmethod
    def delete_analytics(session: Session, analytics_id: int):
        """Delete an analytics entry by its ID."""
        try:
            analytics = session.get(Analytics, analytics_id)
            if not analytics:
                raise AnalyticsNotFoundError(
                    f"Analytics entry with ID {analytics_id} not found."
                )
            session.delete(analytics)
            session.commit()
            logger.log_to_console(
                "INFO", f"Deleted analytics entry with ID: {analytics_id}"
            )
            logger.log_to_db(
                level="INFO",
                message=f"Deleted analytics entry with ID: {analytics_id}",
                module="analytics_helpers",
                meta_data={"analytics_id": analytics_id},
            )
        except AnalyticsNotFoundError as e:
            logger.log_to_console("WARNING", str(e))
            logger.log_to_db(
                level="WARNING",
                message=str(e),
                module="analytics_helpers",
                meta_data={"analytics_id": analytics_id},
            )
            raise
        except SQLAlchemyError as e:
            logger.log_to_console(
                "ERROR",
                f"Failed to delete analytics entry with ID: {analytics_id}",
                exception=e,
            )
            raise AnalyticsDeletionError(
                f"Failed to delete analytics entry with ID {analytics_id}."
            ) from e

    @staticmethod
    def count(session: Session = None):
        """Get the total number of analytics entries."""
        session = session or db.session
        try:
            total = session.query(Analytics).count()
            logger.log_to_console(
                "INFO", "Total analytics entries count retrieved", count=total
            )
            logger.log_to_db(
                level="INFO",
                message="Total analytics entries count retrieved",
                module="analytics_helpers",
                meta_data={"count": total},
            )
            return total
        except SQLAlchemyError as e:
            logger.log_to_console(
                "ERROR", "Failed to count analytics entries", exception=e
            )
            raise AnalyticsQueryError("Failed to count analytics entries.") from e

    @staticmethod
    def exists(session: Session, analytics_id: int):
        """Check if an analytics entry exists."""
        try:
            exists = (
                session.query(Analytics).filter_by(id=analytics_id).first() is not None
            )
            logger.log_to_console(
                "INFO",
                f"Analytics entry existence check for ID: {analytics_id}",
                exists=exists,
            )
            logger.log_to_db(
                level="INFO",
                message=f"Analytics entry existence check for ID: {analytics_id}",
                module="analytics_helpers",
                meta_data={"analytics_id": analytics_id, "exists": exists},
            )
            return exists
        except SQLAlchemyError as e:
            logger.log_to_console(
                "ERROR",
                f"Failed to check existence of analytics entry with ID: {analytics_id}",
                exception=e,
            )
            raise AnalyticsQueryError(
                f"Failed to check existence of analytics entry with ID {analytics_id}."
            ) from e

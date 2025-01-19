from flask import Blueprint, jsonify
from sqlalchemy.sql import text
from sqlalchemy.exc import OperationalError
from backend.db import db
from backend.utils.error_handling.routes.errors import (
    DatabaseUnavailableError,
    format_error_response,
)
from backend.utils.logger import CentralizedLogger

# Initialize the logger
logger = CentralizedLogger("status_routes")

# Create a blueprint for status routes
status_bp = Blueprint("status", __name__)


@status_bp.route("/status", methods=["GET"])
def health_check():
    """
    Health check endpoint to verify API and database status.
    """
    try:
        # Check database connection
        db.session.execute(text("SELECT 1"))
        logger.log_to_console("INFO", "Health check passed: Database connected.")
        return jsonify({"status": "ok", "database": "connected"})
    except OperationalError as e:
        logger.log_to_console("ERROR", "Database connection failed.", exc_info=e)
        logger.log_to_db("ERROR", "Database connection failed.", module="status_routes")
        raise DatabaseUnavailableError("Database connection failed.") from e


# Error handler for DatabaseUnavailableError
@status_bp.app_errorhandler(DatabaseUnavailableError)
def handle_database_unavailable_error(error):
    """
    Error handler for DatabaseUnavailableError.
    """
    logger.log_to_console("ERROR", f"Database unavailable error: {error}")
    return (
        format_error_response(
            status=500,
            error_code="DATABASE_UNAVAILABLE",
            message="The database is not accessible at this time.",
            details=str(error),
        ),
        500,
    )

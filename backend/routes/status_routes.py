from flask import Blueprint, jsonify
from sqlalchemy.sql import text
from sqlalchemy.exc import OperationalError
from backend.db import db
from backend.utils.error_handling.error_handling import format_error_response, log_error
from backend.utils.logger import CentralizedLogger

# Initialize the logger
logger = CentralizedLogger("status_routes")

# Create a blueprint for status routes
status_bp = Blueprint("status", __name__)


@status_bp.route("/status", methods=["GET"])
def health_check():
    """
    Health check endpoint to verify API and database status.
    Returns:
        JSON response indicating API and database health.
    """
    try:
        # Check database connection
        db.session.execute(text("SELECT 1"))
        logger.log_to_console("INFO", "Health check passed: Database connected.")
        return jsonify({"status": "ok", "database": "connected"}), 200
    except OperationalError as e:
        logger.log_to_console("ERROR", "Database connection failed.", exc_info=e)
        log_error(e, module="status_routes")
        return (
            format_error_response(
                status=500,
                error_code="DATABASE_CONNECTION_FAILED",
                message="The database is not accessible at this time.",
                details=str(e),
            ),
            500,
        )
    except Exception as e:
        logger.log_to_console("ERROR", "Unhandled exception during health check.", exc_info=e)
        log_error(e, module="status_routes")
        return (
            format_error_response(
                status=500,
                error_code="HEALTH_CHECK_ERROR",
                message="An error occurred during the health check.",
                details=str(e),
            ),
            500,
        )

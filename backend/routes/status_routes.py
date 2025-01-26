"""
Status routes: Check API and DB connectivity.
"""

# pylint: disable=broad-exception-caught

from flask import Blueprint, jsonify
from sqlalchemy.sql import text
from sqlalchemy.exc import OperationalError
from backend.db import db
from backend.utils.error_handling.error_handling import format_error_response, log_error
from backend.utils.logger import CentralizedLogger

logger = CentralizedLogger("status_routes")
status_bp = Blueprint("status", __name__)


@status_bp.route("/status", methods=["GET"])
def health_check():
    """
    Health check endpoint to verify API and database status.
    Returns:
        JSON indicating API and DB health.
    """
    try:
        db.session.execute(text("SELECT 1"))
        logger.log_to_console("INFO", "Health check passed: DB connected.")
        return jsonify({"status": "ok", "database": "connected"}), 200
    except OperationalError as op_err:
        logger.log_to_console("ERROR", "Database connection failed.", exc_info=op_err)
        log_error(op_err, module="status_routes")
        return (
            format_error_response(
                status=500,
                error_code="DATABASE_CONNECTION_FAILED",
                message="The database is not accessible at this time.",
                details=str(op_err),
            ),
            500,
        )
    except Exception as exc:
        logger.log_to_console(
            "ERROR", "Unhandled exception during health check.", exc_info=exc
        )
        log_error(exc, module="status_routes")
        return (
            format_error_response(
                status=500,
                error_code="HEALTH_CHECK_ERROR",
                message="An error occurred during the health check.",
                details=str(exc),
            ),
            500,
        )

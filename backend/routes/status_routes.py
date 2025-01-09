from flask import Blueprint, jsonify, current_app
from sqlalchemy.sql import text
from sqlalchemy.exc import OperationalError
from backend.db import db
from backend.utils.error_handling.routes.errors import DatabaseUnavailableError, format_error_response

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
        return jsonify({
            "status": "ok",
            "database": "connected"
        })
    except OperationalError as e:
        current_app.logger.error("Database connection failed.", exc_info=e)
        raise DatabaseUnavailableError("Database connection failed.") from e

# Error handler for DatabaseUnavailableError
@status_bp.app_errorhandler(DatabaseUnavailableError)
def handle_database_unavailable_error(error):
    """
    Error handler for DatabaseUnavailableError.
    """
    return format_error_response(
        status=500,
        error_code="DATABASE_UNAVAILABLE",
        message="The database is not accessible at this time.",
        details=str(error)
    ), 500

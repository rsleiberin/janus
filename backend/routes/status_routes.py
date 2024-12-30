from flask import Blueprint, jsonify
from sqlalchemy.sql import text
from backend.models import db


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
        database_status = "connected"
    except Exception as e:
        database_status = f"error: {str(e)}"

    # Debugging logs
    print("Database status in /status route:", database_status)
    print("Database session bind:", db.session.bind)  # Check if session is bound
    print("Database engine bound:", db.engine if hasattr(db, 'engine') else None)

    return jsonify({
        "status": "ok",
        "database": database_status
    })


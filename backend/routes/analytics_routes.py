"""
Routes for creating, fetching, and deleting analytics records.
"""

# pylint: disable=broad-exception-caught

from flask import Blueprint, jsonify, request
from backend.db import db
from backend.models import Analytics
from backend.utils.error_handling.error_handling import format_error_response, log_error
from backend.utils.logger import CentralizedLogger

logger = CentralizedLogger("analytics_routes")
analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("", methods=["POST"])
def create_analytics_entry():
    """
    Create a new analytics entry.
    Expects JSON: { "data": <some JSON>, "research_topic": "optional string" }
    """
    try:
        logger.log_to_console("INFO", "Creating a new analytics record.")
        incoming = request.get_json() or {}
        data = incoming.get("data")
        topic = incoming.get("research_topic")

        if not data:
            raise ValueError("Analytics data is required.")

        analytics_entry = Analytics(data=data, research_topic=topic)
        db.session.add(analytics_entry)
        db.session.commit()

        logger.log_to_console("INFO", "Analytics record created successfully.")
        return (
            jsonify(
                {
                    "id": analytics_entry.id,
                    "message": "Analytics entry created successfully.",
                }
            ),
            201,
        )
    except ValueError as err:
        logger.log_to_console("WARNING", "Invalid analytics request.", details=str(err))
        log_error(err, module="analytics_routes")
        return (
            format_error_response(
                status=400,
                error_code="INVALID_ANALYTICS_REQUEST",
                message="The provided analytics data is invalid.",
                details=str(err),
            ),
            400,
        )
    except Exception as exc:
        logger.log_to_console(
            "ERROR", "Unexpected error creating analytics entry.", exc_info=exc
        )
        log_error(exc, module="analytics_routes")
        return (
            format_error_response(
                status=500,
                error_code="CREATE_ANALYTICS_ERROR",
                message="Unexpected error occurred while creating analytics entry.",
                details=str(exc),
            ),
            500,
        )


@analytics_bp.route("", methods=["GET"])
def get_analytics_records():
    """
    Fetch all analytics records.
    """
    try:
        logger.log_to_console("INFO", "Fetching all analytics records.")
        records = Analytics.query.all()
        serialized = []
        for record in records:
            serialized.append(
                {
                    "id": record.id,
                    "data": record.data,
                    "research_topic": record.research_topic,
                    "created_at": record.created_at.isoformat(),
                }
            )

        logger.log_to_console("INFO", f"Fetched {len(serialized)} analytics records.")
        return jsonify({"analytics": serialized}), 200

    except Exception as exc:
        logger.log_to_console(
            "ERROR", "Unexpected error fetching analytics records.", exc_info=exc
        )
        log_error(exc, module="analytics_routes")
        return (
            format_error_response(
                status=500,
                error_code="FETCH_ANALYTICS_ERROR",
                message="Unexpected error while fetching analytics records.",
                details=str(exc),
            ),
            500,
        )


@analytics_bp.route("/<int:record_id>", methods=["GET"])
def fetch_single_analytics_entry(record_id):
    """
    Fetch a single analytics entry by ID.
    """
    try:
        logger.log_to_console("INFO", f"Fetching analytics record ID {record_id}.")
        record = db.session.get(Analytics, record_id)
        if not record:
            raise ValueError(f"Analytics record with ID {record_id} not found.")

        serialized = {
            "id": record.id,
            "data": record.data,
            "research_topic": record.research_topic,
            "created_at": record.created_at.isoformat(),
        }
        logger.log_to_console("INFO", f"Fetched analytics record ID {record_id}.")
        return jsonify(serialized), 200

    except ValueError as err:
        logger.log_to_console("WARNING", str(err))
        log_error(err, module="analytics_routes")
        return (
            format_error_response(
                status=404,
                error_code="RECORD_NOT_FOUND",
                message="Requested analytics record not found.",
                details=str(err),
            ),
            404,
        )
    except Exception as exc:
        logger.log_to_console("ERROR", "Error fetching analytics record.", exc_info=exc)
        log_error(exc, module="analytics_routes")
        return (
            format_error_response(
                status=500,
                error_code="FETCH_SINGLE_ANALYTICS_ERROR",
                message="Unexpected error fetching the analytics record.",
                details=str(exc),
            ),
            500,
        )


@analytics_bp.route("/<int:record_id>", methods=["DELETE"])
def delete_analytics_record(record_id):
    """
    Delete an analytics record by ID.
    """
    try:
        logger.log_to_console("INFO", f"Deleting analytics record ID {record_id}.")
        record = db.session.get(Analytics, record_id)
        if not record:
            raise ValueError(f"Analytics record with ID {record_id} not found.")

        db.session.delete(record)
        db.session.commit()

        logger.log_to_console("INFO", f"Analytics record {record_id} deleted.")
        return jsonify({"message": "Analytics entry deleted successfully."}), 200

    except ValueError as err:
        logger.log_to_console("WARNING", str(err))
        log_error(err, module="analytics_routes")
        return (
            format_error_response(
                status=404,
                error_code="RECORD_NOT_FOUND",
                message="Requested analytics record not found.",
                details=str(err),
            ),
            404,
        )
    except Exception as exc:
        logger.log_to_console("ERROR", "Error deleting analytics record.", exc_info=exc)
        log_error(exc, module="analytics_routes")
        return (
            format_error_response(
                status=500,
                error_code="DELETE_ANALYTICS_ERROR",
                message="Unexpected error deleting the analytics record.",
                details=str(exc),
            ),
            500,
        )

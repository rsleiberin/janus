from flask import Blueprint, jsonify, request
from backend.models import Analytics, db
from backend.utils.error_handling.error_handling import format_error_response, log_error
from backend.utils.logger import CentralizedLogger

logger = CentralizedLogger("analytics_routes")

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")


@analytics_bp.route("", methods=["POST"])
def create_analytics_entry():
    """
    Create a new analytics entry.
    """
    try:
        logger.log_to_console("INFO", "Creating a new analytics record.")
        data = request.json.get("data")
        research_topic = request.json.get("research_topic")

        if not data:
            raise ValueError("Analytics data is required.")

        analytics_entry = Analytics(data=data, research_topic=research_topic)
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

    except ValueError as e:
        logger.log_to_console("WARNING", "Invalid analytics request.", details=str(e))
        log_error(e, module="analytics_routes")
        return (
            format_error_response(
                status=400,
                error_code="INVALID_ANALYTICS_REQUEST",
                message="The provided analytics data is invalid.",
                details=str(e),
            ),
            400,
        )

    except Exception as e:
        logger.log_to_console(
            "ERROR", "Unexpected error creating analytics entry.", exc_info=e
        )
        log_error(e, module="analytics_routes")
        return (
            format_error_response(
                status=500,
                error_code="CREATE_ANALYTICS_ERROR",
                message="An unexpected error occurred while creating the analytics entry.",
                details=str(e),
            ),
            500,
        )


@analytics_bp.route("", methods=["GET"])
def get_analytics_records():
    """
    Endpoint to fetch all analytics records.
    """
    try:
        logger.log_to_console("INFO", "Fetching all analytics records.")
        records = Analytics.query.all()
        serialized_records = [
            {
                "id": record.id,
                "data": record.data,
                "research_topic": record.research_topic,
                "created_at": record.created_at.isoformat(),
            }
            for record in records
        ]

        logger.log_to_console(
            "INFO", f"Fetched {len(serialized_records)} analytics records."
        )
        return jsonify({"analytics": serialized_records}), 200

    except Exception as e:
        logger.log_to_console(
            "ERROR", "Unexpected error fetching analytics records.", exc_info=e
        )
        log_error(e, module="analytics_routes")
        return (
            format_error_response(
                status=500,
                error_code="FETCH_ANALYTICS_ERROR",
                message="An unexpected error occurred while fetching analytics records.",
                details=str(e),
            ),
            500,
        )


@analytics_bp.route("/<int:record_id>", methods=["GET"])
def fetch_single_analytics_entry(record_id):
    """
    Fetch a single analytics entry by ID.
    """
    try:
        logger.log_to_console(
            "INFO", f"Fetching analytics record with ID: {record_id}."
        )
        record = db.session.get(Analytics, record_id)
        if not record:
            raise ValueError(f"Analytics record with ID {record_id} not found.")

        serialized_record = {
            "id": record.id,
            "data": record.data,
            "research_topic": record.research_topic,
            "created_at": record.created_at.isoformat(),
        }
        logger.log_to_console("INFO", f"Fetched analytics record with ID: {record_id}.")
        return jsonify(serialized_record), 200

    except ValueError as e:
        logger.log_to_console("WARNING", str(e))
        log_error(e, module="analytics_routes")
        return (
            format_error_response(
                status=404,
                error_code="RECORD_NOT_FOUND",
                message="The requested analytics record could not be found.",
                details=str(e),
            ),
            404,
        )

    except Exception as e:
        logger.log_to_console(
            "ERROR", "Unexpected error fetching analytics record.", exc_info=e
        )
        log_error(e, module="analytics_routes")
        return (
            format_error_response(
                status=500,
                error_code="FETCH_SINGLE_ANALYTICS_ERROR",
                message="An unexpected error occurred while fetching the analytics record.",
                details=str(e),
            ),
            500,
        )


@analytics_bp.route("/<int:record_id>", methods=["DELETE"])
def delete_analytics_record(record_id):
    """
    Endpoint to delete an analytics record by ID.
    """
    try:
        logger.log_to_console(
            "INFO", f"Deleting analytics record with ID: {record_id}."
        )
        record = db.session.get(Analytics, record_id)
        if not record:
            raise ValueError(f"Analytics record with ID {record_id} not found.")

        db.session.delete(record)
        db.session.commit()

        logger.log_to_console(
            "INFO", f"Analytics record {record_id} deleted successfully."
        )
        return jsonify({"message": "Analytics entry deleted successfully."}), 200

    except ValueError as e:
        logger.log_to_console("WARNING", str(e))
        log_error(e, module="analytics_routes")
        return (
            format_error_response(
                status=404,
                error_code="RECORD_NOT_FOUND",
                message="The requested analytics record could not be found.",
                details=str(e),
            ),
            404,
        )

    except Exception as e:
        logger.log_to_console(
            "ERROR", "Unexpected error deleting analytics record.", exc_info=e
        )
        log_error(e, module="analytics_routes")
        return (
            format_error_response(
                status=500,
                error_code="DELETE_ANALYTICS_ERROR",
                message="An unexpected error occurred while deleting the analytics record.",
                details=str(e),
            ),
            500,
        )

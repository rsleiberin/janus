from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.error_handling import (
    handle_general_error,
    log_error,
    format_error_response,
)

logger = CentralizedLogger("log_routes")

log_bp = Blueprint("log_routes", __name__)


@log_bp.route("/", methods=["GET"])
@jwt_required()
def get_logs():
    """Retrieve logs."""
    try:
        user_identity = get_jwt_identity()
        logger.log_to_console(
            "INFO", f"Log retrieval initiated by user: {user_identity}"
        )

        # Example: Simulated log retrieval logic
        logs = [
            {"id": 1, "message": "System started."},
            {"id": 2, "message": "User logged in."},
        ]
        logger.log_to_console(
            "INFO", "Logs retrieved successfully.", meta_data={"user_id": user_identity}
        )

        return jsonify({"logs": logs}), 200
    except Exception as e:  # pylint: disable=broad-exception-caught
        return handle_general_error(e, meta_data={"route": "get_logs"})


@log_bp.route("/<int:log_id>", methods=["GET"])
@jwt_required()
def get_log_by_id(log_id):
    """Retrieve a specific log by its ID."""
    try:
        user_identity = get_jwt_identity()
        logger.log_to_console(
            "INFO",
            f"Log detail retrieval by user: {user_identity}",
            meta_data={"log_id": log_id},
        )

        # Example: Simulated log retrieval logic
        if log_id not in [1, 2]:  # Simulated check for existing log IDs
            logger.log_to_console(
                "WARNING",
                "Log not found.",
                meta_data={"log_id": log_id, "user_id": user_identity},
            )
            return (
                format_error_response(
                    status=404,
                    error_code="LOG_NOT_FOUND",
                    message=f"Log with ID {log_id} not found.",
                    meta_data={"log_id": log_id},
                ),
                404,
            )

        log = {"id": log_id, "message": f"Log entry {log_id}"}
        logger.log_to_console(
            "INFO",
            "Log retrieved successfully.",
            meta_data={"log_id": log_id, "user_id": user_identity},
        )

        return jsonify({"log": log}), 200
    except Exception as e:  # pylint: disable=broad-exception-caught
        log_error(e, module="log_routes", meta_data={"log_id": log_id})
        return handle_general_error(
            e, meta_data={"route": "get_log_by_id", "log_id": log_id}
        )


# Future Expansion
# System monitoring features, including CPU, memory, and disk usage metrics.
# Evaluate psutil or alternative libraries before implementation.
# These features will require dedicated helper functions and schema updates
# if needed.

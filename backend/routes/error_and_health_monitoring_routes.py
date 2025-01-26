"""
Error & Health Monitoring Routes
"""

# pylint: disable=broad-exception-caught,R1710

from flask import Blueprint, jsonify, request
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.error_handling import (
    log_error,
    format_error_response,
    handle_route_error,
)

error_and_health_bp = Blueprint("error_and_health", __name__)
logger = CentralizedLogger("error_and_health_routes")


@error_and_health_bp.route("/health", methods=["GET"])
def health_check():
    """
    Returns system health status.
    """
    try:
        logger.log_to_console("INFO", "Health check requested.")
        status = {"database": "Available", "service": "Operational"}
        logger.log_to_console("INFO", "Health check success.", status=status)
        return jsonify({"status": "healthy", "details": status}), 200
    except Exception as exc:
        log_error(exc, module="health_check")
        return (
            format_error_response(
                status=500,
                error_code="HEALTH_CHECK_FAILED",
                message="Health check failed due to an error.",
                details=str(exc),
            ),
            500,
        )


@error_and_health_bp.route("/simulate-error", methods=["POST"])
def simulate_error():
    """
    Endpoint to simulate different errors for testing.
    JSON: { "error_type": "custom" | "db" | ... }
    """
    try:
        error_type = request.json.get("error_type")
        if error_type == "custom":
            logger.log_to_console("INFO", "Simulating custom error.")
            raise ValueError("This is a simulated custom error.")
        if error_type == "db":
            logger.log_to_console("INFO", "Simulating DB health check failure.")
            raise RuntimeError("Simulated DB health check failure.")
        logger.log_to_console("INFO", "Simulating generic error.")
        raise RuntimeError("Simulated generic error.")
    except ValueError as val_err:
        logger.log_to_console(
            "ERROR", "Simulated custom error occurred.", details=str(val_err)
        )
        return (
            format_error_response(
                status=500,
                error_code="SIMULATED_ERROR",
                message="Simulated error for testing purposes.",
                details=str(val_err),
            ),
            500,
        )
    except Exception as exc:
        return handle_route_error(exc)


@error_and_health_bp.route("/simulate-unhandled-error", methods=["GET"])
def simulate_unhandled_error():
    """
    Simulate an unhandled exception for testing.
    """
    try:
        logger.log_to_console("ERROR", "Simulating unhandled exception.")
        raise RuntimeError("Simulated unhandled exception for testing.")
    except RuntimeError as exc:
        return handle_route_error(exc)

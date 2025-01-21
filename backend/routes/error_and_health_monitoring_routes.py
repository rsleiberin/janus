from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.error_handling import (
    log_error,
    format_error_response,
)
from backend.utils.error_handling.routes.errors import (
    handle_route_error,
    HealthCheckError,
)

# Initialize blueprint
error_and_health_bp = Blueprint("error_and_health", __name__)

# Initialize logger
logger = CentralizedLogger("error_and_health_routes")


@error_and_health_bp.route("/health", methods=["GET"])
def health_check():
    """
    Endpoint to check system health.
    Returns:
        JSON response with health status.
    """
    try:
        logger.log_to_console("INFO", "Health check requested.")
        status = {
            "database": "Available",
            "service": "Operational",
        }
        logger.log_to_console(
            "INFO", "Health check completed successfully.", status=status
        )
        return jsonify({"status": "healthy", "details": status}), 200

    except Exception as e:  # pylint: disable=broad-exception-caught
        log_error(e, module="health_check")
        raise HealthCheckError("Health check failed.") from e  # pylint: disable=broad-exception-raised


@error_and_health_bp.route("/simulate-error", methods=["POST"])
def simulate_error():
    """
    Endpoint to simulate an error for testing purposes.
    Returns:
        JSON response with simulated error message.
    """
    try:
        error_type = request.json.get("error_type")
        if error_type == "custom":
            logger.log_to_console("INFO", "Simulating custom error.")
            raise ValueError("This is a simulated custom error.")
        if error_type == "db":  # Changed 'elif' to 'if' to comply with no-else-raise
            logger.log_to_console("INFO", "Simulating database health check failure.")
            raise HealthCheckError("Simulated database health check failure.")
        else:
            logger.log_to_console("INFO", "Simulating generic error.")
            raise Exception("Simulated generic error.")  # pylint: disable=broad-exception-raised
    except ValueError as e:
        logger.log_to_console(
            "ERROR", "Simulated custom error occurred.", details=str(e)
        )
        return (
            format_error_response(
                status=500,
                error_code="SIMULATED_ERROR",
                message="This is a simulated error for testing purposes.",
                details=str(e),
            ),
            500,
        )
    except Exception as e:  # pylint: disable=broad-exception-caught
        return handle_route_error(e)


@error_and_health_bp.route("/simulate-unhandled-error", methods=["GET"])
def simulate_unhandled_error():
    """
    Endpoint to simulate an unhandled exception for testing purposes.
    Raises:
        HealthCheckError: Simulated unhandled exception.
    """
    try:
        logger.log_to_console("ERROR", "Simulating unhandled exception.")
        raise HealthCheckError("Simulated unhandled exception for testing.")
    except HealthCheckError as e:
        return handle_route_error(e)

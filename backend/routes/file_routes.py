from flask import Blueprint, jsonify, request
import os
from backend.utils.error_handling.error_handling import format_error_response, log_error
from backend.utils.logger import CentralizedLogger

# Initialize the logger
logger = CentralizedLogger("file_routes")

BASE_DIRECTORY = "/home/tank/janus"
file_bp = Blueprint("file", __name__)


@file_bp.route("/files", methods=["GET"])
def list_files():
    """
    List all files in the project directory.

    Returns:
        JSON response containing a list of all files.
    """
    try:
        files_list = [
            os.path.join(root, file)
            for root, _, files in os.walk(BASE_DIRECTORY)
            for file in files
        ]

        logger.log_to_console("INFO", "Listed all files in the directory.")
        return jsonify(files=files_list), 200

    except Exception as e:
        logger.log_to_console("ERROR", "Error listing files.", exc_info=e)
        log_error(e, module="file_routes")
        return (
            format_error_response(
                status=500,
                error_code="LIST_FILES_ERROR",
                message="An error occurred while listing files.",
                details=str(e),
            ),
            500,
        )


@file_bp.route("/files/content", methods=["POST"])
def read_file():
    """
    Read the content of a specific file.

    Expects:
        JSON payload with "path" as the relative file path.

    Returns:
        JSON response containing the file content.
    """
    try:
        relative_path = request.json.get("path")
        if not relative_path:
            raise ValueError("File path not provided.")

        # Resolve and validate the file path
        full_path = os.path.abspath(os.path.join(BASE_DIRECTORY, relative_path))
        if not full_path.startswith(BASE_DIRECTORY):
            raise PermissionError("Access denied: Invalid file path.")

        with open(full_path, "r", encoding="utf-8") as file:
            content = file.read()

        logger.log_to_console("INFO", f"Read file: {relative_path}")
        return jsonify(content=content), 200

    except FileNotFoundError:
        error_message = f"The requested file was not found: {relative_path}"
        logger.log_to_console("WARNING", error_message)
        log_error(error_message, module="file_routes")
        return (
            format_error_response(
                status=404,
                error_code="FILE_NOT_FOUND",
                message="The requested file could not be found.",
                details=error_message,
            ),
            404,
        )

    except PermissionError as e:
        logger.log_to_console("ERROR", "File access error.", exc_info=e)
        log_error(e, module="file_routes", meta_data={"path": relative_path})
        return (
            format_error_response(
                status=403,
                error_code="FILE_ACCESS_DENIED",
                message="Access denied to the requested file.",
                details=str(e),
            ),
            403,
        )

    except ValueError as e:
        logger.log_to_console("ERROR", "File path validation error.", exc_info=e)
        log_error(e, module="file_routes", meta_data={"path": relative_path})
        return (
            format_error_response(
                status=400,
                error_code="INVALID_FILE_PATH",
                message="File path is required and must be valid.",
                details=str(e),
            ),
            400,
        )

    except Exception as e:
        logger.log_to_console("ERROR", "Unexpected error reading file.", exc_info=e)
        log_error(e, module="file_routes")
        return (
            format_error_response(
                status=500,
                error_code="READ_FILE_ERROR",
                message="An unexpected error occurred while reading the file.",
                details=str(e),
            ),
            500,
        )

from flask import Blueprint, jsonify, request
import os
from backend.utils.error_handling.routes.errors import (
    FileAccessError,
    FileNotFoundErrorCustom,
    handle_route_error,
)
from backend.utils.logger import CentralizedLogger

# Initialize the logger
logger = CentralizedLogger("file_routes")

BASE_DIRECTORY = "/home/tank/janus"
file_bp = Blueprint("file", __name__)


@file_bp.route("/files", methods=["GET"])
def list_files():
    """
    List all files in the project directory.
    """
    try:
        files_list = []
        for root, dirs, files in os.walk(BASE_DIRECTORY):
            for file in files:
                files_list.append(os.path.join(root, file))

        logger.log_to_console("INFO", "Listed all files in the directory.")
        return jsonify(files=files_list)
    except Exception as e:
        logger.log_to_console("ERROR", "Unexpected error listing files", exc_info=e)
        logger.log_to_db(
            "ERROR", "Unexpected error listing files", module="file_routes"
        )
        return handle_route_error(e)


@file_bp.route("/files/content", methods=["POST"])
def read_file():
    """
    Read the content of a specific file.
    """
    try:
        relative_path = request.json.get("path", "")
        if not relative_path:
            raise FileAccessError("File path not provided.")

        # Resolve and validate file path
        full_path = os.path.abspath(os.path.join(BASE_DIRECTORY, relative_path))
        if not full_path.startswith(BASE_DIRECTORY):
            raise FileAccessError("Access denied: Invalid file path.")

        with open(full_path, "r") as file:
            content = file.read()

        logger.log_to_console("INFO", f"Read file: {relative_path}")
        logger.log_to_db(
            "INFO", f"File read successfully: {relative_path}", module="file_routes"
        )
        return jsonify(content=content)

    except FileNotFoundError:
        # Properly map the error with a custom message
        error = FileNotFoundErrorCustom(
            f"The requested file was not found: {relative_path}"
        )
        logger.log_to_console("WARNING", str(error))
        logger.log_to_db("WARNING", str(error), module="file_routes")
        return handle_route_error(error)

    except FileAccessError as e:
        logger.log_to_console("ERROR", "File access error", exc_info=e)
        logger.log_to_db(
            "ERROR", f"File access error: {relative_path}", module="file_routes"
        )
        return handle_route_error(e)

    except Exception as e:
        logger.log_to_console("ERROR", "Unexpected error reading file", exc_info=e)
        logger.log_to_db("ERROR", "Unexpected error reading file", module="file_routes")
        return handle_route_error(RuntimeError("An unexpected error occurred."))

from flask import Blueprint, jsonify, request, current_app
import os
from backend.utils.error_handling.routes.errors import (
    FileAccessError,
    FileNotFoundErrorCustom,
    handle_route_error,
)

BASE_DIRECTORY = "/home/tank/janus"
file_bp = Blueprint("file", __name__)

@file_bp.route('/files', methods=['GET'])
def list_files():
    """
    List all files in the project directory.
    """
    try:
        files_list = []
        for root, dirs, files in os.walk(BASE_DIRECTORY):
            for file in files:
                files_list.append(os.path.join(root, file))

        current_app.logger.info("Listed all files in the directory.")
        return jsonify(files=files_list)
    except Exception as e:
        current_app.logger.error("Unexpected error listing files", exc_info=e)
        return handle_route_error(e)

@file_bp.route('/files/content', methods=['POST'])
def read_file():
    """
    Read the content of a specific file.
    """
    try:
        relative_path = request.json.get('path', '')
        if not relative_path:
            raise FileAccessError("File path not provided.")

        # Resolve and validate file path
        full_path = os.path.abspath(os.path.join(BASE_DIRECTORY, relative_path))
        if not full_path.startswith(BASE_DIRECTORY):
            raise FileAccessError("Access denied: Invalid file path.")

        with open(full_path, 'r') as file:
            content = file.read()

        current_app.logger.info(f"Read file: {relative_path}")
        return jsonify(content=content)
    except FileNotFoundError:
        current_app.logger.warning(f"File not found: {relative_path}")
        return handle_route_error(FileNotFoundErrorCustom("The requested file was not found."))
    except FileAccessError as e:
        current_app.logger.error("File access error", exc_info=e)
        return handle_route_error(e)
    except Exception as e:
        current_app.logger.error("Unexpected error reading file", exc_info=e)
        # Use handle_route_error for unexpected errors
        return handle_route_error(RuntimeError("An unexpected error occurred."))


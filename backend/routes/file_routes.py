from flask import Blueprint, jsonify, request
import os
from backend.models import db


file_bp = Blueprint("file", __name__)

@file_bp.route('/files', methods=['GET'])
def list_files():
    """List all files in the project directory."""
    base_directory = "/home/tank/janus"
    files_list = []

    for root, dirs, files in os.walk(base_directory):
        for file in files:
            files_list.append(os.path.join(root, file))

    return jsonify(files=files_list)

@file_bp.route('/files/content', methods=['POST'])
def read_file():
    """Read the content of a specific file."""
    base_directory = "/home/tank/janus"
    relative_path = request.json.get('path', '')
    full_path = os.path.join(base_directory, relative_path)

    if not full_path.startswith(base_directory):
        return jsonify(error="Access denied: Invalid file path"), 403

    try:
        with open(full_path, 'r') as file:
            content = file.read()
        return jsonify(content=content)
    except FileNotFoundError:
        return jsonify(error="File not found"), 404
    except Exception as e:
        return jsonify(error=f"An unexpected error occurred: {str(e)}"), 500

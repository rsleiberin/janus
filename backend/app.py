import os
from flask import Flask, jsonify, request
from routes.status_routes import status_bp  # Import the status blueprint
from models import db  # Import the SQLAlchemy instance

# Initialize the Flask app
app = Flask(__name__)

# Resolve the absolute path to the database file, relative to this file's location
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, "instance/image_processing.db")

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"  # Absolute path for SQLite
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database
db.init_app(app)

# Register blueprints
app.register_blueprint(status_bp)

# Root route for health checks and basic connectivity
@app.route('/')
def home():
    """
    WHY: Provides a simple endpoint to verify the API is running. Useful for monitoring and basic testing.

    Returns:
        JSON: {"message": "Welcome to the Janus API!"}
    """
    return jsonify(message="Welcome to the Janus API!")

# Route to list all files in a specific directory
@app.route('/files', methods=['GET'])
def list_files():
    """
    WHY: Offers a way to explore files in the project directory, supporting dynamic file-based operations.

    Returns:
        JSON: {"files": [<list of file paths>]}

    Raises:
        - 500: If an unexpected error occurs during directory traversal.
    """
    base_directory = "/home/tank/janus"  # Base directory for file access
    files_list = []

    # Recursively collect all file paths
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            files_list.append(os.path.join(root, file))
    
    return jsonify(files=files_list)

# Route to read the content of a specific file
@app.route('/files/content', methods=['POST'])
def read_file():
    """
    WHY: Enables secure file access to retrieve content dynamically, critical for data-driven workflows.

    Input:
        JSON: {"path": "<relative path to file>"}

    Output:
        JSON:
            {"content": "<file content>"} (on success)
            {"error": "<error message>"} (on failure)

    Raises:
        - 403: If the requested file path is outside the base directory.
        - 404: If the file does not exist.
        - 500: If an unexpected error occurs during file reading.
    """
    base_directory = "/home/tank/janus"
    relative_path = request.json.get('path', '')  # Relative path input from the request
    full_path = os.path.join(base_directory, relative_path)

    # WHY: Prevents unauthorized access to files outside the project directory
    if not full_path.startswith(base_directory):
        return jsonify(error="Access denied: Invalid file path"), 403

    try:
        # Read and return the file content
        with open(full_path, 'r') as file:
            content = file.read()
        return jsonify(content=content)
    except FileNotFoundError:
        return jsonify(error="File not found"), 404
    except Exception as e:
        return jsonify(error=f"An unexpected error occurred: {str(e)}"), 500

# Entry point for the Flask application
if __name__ == '__main__':
    # WHY: Runs the app in debug mode for local development, accessible on all network interfaces
    app.run(debug=True, host='0.0.0.0', port=5000)

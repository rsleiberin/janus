import os
from flask import Flask, jsonify, request

# Initialize the Flask app
app = Flask(__name__)

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

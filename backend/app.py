import os

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify(message="Hello, World!")

@app.route('/files', methods=['GET'])
def list_files():
    files_list = []
    for root, dirs, files in os.walk("/home/tank/janus"):
        for file in files:
            files_list.append(os.path.join(root, file))
    return jsonify(files_list)

@app.route('/files/content', methods=['POST'])
def read_file():
    relative_path = request.json.get('path')
    full_path = os.path.join("/home/tank/janus", relative_path)

    # Security check to prevent accessing files outside the project directory
    if not full_path.startswith("/home/tank/janus"):
        return jsonify({"error": "Access denied"}), 403

    try:
        with open(full_path, 'r') as file:
            content = file.read()
        return jsonify({"content": content})
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


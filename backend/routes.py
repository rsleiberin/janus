from flask import Blueprint, jsonify

api = Blueprint('api', __name__)

@api.route('/test')
def test_route():
    return jsonify({"message": "This is a test endpoint."})

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from backend.db import db
from backend.models import Image
from backend.utils.logger import CentralizedLogger
from backend.utils.file_handler import construct_file_path, write_file, delete_file
import uuid

image_bp = Blueprint("image_routes", __name__)
logger = CentralizedLogger("image_routes")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@image_bp.route("/upload", methods=["POST"])
def upload_image():
    try:
        user_id = request.headers.get("User-ID")
        logger.log_to_console("INFO", "Image upload initiated.", user_id=user_id)

        if "file" not in request.files:
            return jsonify({"error": "No file part in the request."}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No selected file."}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            write_file(user_id, unique_filename, file.read(), mode="wb")

            new_image = Image(filename=unique_filename, user_id=user_id)
            db.session.add(new_image)
            db.session.commit()

            logger.log_to_console("INFO", "Image uploaded successfully.", user_id=user_id, filename=unique_filename)
            return jsonify({"message": "Image uploaded successfully.", "image_id": new_image.id}), 201

        return jsonify({"error": "Unsupported file type."}), 400
    except Exception as e:
        logger.log_to_console("ERROR", "Error during image upload.", error=str(e))
        return jsonify({"error": "An error occurred while uploading the image."}), 500

@image_bp.route("/<int:image_id>", methods=["GET"])
def get_image(image_id):
    try:
        image = Image.query.get(image_id)
        if not image:
            return jsonify({"error": "Image not found."}), 404

        file_path = construct_file_path(image.user_id, image.filename)
        return jsonify({
            "id": image.id,
            "filename": image.filename,
            "path": file_path,
            "uploaded_by": image.user_id,
            "uploaded_at": image.created_at
        }), 200
    except Exception as e:
        logger.log_to_console("ERROR", "Error retrieving image metadata.", error=str(e))
        return jsonify({"error": "An error occurred while retrieving the image metadata."}), 500

@image_bp.route("/<int:image_id>", methods=["DELETE"])
def delete_image(image_id):
    try:
        user_id = request.headers.get("User-ID")
        image = Image.query.get(image_id)
        if not image:
            return jsonify({"error": "Image not found."}), 404

        delete_file(image.user_id, image.filename)

        db.session.delete(image)
        db.session.commit()

        logger.log_to_console("INFO", "Image deleted successfully.", user_id=user_id, image_id=image_id)
        return jsonify({"message": "Image deleted successfully."}), 200
    except Exception as e:
        logger.log_to_console("ERROR", "Error during image deletion.", error=str(e))
        return jsonify({"error": "An error occurred while deleting the image."}), 500

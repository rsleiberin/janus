"""
Image routes: upload, retrieve, and delete images.
"""

# pylint: disable=broad-exception-caught

import uuid
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from backend.db import db
from backend.models import Image, Admin
from backend.utils.logger import CentralizedLogger
from backend.utils.file_handler import construct_file_path, write_file, delete_file

logger = CentralizedLogger("image_routes")
image_bp = Blueprint("image_routes", __name__, url_prefix="/images")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def is_admin_user(user_id: int) -> bool:
    """
    Checks if the given user_id belongs to an Admin record.
    """
    admin_rec = db.session.query(Admin).filter_by(user_id=user_id).first()
    return admin_rec is not None


@image_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_image():
    """
    Upload an image file for the current user.
    """
    try:
        current_user = get_jwt_identity()
        user_id = current_user["id"]
        file_obj = request.files.get("file")

        if not file_obj or file_obj.filename == "":
            return jsonify({"error": "No selected file."}), 400

        if file_obj and allowed_file(file_obj.filename):
            original_filename = secure_filename(file_obj.filename)
            unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
            file_contents = file_obj.read()

            write_file(user_id, unique_filename, file_contents, mode="wb")

            new_image = Image(filename=unique_filename, user_id=user_id)
            db.session.add(new_image)
            db.session.commit()

            logger.log_to_console(
                "INFO", "Image uploaded.", user_id=user_id, filename=unique_filename
            )
            return (
                jsonify({"message": "Image uploaded.", "image_id": new_image.id}),
                201,
            )

        return jsonify({"error": "Unsupported file type."}), 400
    except Exception as exc:
        logger.log_to_console("ERROR", "Error uploading image.", error=str(exc))
        return jsonify({"error": "An error occurred while uploading the image."}), 500


@image_bp.route("/<int:image_id>", methods=["GET"])
@jwt_required()
def get_image(image_id):
    """
    Retrieve metadata for an image by its ID.
    """
    try:
        image_obj = db.session.get(Image, image_id)
        if not image_obj:
            return jsonify({"error": "Image not found."}), 404

        file_path = construct_file_path(image_obj.user_id, image_obj.filename)
        return (
            jsonify(
                {
                    "id": image_obj.id,
                    "filename": image_obj.filename,
                    "path": file_path,
                    "uploaded_by": image_obj.user_id,
                    "uploaded_at": image_obj.created_at.isoformat(),
                }
            ),
            200,
        )
    except Exception as exc:
        logger.log_to_console(
            "ERROR", "Error retrieving image metadata.", error=str(exc)
        )
        return jsonify({"error": "Error retrieving the image metadata."}), 500


@image_bp.route("/<int:image_id>", methods=["DELETE"])
@jwt_required()
def delete_image(image_id):
    """
    Delete an image if the user owns it or is an admin.
    """
    try:
        current_user = get_jwt_identity()
        user_id = current_user["id"]
        image_obj = db.session.get(Image, image_id)
        if not image_obj:
            return jsonify({"error": "Image not found."}), 404

        if image_obj.user_id != user_id and not is_admin_user(user_id):
            return jsonify({"error": "Not authorized to delete this image."}), 403

        delete_file(image_obj.user_id, image_obj.filename)
        db.session.delete(image_obj)
        db.session.commit()

        logger.log_to_console(
            "INFO", "Image deleted.", user_id=user_id, image_id=image_id
        )
        return jsonify({"message": "Image deleted successfully."}), 200

    except Exception as exc:
        logger.log_to_console("ERROR", "Error deleting image.", error=str(exc))
        return jsonify({"error": "Error occurred while deleting the image."}), 500

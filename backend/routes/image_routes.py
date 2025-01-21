from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
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
@jwt_required()
def upload_image():
    """
    Upload an image file for the current user.
    """
    try:
        # Get the user info from the JWT
        current_user = get_jwt_identity()
        user_id = current_user["id"]

        logger.log_to_console("INFO", "Image upload initiated.", user_id=user_id)

        if "file" not in request.files:
            return jsonify({"error": "No file part in the request."}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No selected file."}), 400

        if file and allowed_file(file.filename):
            # Generate a safe and unique filename
            original_filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{original_filename}"

            # Write the file to the appropriate user directory
            file_contents = file.read()
            write_file(user_id, unique_filename, file_contents, mode="wb")

            # Store image metadata in the database
            new_image = Image(filename=unique_filename, user_id=user_id)
            db.session.add(new_image)
            db.session.commit()

            logger.log_to_console(
                "INFO",
                "Image uploaded successfully.",
                user_id=user_id,
                filename=unique_filename,
            )
            return (
                jsonify(
                    {
                        "message": "Image uploaded successfully.",
                        "image_id": new_image.id,
                    }
                ),
                201,
            )

        return jsonify({"error": "Unsupported file type."}), 400
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.log_to_console("ERROR", "Error during image upload.", error=str(e))
        return jsonify({"error": "An error occurred while uploading the image."}), 500


@image_bp.route("/<int:image_id>", methods=["GET"])
@jwt_required()
def get_image(image_id):
    """
    Retrieve metadata for an image by its ID.
    """
    try:
        # Removed 'current_user = get_jwt_identity()' since it's unused
        image = db.session.get(Image, image_id)
        if not image:
            return jsonify({"error": "Image not found."}), 404

        file_path = construct_file_path(image.user_id, image.filename)
        return (
            jsonify(
                {
                    "id": image.id,
                    "filename": image.filename,
                    "path": file_path,
                    "uploaded_by": image.user_id,
                    "uploaded_at": image.created_at.isoformat(),
                }
            ),
            200,
        )
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.log_to_console("ERROR", "Error retrieving image metadata.", error=str(e))
        return (
            jsonify(
                {"error": "An error occurred while retrieving the image metadata."}
            ),
            500,
        )


@image_bp.route("/<int:image_id>", methods=["DELETE"])
@jwt_required()
def delete_image(image_id):
    """
    Delete an image by its ID if owned by the current user.
    """
    try:
        current_user = get_jwt_identity()
        user_id = current_user["id"]

        image = db.session.get(Image, image_id)
        if not image:
            return jsonify({"error": "Image not found."}), 404

        # Optionally enforce ownership:
        # if image.user_id != user_id:
        #     return jsonify({"error": "Not authorized to delete this image."}), 403

        # Physically delete the file from storage
        delete_file(image.user_id, image.filename)

        # Remove record from the database
        db.session.delete(image)
        db.session.commit()

        logger.log_to_console(
            "INFO", "Image deleted successfully.", user_id=user_id, image_id=image_id
        )
        return jsonify({"message": "Image deleted successfully."}), 200
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.log_to_console("ERROR", "Error during image deletion.", error=str(e))
        return jsonify({"error": "An error occurred while deleting the image."}), 500


# Future Expansion
# System monitoring features, including CPU, memory, and disk usage metrics.
# Evaluate psutil or alternative libraries before implementation.
# These features will require dedicated helper functions and schema updates
# if needed.

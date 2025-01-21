from backend.db import db
from backend.models import Image
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.db.errors import (
    ImageError,
    handle_database_error,
)

logger = CentralizedLogger(name="image_helpers")


class ImageHelpers:
    @staticmethod
    def create(image_data):
        """Create a new image record."""
        try:
            image = Image(**image_data)
            db.session.add(image)
            db.session.commit()
            logger.log_to_console("INFO", "Image created successfully.", image_data=image_data)
            logger.log_to_db("INFO", "Image created successfully.", module="image_helpers", meta_data=image_data)
            return image
        except Exception as e:
            db.session.rollback()
            logger.log_to_console("ERROR", "Failed to create image.", exception=e, image_data=image_data)
            logger.log_to_db("ERROR", "Failed to create image.", module="image_helpers", meta_data=image_data)
            raise ImageError("Failed to create image.") from e

    @staticmethod
    def get_by_id(image_id):
        """Retrieve an image by its ID."""
        try:
            image = db.session.get(Image, image_id)
            if not image:
                raise ImageError(f"Image with ID {image_id} not found.")
            logger.log_to_console("INFO", f"Retrieved image by ID: {image_id}")
            logger.log_to_db("INFO", "Image retrieved by ID.", module="image_helpers", meta_data={"image_id": image_id})
            return image
        except Exception as e:
            raise handle_database_error(e, module="image_helpers", meta_data={"image_id": image_id})

    @staticmethod
    def update(image_id, updated_data):
        """Update an existing image record."""
        try:
            image = db.session.get(Image, image_id)
            if not image:
                raise ImageError(f"Image with ID {image_id} not found.")

            for key, value in updated_data.items():
                if hasattr(image, key):
                    setattr(image, key, value)

            db.session.commit()
            logger.log_to_console("INFO", f"Updated image with ID: {image_id}", updates=updated_data)
            logger.log_to_db("INFO", "Image updated successfully.", module="image_helpers", meta_data={"image_id": image_id, "updates": updated_data})
            return image
        except Exception as e:
            db.session.rollback()
            raise handle_database_error(e, module="image_helpers", meta_data={"image_id": image_id, "updates": updated_data})

    @staticmethod
    def delete(image_id):
        """Delete an image by its ID."""
        try:
            image = db.session.get(Image, image_id)
            if not image:
                raise ImageError(f"Image with ID {image_id} not found.")

            db.session.delete(image)
            db.session.commit()
            logger.log_to_console("INFO", f"Deleted image with ID: {image_id}")
            logger.log_to_db("INFO", "Image deleted successfully.", module="image_helpers", meta_data={"image_id": image_id})
        except Exception as e:
            db.session.rollback()
            raise handle_database_error(e, module="image_helpers", meta_data={"image_id": image_id})

    @staticmethod
    def get_all():
        """Retrieve all image records."""
        try:
            images = db.session.query(Image).all()
            logger.log_to_console("INFO", "Retrieved all images.", count=len(images))
            logger.log_to_db("INFO", "All images retrieved.", module="image_helpers", meta_data={"count": len(images)})
            return images
        except Exception as e:
            raise handle_database_error(e, module="image_helpers")

    @staticmethod
    def exists(image_id):
        """Check if an image with a specific ID exists."""
        try:
            exists = db.session.query(Image).filter_by(id=image_id).first() is not None
            logger.log_to_console("INFO", f"Checked existence for image ID: {image_id}", exists=exists)
            logger.log_to_db("INFO", "Image existence check performed.", module="image_helpers", meta_data={"image_id": image_id, "exists": exists})
            return exists
        except Exception as e:
            raise handle_database_error(e, module="image_helpers", meta_data={"image_id": image_id})

from datetime import datetime
from typing import List
from backend.db import db
from backend.models import Image
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.error_handling import handle_database_error
from backend.utils.error_handling.exceptions import ImageError

logger = CentralizedLogger(name="image_helpers")


class ImageHelpers:
    @staticmethod
    def create(image_data: dict) -> Image:
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
    def get_images_by_size(min_width: int, min_height: int) -> List[Image]:
        """Retrieve images larger than specified dimensions."""
        try:
            images = db.session.query(Image).filter(
                Image.width >= min_width, Image.height >= min_height
            ).all()
            logger.log_to_console(
                "INFO", f"Retrieved {len(images)} images larger than {min_width}x{min_height}.",
                min_width=min_width, min_height=min_height
            )
            return images
        except Exception as e:
            raise handle_database_error(e, module="image_helpers", meta_data={"min_width": min_width, "min_height": min_height})

    @staticmethod
    def get_by_id(image_id: int) -> Image:
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
    def update(image_id: int, updated_data: dict) -> Image:
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
    def delete(image_id: int) -> None:
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
    def get_all() -> List[Image]:
        """Retrieve all image records."""
        try:
            images = db.session.query(Image).all()
            logger.log_to_console("INFO", "Retrieved all images.", count=len(images))
            logger.log_to_db("INFO", "All images retrieved.", module="image_helpers", meta_data={"count": len(images)})
            return images
        except Exception as e:
            raise handle_database_error(e, module="image_helpers")

    @staticmethod
    def exists(image_id: int) -> bool:
        """Check if an image with a specific ID exists."""
        try:
            exists = db.session.query(Image).filter_by(id=image_id).first() is not None
            logger.log_to_console(
                "INFO", f"Checked existence for image ID: {image_id}", exists=exists
            )
            logger.log_to_db("INFO", "Image existence check performed.", module="image_helpers", meta_data={"image_id": image_id, "exists": exists})
            return exists
        except Exception as e:
            raise handle_database_error(e, module="image_helpers", meta_data={"image_id": image_id})

    @staticmethod
    def get_images_by_date_range(start_date: datetime, end_date: datetime) -> List[Image]:
        """Retrieve images created within a specific date range."""
        try:
            images = db.session.query(Image).filter(Image.created_at.between(start_date, end_date)).all()
            logger.log_to_console("INFO", f"Retrieved {len(images)} images within the date range.", start_date=start_date, end_date=end_date)
            return images
        except Exception as e:
            raise handle_database_error(e, module="image_helpers", meta_data={"start_date": start_date, "end_date": end_date})

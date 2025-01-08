from backend.db import db
from backend.models import Image
from backend.utils.logger import CentralizedLogger
from backend.utils.error_handling.db.errors import (
    ImageNotFoundError,
    ImageCreationError,
    ImageUpdateError,
    ImageDeletionError,
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
            logger.log_to_console("INFO", "Image created successfully", image_data=image_data)
            logger.log_to_db(
                level="INFO",
                message="Image created successfully",
                module="image_helpers",
                meta_data=image_data
            )
            return image
        except Exception as e:
            logger.log_to_console("ERROR", f"Failed to create image: {str(e)}", image_data=image_data)
            logger.log_to_db(
                level="ERROR",
                message=f"Failed to create image: {str(e)}",
                module="image_helpers",
                meta_data=image_data
            )
            db.session.rollback()
            raise ImageCreationError(f"Failed to create image: {str(e)}") from e

    @staticmethod
    def get_by_id(image_id):
        """Get an image by its ID."""
        try:
            image = db.session.get(Image, image_id)
            if not image:
                raise ImageNotFoundError(f"Image with ID {image_id} not found.")
            logger.log_to_console("INFO", f"Retrieved image by ID: {image_id}", found=True)
            logger.log_to_db(
                level="INFO",
                message=f"Retrieved image by ID: {image_id}",
                module="image_helpers",
                meta_data={"image_id": image_id, "found": True}
            )
            return image
        except ImageNotFoundError as e:
            logger.log_to_console("WARNING", str(e))
            logger.log_to_db(
                level="WARNING",
                message=str(e),
                module="image_helpers",
                meta_data={"image_id": image_id}
            )
            raise
        except Exception as e:
            raise handle_database_error(e, module="image_helpers", meta_data={"image_id": image_id})

    @staticmethod
    def update(image_id, updated_data):
        """Update an existing image record."""
        try:
            image = db.session.get(Image, image_id)
            if not image:
                raise ImageNotFoundError(f"Image with ID {image_id} not found.")

            # Validate fields
            valid_fields = {column.name for column in Image.__table__.columns}
            for key in updated_data.keys():
                if key not in valid_fields:
                    raise ImageUpdateError(f"Invalid field: {key}")

            # Update valid fields
            for key, value in updated_data.items():
                setattr(image, key, value)

            db.session.commit()
            logger.log_to_console("INFO", f"Updated image with ID: {image_id}", updates=updated_data)
            logger.log_to_db(
                level="INFO",
                message=f"Updated image with ID: {image_id}",
                module="image_helpers",
                meta_data={"image_id": image_id, "updates": updated_data}
            )
            return image
        except ImageNotFoundError as e:
            logger.log_to_console("WARNING", str(e))
            logger.log_to_db(
                level="WARNING",
                message=str(e),
                module="image_helpers",
                meta_data={"image_id": image_id}
            )
            raise
        except ImageUpdateError as e:
            logger.log_to_console("ERROR", str(e), updates=updated_data)
            logger.log_to_db(
                level="ERROR",
                message=str(e),
                module="image_helpers",
                meta_data={"image_id": image_id, "updates": updated_data}
            )
            db.session.rollback()
            raise
        except Exception as e:
            db.session.rollback()
            raise ImageUpdateError(f"Failed to update image with ID {image_id}: {str(e)}") from e

    @staticmethod
    def delete(image_id):
        """Delete an image by its ID."""
        try:
            image = db.session.get(Image, image_id)
            if not image:
                raise ImageNotFoundError(f"Image with ID {image_id} not found.")
            db.session.delete(image)
            db.session.commit()
            logger.log_to_console("INFO", f"Deleted image with ID: {image_id}")
            logger.log_to_db(
                level="INFO",
                message=f"Deleted image with ID: {image_id}",
                module="image_helpers",
                meta_data={"image_id": image_id}
            )
        except ImageNotFoundError as e:
            logger.log_to_console("WARNING", str(e))
            logger.log_to_db(
                level="WARNING",
                message=str(e),
                module="image_helpers",
                meta_data={"image_id": image_id}
            )
            raise
        except Exception as e:
            db.session.rollback()
            raise ImageDeletionError(f"Failed to delete image with ID {image_id}: {str(e)}") from e

    @staticmethod
    def get_all():
        """Get all images."""
        try:
            images = db.session.query(Image).all()
            logger.log_to_console("INFO", "Retrieved all images", count=len(images))
            logger.log_to_db(
                level="INFO",
                message="Retrieved all images",
                module="image_helpers",
                meta_data={"count": len(images)}
            )
            return images
        except Exception as e:
            raise handle_database_error(e, module="image_helpers")

    @staticmethod
    def filter_by(field, value):
        """Filter images by a specific field."""
        try:
            images = db.session.query(Image).filter(getattr(Image, field) == value).all()
            logger.log_to_console("INFO", f"Filtered images by {field}", value=value, count=len(images))
            logger.log_to_db(
                level="INFO",
                message=f"Filtered images by {field}",
                module="image_helpers",
                meta_data={"field": field, "value": value, "count": len(images)}
            )
            return images
        except Exception as e:
            raise handle_database_error(e, module="image_helpers", meta_data={"field": field, "value": value})

    @staticmethod
    def count():
        """Get the number of images."""
        try:
            count = db.session.query(Image).count()
            logger.log_to_console("INFO", "Counted all images", count=count)
            logger.log_to_db(
                level="INFO",
                message="Counted all images",
                module="image_helpers",
                meta_data={"count": count}
            )
            return count
        except Exception as e:
            raise handle_database_error(e, module="image_helpers")

    @staticmethod
    def exists(image_id):
        """Check if an image with a specific ID exists."""
        try:
            exists = db.session.query(Image).filter_by(id=image_id).first() is not None
            logger.log_to_console("INFO", f"Checked existence for image ID: {image_id}", exists=exists)
            logger.log_to_db(
                level="INFO",
                message=f"Checked existence for image ID: {image_id}",
                module="image_helpers",
                meta_data={"image_id": image_id, "exists": exists}
            )
            return exists
        except Exception as e:
            raise handle_database_error(e, module="image_helpers", meta_data={"image_id": image_id})

    @staticmethod
    def get_by_filename(filename):
        """Get an image by its filename."""
        try:
            image = db.session.query(Image).filter_by(filename=filename).first()
            if not image:
                raise ImageNotFoundError(f"Image with filename {filename} not found.")
            logger.log_to_console("INFO", f"Retrieved image by filename: {filename}", found=True)
            logger.log_to_db(
                level="INFO",
                message=f"Retrieved image by filename: {filename}",
                module="image_helpers",
                meta_data={"filename": filename, "found": True}
            )
            return image
        except ImageNotFoundError as e:
            logger.log_to_console("WARNING", str(e))
            logger.log_to_db(
                level="WARNING",
                message=str(e),
                module="image_helpers",
                meta_data={"filename": filename}
            )
            raise
        except Exception as e:
            raise handle_database_error(e, module="image_helpers", meta_data={"filename": filename})

    @staticmethod
    def get_images_by_date_range(start_date, end_date):
        """Get images created within a specific date range."""
        try:
            images = db.session.query(Image).filter(
                Image.created_at >= start_date,
                Image.created_at <= end_date
            ).all()
            logger.log_to_console("INFO", "Retrieved images by date range", start_date=start_date, end_date=end_date, count=len(images))
            logger.log_to_db(
                level="INFO",
                message="Retrieved images by date range",
                module="image_helpers",
                meta_data={"start_date": start_date, "end_date": end_date, "count": len(images)}
            )
            return images
        except Exception as e:
            raise handle_database_error(
                e,
                module="image_helpers",
                meta_data={"start_date": start_date, "end_date": end_date}
            )

    @staticmethod
    def get_images_by_size(min_width, min_height):
        """Get images larger than a specified size."""
        try:
            images = db.session.query(Image).filter(
                Image.width >= min_width,
                Image.height >= min_height
            ).all()
            logger.log_to_console("INFO", "Retrieved images by size", min_width=min_width, min_height=min_height, count=len(images))
            logger.log_to_db(
                level="INFO",
                message="Retrieved images by size",
                module="image_helpers",
                meta_data={"min_width": min_width, "min_height": min_height, "count": len(images)}
            )
            return images
        except Exception as e:
            raise handle_database_error(
                e,
                module="image_helpers",
                meta_data={"min_width": min_width, "min_height": min_height}
            )

    @staticmethod
    def get_by_metadata(metadata):
        """Get images by specific metadata."""
        try:
            images = db.session.query(Image).filter_by(image_metadata=metadata).all()
            logger.log_to_console("INFO", "Retrieved images by metadata", metadata=metadata, count=len(images))
            logger.log_to_db(
                level="INFO",
                message="Retrieved images by metadata",
                module="image_helpers",
                meta_data={"metadata": metadata, "count": len(images)}
            )
            return images
        except Exception as e:
            raise handle_database_error(e, module="image_helpers", meta_data={"metadata": metadata})

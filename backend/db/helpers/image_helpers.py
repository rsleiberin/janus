# image_helpers.py
from backend.db import db
from backend.models import Image
from backend.utils.logger import CentralizedLogger

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
            raise

    @staticmethod
    def get_by_id(image_id):
        """Get an image by its ID."""
        image = db.session.get(Image, image_id)
        logger.log_to_console("INFO", f"Retrieved image by ID: {image_id}", found=image is not None)
        logger.log_to_db(
            level="INFO",
            message=f"Retrieved image by ID: {image_id}",
            module="image_helpers",
            meta_data={"image_id": image_id, "found": image is not None}
        )
        return image

    @staticmethod
    def update(image_id, updated_data):
        """Update an existing image record."""
        image = db.session.get(Image, image_id)
        if image:
            try:
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
            except Exception as e:
                logger.log_to_console("ERROR", f"Failed to update image with ID {image_id}: {str(e)}", updates=updated_data)
                logger.log_to_db(
                    level="ERROR",
                    message=f"Failed to update image with ID {image_id}: {str(e)}",
                    module="image_helpers",
                    meta_data={"image_id": image_id, "updates": updated_data}
                )
                db.session.rollback()
                raise
        return image

    @staticmethod
    def delete(image_id):
        """Delete an image by its ID."""
        image = db.session.get(Image, image_id)
        if image:
            try:
                db.session.delete(image)
                db.session.commit()
                logger.log_to_console("INFO", f"Deleted image with ID: {image_id}")
                logger.log_to_db(
                    level="INFO",
                    message=f"Deleted image with ID: {image_id}",
                    module="image_helpers",
                    meta_data={"image_id": image_id}
                )
            except Exception as e:
                logger.log_to_console("ERROR", f"Failed to delete image with ID {image_id}: {str(e)}")
                logger.log_to_db(
                    level="ERROR",
                    message=f"Failed to delete image with ID {image_id}: {str(e)}",
                    module="image_helpers",
                    meta_data={"image_id": image_id}
                )
                db.session.rollback()
                raise
        else:
            logger.log_to_console("WARNING", f"Image not found for ID: {image_id}")
            logger.log_to_db(
                level="WARNING",
                message=f"Image not found for ID: {image_id}",
                module="image_helpers",
                meta_data={"image_id": image_id}
            )

    @staticmethod
    def get_all():
        """Get all images."""
        images = db.session.query(Image).all()
        logger.log_to_console("INFO", "Retrieved all images", count=len(images))
        logger.log_to_db(
            level="INFO",
            message="Retrieved all images",
            module="image_helpers",
            meta_data={"count": len(images)}
        )
        return images

    @staticmethod
    def filter_by(field, value):
        """Filter images by a specific field."""
        images = db.session.query(Image).filter(getattr(Image, field) == value).all()
        logger.log_to_console("INFO", f"Filtered images by {field}", value=value, count=len(images))
        logger.log_to_db(
            level="INFO",
            message=f"Filtered images by {field}",
            module="image_helpers",
            meta_data={"field": field, "value": value, "count": len(images)}
        )
        return images

    @staticmethod
    def count():
        """Get the number of images."""
        count = db.session.query(Image).count()
        logger.log_to_console("INFO", "Counted all images", count=count)
        logger.log_to_db(
            level="INFO",
            message="Counted all images",
            module="image_helpers",
            meta_data={"count": count}
        )
        return count

    @staticmethod
    def exists(image_id):
        """Check if an image with a specific ID exists."""
        exists = db.session.query(Image).filter_by(id=image_id).first() is not None
        logger.log_to_console("INFO", f"Checked existence for image ID: {image_id}", exists=exists)
        logger.log_to_db(
            level="INFO",
            message=f"Checked existence for image ID: {image_id}",
            module="image_helpers",
            meta_data={"image_id": image_id, "exists": exists}
        )
        return exists

    @staticmethod
    def get_by_filename(filename):
        """Get an image by its filename."""
        image = db.session.query(Image).filter_by(filename=filename).first()
        logger.log_to_console("INFO", f"Retrieved image by filename: {filename}", found=image is not None)
        logger.log_to_db(
            level="INFO",
            message=f"Retrieved image by filename: {filename}",
            module="image_helpers",
            meta_data={"filename": filename, "found": image is not None}
        )
        return image

    @staticmethod
    def get_images_by_date_range(start_date, end_date):
        """Get images created within a specific date range."""
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

    @staticmethod
    def get_images_by_size(min_width, min_height):
        """Get images larger than a specified size."""
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

    @staticmethod
    def get_by_metadata(metadata):
        """Get images by specific metadata."""
        images = db.session.query(Image).filter_by(image_metadata=metadata).all()
        logger.log_to_console("INFO", "Retrieved images by metadata", metadata=metadata, count=len(images))
        logger.log_to_db(
            level="INFO",
            message="Retrieved images by metadata",
            module="image_helpers",
            meta_data={"metadata": metadata, "count": len(images)}
        )
        return images

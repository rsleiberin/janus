# image_helpers.py

from backend.db import db
from backend.models import Image


class ImageHelpers:
    @staticmethod
    def create(image_data):
        """Create a new image record."""
        image = Image(**image_data)
        db.session.add(image)
        db.session.commit()
        return image

    @staticmethod
    def get_by_id(image_id):
        """Get an image by its ID."""
        return db.session.get(Image, image_id)

    @staticmethod
    def update(image_id, updated_data):
        """Update an existing image record."""
        image = db.session.get(Image, image_id)
        if image:
            for key, value in updated_data.items():
                setattr(image, key, value)
            db.session.commit()
        return image

    @staticmethod
    def delete(image_id):
        """Delete an image by its ID."""
        image = db.session.get(Image, image_id)
        if image:
            db.session.delete(image)
            db.session.commit()

    @staticmethod
    def get_all():
        """Get all images."""
        return db.session.query(Image).all()

    @staticmethod
    def filter_by(field, value):
        """Filter images by a specific field."""
        return db.session.query(Image).filter(getattr(Image, field) == value).all()

    @staticmethod
    def count():
        """Get the number of images."""
        return db.session.query(Image).count()

    @staticmethod
    def exists(image_id):
        """Check if an image with a specific ID exists."""
        return db.session.query(Image).filter_by(id=image_id).first() is not None

    @staticmethod
    def get_by_filename(filename):
        """Get an image by its filename."""
        return db.session.query(Image).filter_by(filename=filename).first()

    @staticmethod
    def get_images_by_date_range(start_date, end_date):
        """Get images created within a specific date range."""
        return db.session.query(Image).filter(
            Image.created_at >= start_date, 
            Image.created_at <= end_date
        ).all()

    @staticmethod
    def get_images_by_size(min_width, min_height):
        """Get images larger than a specified size."""
        return db.session.query(Image).filter(
            Image.width >= min_width, 
            Image.height >= min_height
        ).all()

    @staticmethod
    def get_by_metadata(metadata):
        """Get images by specific metadata."""
        return db.session.query(Image).filter_by(image_metadata=metadata).all()

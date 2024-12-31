# image_helpers.py
from backend.db import db
from backend.models import Image
from datetime import datetime

# Image Model Helpers
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
        return Image.query.get(image_id)

    @staticmethod
    def update(image_id, updated_data):
        """Update an existing image record."""
        image = Image.query.get(image_id)
        if image:
            for key, value in updated_data.items():
                setattr(image, key, value)
            db.session.commit()
        return image

    @staticmethod
    def delete(image_id):
        """Delete an image by its ID."""
        image = Image.query.get(image_id)
        if image:
            db.session.delete(image)
            db.session.commit()

    @staticmethod
    def get_all():
        """Get all images."""
        return Image.query.all()

    @staticmethod
    def filter_by(field, value):
        """Filter images by a specific field."""
        return Image.query.filter(getattr(Image, field) == value).all()

    @staticmethod
    def count():
        """Get the number of images."""
        return Image.query.count()

    @staticmethod
    def exists(image_id):
        """Check if an image with a specific ID exists."""
        return Image.query.filter_by(id=image_id).first() is not None

    @staticmethod
    def get_by_filename(filename):
        """Get an image by its filename."""
        return Image.query.filter_by(filename=filename).first()

    @staticmethod
    def get_images_by_date_range(start_date, end_date):
        """Get images created within a specific date range."""
        return Image.query.filter(
            Image.created_at >= start_date, Image.created_at <= end_date
        ).all()

    @staticmethod
    def get_images_by_size(min_width, min_height):
        """Get images larger than a specified size."""
        return Image.query.filter(
            Image.width >= min_width, Image.height >= min_height
        ).all()

    @staticmethod
    def get_by_metadata(metadata):
        """Get images by specific metadata."""
        return Image.query.filter_by(image_metadata=metadata).all()

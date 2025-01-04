# multi_model_helpers.py

from backend.db import db
from backend.models import Image, User, Admin, Log, Analytics, Security

def get_logs_by_user(user_id):
    """Fetch all logs associated with a user."""
    return db.session.query(Log).filter_by(user_id=user_id).all()

def count_user_actions(user_id):
    """Count the number of actions performed by a user."""
    return db.session.query(Log).filter_by(user_id=user_id).count()

def is_user_admin(user_id):
    """Check if a user has admin privileges."""
    user = db.session.get(User, user_id)
    if user:
        return db.session.query(Admin).filter_by(user_id=user.id).first() is not None
    return False

def get_admin_level(user_id):
    """Fetch the admin level of a user."""
    admin = db.session.query(Admin).filter_by(user_id=user_id).first()
    return admin.admin_level if admin else None

def get_analytics_data_for_image(image_id):
    """Fetch analytics data associated with a specific image."""
    image = db.session.get(Image, image_id)
    if image:
        return db.session.query(Analytics).filter_by(id=image_id).all()
    return []

def track_user_security_actions(user_id):
    """Fetch all security-related actions for a specific user."""
    return db.session.query(Security).filter_by(user_id=user_id).all()

def get_images_with_analytics():
    """Fetch all images with associated analytics data."""
    images = db.session.query(Image).all()
    result = []
    for image in images:
        analytics = db.session.query(Analytics).filter_by(id=image.id).all()
        result.append({"image": image, "analytics": analytics})
    return result

# admin_helpers.py

from backend.db import db
from backend.models import Admin
from flask import current_app  # To get the current app context
from datetime import datetime

class AdminHelpers:
    @staticmethod
    def create(admin_data):
        """Create a new admin record, linking it to a user."""
        admin = Admin(**admin_data)
        db.session.add(admin)
        db.session.commit()
        return admin

    @staticmethod
    def get_by_id(admin_id):
        """Get an admin by their ID."""
        with current_app.app_context():
            return db.session.get(Admin, admin_id)

    @staticmethod
    def get_by_user_id(user_id):
        """Get an admin by the associated user's ID."""
        return db.session.query(Admin).filter_by(user_id=user_id).first()

    @staticmethod
    def update(admin_id, updated_data):
        """Update an existing admin record."""
        admin = db.session.get(Admin, admin_id)
        if admin:
            for key, value in updated_data.items():
                setattr(admin, key, value)
            db.session.commit()
        return admin

    @staticmethod
    def delete(admin_id):
        """Delete an admin by their ID."""
        admin = db.session.get(Admin, admin_id)
        if admin:
            db.session.delete(admin)
            db.session.commit()

    @staticmethod
    def count():
        """Get the number of admins."""
        return db.session.query(Admin).count()

    @staticmethod
    def exists(admin_id):
        """Check if an admin with a specific ID exists."""
        return db.session.query(Admin).filter_by(id=admin_id).first() is not None

# admin_helpers.py
from backend.db import db
from backend.models import Admin
from datetime import datetime

# Admin Model Helpers
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
        return Admin.query.get(admin_id)

    @staticmethod
    def get_by_user_id(user_id):
        """Get an admin by the associated user's ID."""
        return Admin.query.filter_by(user_id=user_id).first()

    @staticmethod
    def update(admin_id, updated_data):
        """Update an existing admin record."""
        admin = Admin.query.get(admin_id)
        if admin:
            for key, value in updated_data.items():
                setattr(admin, key, value)
            db.session.commit()
        return admin

    @staticmethod
    def delete(admin_id):
        """Delete an admin by their ID."""
        admin = Admin.query.get(admin_id)
        if admin:
            db.session.delete(admin)
            db.session.commit()

    @staticmethod
    def count():
        """Get the number of admins."""
        return Admin.query.count()

    @staticmethod
    def exists(admin_id):
        """Check if an admin with a specific ID exists."""
        return Admin.query.filter_by(id=admin_id).first() is not None
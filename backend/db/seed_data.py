# seed_data.py
# Script to populate the database with initial data for testing purposes.

from backend import db
from backend.models import Image, User, Admin, Log, Analytics, Security
from datetime import datetime

def seed_db():
    """Seed the database with initial data."""
    
    # Create sample user
    user1 = User(username="admin", email="admin@example.com", password_hash="hashedpassword", role="admin")
    db.session.add(user1)

    # Create an admin entry
    admin1 = Admin(user_id=user1.id, admin_level="superadmin")
    db.session.add(admin1)

    # Create image entry
    image1 = Image(filename="image1.jpg", width=800, height=600, bit_depth=24, color_type="RGB", compression_method="JPEG", image_metadata=None, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    db.session.add(image1)

    # Create log entry
    log1 = Log(user_id=user1.id, action="Uploaded image1.jpg", timestamp=datetime.utcnow())
    db.session.add(log1)

    # Create analytics entry
    analytics1 = Analytics(data={"metric": "example_data"}, created_at=datetime.utcnow())
    db.session.add(analytics1)

    # Create security entry
    security1 = Security(user_id=user1.id, action="Login attempt", timestamp=datetime.utcnow())
    db.session.add(security1)

    db.session.commit()
    print("Database seeded successfully.")

# Call the function to seed the database
seed_db()

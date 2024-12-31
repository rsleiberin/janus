#!/usr/bin/env python3

from backend import create_app
from backend.db import db
from backend.models import Image, User, Admin, Log, Analytics, Security
from datetime import datetime

# Create Flask app context
app = create_app()

def seed_data():
    """Seed the database with initial data."""
    # Create default users
    user1 = User(username='admin', email='admin@example.com', password_hash='hashed_password', role='admin')
    user2 = User(username='user', email='user@example.com', password_hash='hashed_password', role='user')
    
    # Commit users before creating admins, so user_id is valid
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    # Create default images
    image1 = Image(filename='image1.jpg', width=800, height=600, bit_depth=24, color_type='RGB', compression_method='JPEG', image_metadata={'size': 'small'}, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    image2 = Image(filename='image2.jpg', width=1920, height=1080, bit_depth=24, color_type='RGB', compression_method='JPEG', image_metadata={'size': 'large'}, created_at=datetime.utcnow(), updated_at=datetime.utcnow())

    db.session.add(image1)
    db.session.add(image2)

    # Now create admin user (user1 already has a valid user_id)
    admin1 = Admin(user_id=user1.id, admin_level='superadmin')
    db.session.add(admin1)

    # Create logs for user actions
    log1 = Log(action='User logged in', user_id=user1.id, timestamp=datetime.utcnow())
    log2 = Log(action='Image uploaded', user_id=user2.id, timestamp=datetime.utcnow())

    db.session.add(log1)
    db.session.add(log2)

    # Create analytics data for research purposes
    analytics1 = Analytics(data={'analysis': 'image1 analysis data'}, research_topic='Image Processing', created_at=datetime.utcnow())
    analytics2 = Analytics(data={'analysis': 'image2 analysis data'}, research_topic='Image Processing', created_at=datetime.utcnow())

    db.session.add(analytics1)
    db.session.add(analytics2)

    # Create security logs for actions taken by users
    security1 = Security(user_id=user1.id, action='Password change', timestamp=datetime.utcnow())
    security2 = Security(user_id=user2.id, action='Login attempt', timestamp=datetime.utcnow())

    db.session.add(security1)
    db.session.add(security2)

    # Commit all changes to the database
    db.session.commit()

if __name__ == "__main__":
    # Ensure the app context is properly set before calling the seed function
    with app.app_context():
        seed_data()
        print("Database seeded successfully!")

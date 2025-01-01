#!/usr/bin/env python3

from datetime import datetime
from backend.db import db
from backend.models import Image, User, Admin, Log, Analytics, Security

def seed_data():
    """
    Seed the database with initial data.
    Expects an active Flask app context and DB session.
    """
    # Create default users
    user1 = User(username='admin', email='admin@example.com',
                 password_hash='hashed_password', role='admin')
    user2 = User(username='user', email='user@example.com',
                 password_hash='hashed_password', role='user')
    db.session.add_all([user1, user2])
    db.session.commit()

    # Create default images
    image1 = Image(
        filename='image1.jpg',
        width=800,
        height=600,
        bit_depth=24,
        color_type='RGB',
        compression_method='JPEG',
        image_metadata={'size': 'small'},
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    image2 = Image(
        filename='image2.jpg',
        width=1920,
        height=1080,
        bit_depth=24,
        color_type='RGB',
        compression_method='JPEG',
        image_metadata={'size': 'large'},
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add_all([image1, image2])

    # Now create an admin for user1
    admin1 = Admin(user_id=user1.id, admin_level='superadmin')
    db.session.add(admin1)

    # Create logs for user actions
    log1 = Log(action='User logged in', user_id=user1.id, timestamp=datetime.utcnow())
    log2 = Log(action='Image uploaded', user_id=user2.id, timestamp=datetime.utcnow())
    db.session.add_all([log1, log2])

    # Create analytics data
    analytics1 = Analytics(
        data={'analysis': 'image1 analysis data'},
        research_topic='Image Processing',
        created_at=datetime.utcnow()
    )
    analytics2 = Analytics(
        data={'analysis': 'image2 analysis data'},
        research_topic='Image Processing',
        created_at=datetime.utcnow()
    )
    db.session.add_all([analytics1, analytics2])

    # Create security logs
    security1 = Security(user_id=user1.id, action='Password change', timestamp=datetime.utcnow())
    security2 = Security(user_id=user2.id, action='Login attempt', timestamp=datetime.utcnow())
    db.session.add_all([security1, security2])

    db.session.commit()

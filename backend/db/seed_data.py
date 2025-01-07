# seed_data.py

from datetime import datetime
from backend.db import db
from backend.models import Image, User, Admin, Log, Analytics, Security
from backend.utils.logger import CentralizedLogger

logger = CentralizedLogger()

def seed_data():
    """
    Seed the database with initial data.
    Expects an active Flask app context and DB session.
    """
    logger.log_to_console("INFO", "Starting database seeding...")

    # Create default users
    user1 = User(
        username="admin",
        email="admin@example.com",
        password_hash="hashed_password",
        role="admin",
    )
    user2 = User(
        username="user",
        email="user@example.com",
        password_hash="hashed_password",
        role="user",
    )
    db.session.add_all([user1, user2])
    db.session.commit()  # Commit here to generate user IDs for FK relationships
    logger.log_to_console("INFO", "Default users seeded.")
    logger.log_to_db(
        level="INFO",
        message="Default users seeded",
        module="seed_data",
        user_id=user1.id,  # Attach the admin user for traceability
        meta_data={"user_count": 2},
    )

    # Create default images
    image1 = Image(
        filename="image1.jpg",
        width=800,
        height=600,
        bit_depth=24,
        color_type="RGB",
        compression_method="JPEG",
        image_metadata={"size": "small"},
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    image2 = Image(
        filename="image2.jpg",
        width=1920,
        height=1080,
        bit_depth=24,
        color_type="RGB",
        compression_method="JPEG",
        image_metadata={"size": "large"},
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.session.add_all([image1, image2])
    logger.log_to_console("INFO", "Default images seeded.")
    logger.log_to_db(
        level="INFO",
        message="Default images seeded",
        module="seed_data",
        user_id=user1.id,
        meta_data={"image_count": 2},
    )

    # Create an admin for user1
    admin1 = Admin(user_id=user1.id, admin_level="superadmin")
    db.session.add(admin1)
    logger.log_to_console("INFO", "Admin created for user1.")
    logger.log_to_db(
        level="INFO",
        message="Admin created",
        module="seed_data",
        user_id=user1.id,
        meta_data={"user_id": user1.id, "admin_level": "superadmin"},
    )

    # Create logs for user actions
    log1 = Log(
        action="User logged in",
        user_id=user1.id,
        timestamp=datetime.utcnow(),
        level="INFO",
        module="auth",
        meta_data={"ip": "127.0.0.1", "device": "desktop"},
    )
    log2 = Log(
        action="Image uploaded",
        user_id=user2.id,
        timestamp=datetime.utcnow(),
        level="INFO",
        module="images",
        meta_data={"filename": "image2.jpg"},
    )
    db.session.add_all([log1, log2])
    logger.log_to_console("INFO", "User actions logged.")
    logger.log_to_db(
        level="INFO",
        message="User logs created",
        module="seed_data",
        user_id=user1.id,
        meta_data={"log_count": 2},
    )

    # Create analytics data
    analytics1 = Analytics(
        data={"analysis": "image1 analysis data"},
        research_topic="Image Processing",
        created_at=datetime.utcnow(),
    )
    analytics2 = Analytics(
        data={"analysis": "image2 analysis data"},
        research_topic="Image Processing",
        created_at=datetime.utcnow(),
    )
    db.session.add_all([analytics1, analytics2])
    logger.log_to_console("INFO", "Analytics data seeded.")
    logger.log_to_db(
        level="INFO",
        message="Analytics data created",
        module="seed_data",
        user_id=user1.id,
        meta_data={"analytics_count": 2},
    )

    # Create security logs
    security1 = Security(
        user_id=user1.id, action="Password change", timestamp=datetime.utcnow()
    )
    security2 = Security(
        user_id=user2.id, action="Login attempt", timestamp=datetime.utcnow()
    )
    db.session.add_all([security1, security2])
    logger.log_to_console("INFO", "Security logs created.")
    logger.log_to_db(
        level="INFO",
        message="Security logs created",
        module="seed_data",
        user_id=user1.id,
        meta_data={"security_log_count": 2},
    )

    # Commit all changes
    db.session.commit()
    logger.log_to_console("INFO", "Database seeding completed successfully.")
    logger.log_to_db(
        level="INFO",
        message="Database seeding process completed",
        module="seed_data",
        user_id=user1.id,
    )


if __name__ == "__main__":
    logger.log_to_console("WARNING", "Ensure this script is run within a Flask app context.")

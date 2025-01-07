# test_seed_data.py

import pytest
import logging
from backend.db import db
from backend.db.seed_data import seed_data  # Ensure you import from the correct path
from backend.models import User, Admin, Image, Log, Analytics, Security

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("test_logger")


@pytest.mark.usefixtures("function_db_setup")
def test_seed_data():
    """
    Tests that the seed_data function properly inserts initial data into the DB.
    """
    logger.debug("Starting test_seed_data...")
    seed_data()  # This should insert the data into the DB

    # Verify default users
    assert db.session.query(User).count() == 2, "Expected exactly 2 users."
    admin_user = db.session.query(User).filter_by(username="admin").first()
    normal_user = db.session.query(User).filter_by(username="user").first()
    assert admin_user is not None, "Admin user not found."
    assert normal_user is not None, "Regular user not found."

    # Verify admin record
    assert db.session.query(Admin).count() == 1, "Expected exactly 1 admin."
    admin_record = db.session.query(Admin).first()
    assert admin_record.admin_level == "superadmin", "Admin level mismatch."

    # Verify images
    images = db.session.query(Image).all()
    assert len(images) == 2, f"Expected 2 images, found {len(images)}."

    # Verify logs specific to seeding
    logs = db.session.query(Log).filter_by(module="seed_data").all()
    assert len(logs) == 7, f"Expected 7 logs from seed_data, found {len(logs)}."

    # Verify analytics entries
    analytics_entries = db.session.query(Analytics).all()
    assert len(analytics_entries) == 2, f"Expected 2 analytics entries, found {len(analytics_entries)}."

    # Verify security entries
    security_entries = db.session.query(Security).all()
    assert len(security_entries) == 2, f"Expected 2 security entries, found {len(security_entries)}."

    logger.debug("test_seed_data passed successfully.")

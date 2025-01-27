# File: backend/db/seed_data/users_seed.py

import random
import string
from backend.db import db
from backend.models import User
from backend.utils.logger import CentralizedLogger

logger = CentralizedLogger("seed_users")


def _random_string(length=8):
    """Generate a random string of given length."""
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def seed_users(count=2):
    """
    Seed 'count' random users into the database.
    """
    logger.log_to_console("INFO", f"Seeding {count} users...")

    for _ in range(count):
        username = _random_string()
        email = f"{_random_string(5)}@example.com"
        password_hash = "hashed_" + _random_string(5)
        user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(user)

    db.session.commit()
    logger.log_to_console("INFO", f"{count} users seeded.")

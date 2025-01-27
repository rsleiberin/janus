# File: backend/db/seed_data/images_seed.py

import random
import string
from backend.db import db
from backend.models import Image
from backend.utils.logger import CentralizedLogger

logger = CentralizedLogger("seed_images")


def _random_filename():
    """Generate a random filename with .jpg extension."""
    name_part = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{name_part}.jpg"


def seed_images(count=2, user_ids=(1, 2)):
    """
    Seed 'count' random images, assigning them to user_ids in round-robin fashion.
    """
    logger.log_to_console("INFO", f"Seeding {count} images...")

    user_index = 0
    user_ids = list(user_ids)

    for _ in range(count):
        curr_user_id = user_ids[user_index]
        width = random.randint(200, 2000)
        height = random.randint(200, 2000)
        filename = _random_filename()
        image = Image(
            filename=filename,
            user_id=curr_user_id,
            width=width,
            height=height,
            bit_depth=24,
            color_type="RGB",
            compression_method="JPEG",
            image_metadata={"seeded": True},
        )
        db.session.add(image)
        user_index = (user_index + 1) % len(user_ids)

    db.session.commit()
    logger.log_to_console("INFO", f"{count} images seeded.")

# File: backend/db/seed_data/logs_seed.py

import random
from backend.db import db
from backend.models import Log
from backend.utils.logger import CentralizedLogger

logger = CentralizedLogger("seed_logs")


def seed_logs(count=2, user_ids=(1, 2)):
    """
    Seed 'count' logs, alternating user IDs.
    """
    logger.log_to_console("INFO", f"Seeding {count} logs...")

    user_index = 0
    user_ids = list(user_ids)

    actions = ["User logged in", "User updated profile", "Image uploaded"]
    modules = ["auth", "profile", "images"]

    for _ in range(count):
        user_id = user_ids[user_index]
        action = random.choice(actions)
        module = random.choice(modules)
        log_metadata = {"example_key": "example_value"}
        log_entry = Log(
            action=action,
            user_id=user_id,
            level="INFO",
            module=module,
            log_metadata=log_metadata,
        )
        db.session.add(log_entry)
        user_index = (user_index + 1) % len(user_ids)

    db.session.commit()
    logger.log_to_console("INFO", f"{count} logs seeded.")

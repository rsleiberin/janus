# File: backend/db/seed_data/security_seed.py

import random
from backend.db import db
from backend.models import Security
from backend.utils.logger import CentralizedLogger

logger = CentralizedLogger("seed_security")


def seed_security(count=2, user_ids=(1, 2)):
    """
    Seed 'count' Security events.
    """
    logger.log_to_console("INFO", f"Seeding {count} security events...")

    user_index = 0
    user_ids = list(user_ids)
    actions = ["Password change", "Failed login", "MFA challenge"]

    for _ in range(count):
        curr_user_id = user_ids[user_index]
        action = random.choice(actions)
        security_entry = Security(
            user_id=curr_user_id,
            action=action,
            security_metadata={"initiator": "seed_script"},
        )
        db.session.add(security_entry)
        user_index = (user_index + 1) % len(user_ids)

    db.session.commit()
    logger.log_to_console("INFO", f"{count} security events seeded.")

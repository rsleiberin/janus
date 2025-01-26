# File: backend/db/seed_data/__init__.py

"""
Collects all seed modules. 'run_all_seeds()' orchestrates the entire seeding process.
"""

from backend.db.seed_data.users_seed import seed_users
from backend.db.seed_data.images_seed import seed_images
from backend.db.seed_data.logs_seed import seed_logs
from backend.db.seed_data.security_seed import seed_security


def run_all_seeds():
    print("Seeding database with mock data...")
    seed_users()
    seed_images()
    seed_logs()
    seed_security()
    print("Seed process completed successfully!")

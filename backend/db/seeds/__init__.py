# File: backend/db/seeds/__init__.py

"""
Collects all seed modules. 'run_all_seeds()' orchestrates the entire seeding process.
"""

from backend.db.seeds.users_seed import seed_users
from backend.db.seeds.images_seed import seed_images
from backend.db.seeds.logs_seed import seed_logs
from backend.db.seeds.security_seed import seed_security


def run_all_seeds():
    print("Seeding database with mock data...")
    seed_users()
    seed_images()
    seed_logs()
    seed_security()
    print("Seed process completed successfully!")

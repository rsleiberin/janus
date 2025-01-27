# File: backend/db/seed_data.py

"""
An entry point to run all seeds in a single go:
    $ flask shell
    >>> from backend.db.seed_data import run_all_seeds
    >>> run_all_seeds()

Or from a script that sets up the app context first.
"""

from backend.db.seeds import run_all_seeds as run_seeds

if __name__ == "__main__":
    print("Running main seed script (ensure you have an active Flask app context) ...")
    run_seeds()

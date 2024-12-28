import sys
import os
from flask import Flask
from sqlalchemy import inspect
from sqlalchemy.schema import CreateTable

# Add the root directory to the Python path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.insert(0, root_dir)

print("PYTHONPATH:", sys.path)  # Debug: Print the updated path

# Import models after updating the Python path
try:
    from models import db
except ModuleNotFoundError as e:
    print("ERROR: Unable to import models:", str(e))
    sys.exit(1)

def create_app():
    """Create and configure the Flask application for database setup."""
    app = Flask(__name__)

    # Database configuration
    db_path = os.path.abspath("./instance/image_processing.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"  # Absolute path for SQLite
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    print("Database URI:", app.config["SQLALCHEMY_DATABASE_URI"])  # Log URI for debugging
    
    # Initialize extensions
    db.init_app(app)
    return app

if __name__ == "__main__":
    app = create_app()

    # Create the database schema
    with app.app_context():
        print("Creating database schema...")
        db.create_all()
        print("Database schema created.")
        db.session.commit()  # Ensure changes are flushed
        print("Schema creation completed.")

        # Debug generated table schema
        if 'images' in db.metadata.tables:
            print("Generated Table Schema:")
            print(str(CreateTable(db.metadata.tables['images'])))

        # Debug tables in the database
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print("Tables in database:", tables)

    # Check if the database file exists and its size
    db_path = os.path.abspath("./instance/image_processing.db")
    if os.path.exists(db_path):
        print(f"Database file created successfully at {db_path}")
        print(f"File size: {os.path.getsize(db_path)} bytes")
    else:
        print("ERROR: Database file not created!")

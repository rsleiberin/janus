import os
from flask import Flask
from backend.models import db


def create_app():
    """Factory function to create and configure the Flask application."""
    app = Flask(__name__)

    # Correctly resolve the database file path
    base_dir = os.path.abspath(os.path.dirname(__file__))
    instance_dir = os.path.join(base_dir, "instance")
    os.makedirs(instance_dir, exist_ok=True)  # Ensure 'instance' directory exists
    db_path = os.path.join(instance_dir, "image_processing.db")

    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize the database
    db.init_app(app)
    print("SQLAlchemy initialized for app:", app.name)

    # Create the database schema
    with app.app_context():
        db.create_all()
        print("Database schema created at:", db_path)

    # Import and register blueprints (inline to avoid circular imports)
    from backend.routes.status_routes import status_bp
    from backend.routes.file_routes import file_bp

    app.register_blueprint(status_bp)
    app.register_blueprint(file_bp)

    return app

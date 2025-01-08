from backend import create_app
from backend.db import db
from flask_migrate import Migrate

# Create the Flask application
app = create_app()

# Initialize Flask-Migrate
migrate = Migrate(app, db, directory="backend/migrations")

if __name__ == "__main__":
    # Access the logger after the app is fully initialized
    logger = app.config.get("logger")
    if logger:
        logger.log_to_console("INFO", "Flask app initialized.", environment=app.config.get("FLASK_ENV", "development"))
    app.run(debug=app.config.get("DEBUG", True))

from backend import create_app  # Import `db` from backend
from backend.db import db  # Import db here for Flask-Migrate
from flask_migrate import Migrate  # Import Flask-Migrate

# Initialize the Flask application
app = create_app()

# Access the logger from the app's configuration
logger = app.config.get("logger")
logger.log_to_console("INFO", "Flask app initialized.", environment=app.config.get("ENV"))

# Initialize Flask-Migrate
migrate = Migrate(app, db, directory="backend/migrations")

if __name__ == "__main__":
    app.run(debug=True)

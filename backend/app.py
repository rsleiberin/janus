from backend import create_app  # Import `db` from backend
from backend.db import db  # Import db here for Flask-Migrate
from flask_migrate import Migrate  # Import Flask-Migrate

app = create_app()  # Create the Flask application
migrate = Migrate(app, db, directory="backend/migrations")

if __name__ == "__main__":
    app.run(debug=True)

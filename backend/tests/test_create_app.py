from backend import create_app
from backend.db import db

def test_create_app():
    print("Testing app creation manually...")
    app = create_app()
    with app.app_context():
        print("App context is set up.")
        try:
            db.create_all()  # Attempt to create all tables
            print("Database schema created successfully.")
        except Exception as e:
            print(f"Error creating schema: {e}")

if __name__ == "__main__":
    test_create_app()

"""
Application entry point for the Flask application.
"""

from backend import create_app  # Import create_app from backend/__init__.py

app = create_app()

if __name__ == "__main__":
    app.run()

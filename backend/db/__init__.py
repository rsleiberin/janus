# File: backend/db/__init__.py

from flask_sqlalchemy import SQLAlchemy

# Shared SQLAlchemy instance, importable across the app
db = SQLAlchemy()

import pytest
from backend.db.db_helpers import *  # Import your helpers
from backend.models import db, Image

def test_schema_creation():
    """Test that the schema is properly created"""
    # Run logic to check if tables are created
    result = db.session.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in result]
    assert 'images' in tables  # You can add other tables as necessary

def test_insert_image():
    """Test inserting a new image record"""
    new_image = Image(filename="test.jpg", width=100, height=100)
    db.session.add(new_image)
    db.session.commit()

    inserted_image = db.session.query(Image).filter_by(filename="test.jpg").first()
    assert inserted_image is not None
    assert inserted_image.filename == "test.jpg"

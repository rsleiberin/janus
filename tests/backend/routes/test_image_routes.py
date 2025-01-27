"""
Tests for image_routes.py
"""

# pylint: disable=redefined-outer-name,unused-argument

import pytest
from flask import url_for
from unittest.mock import patch
from werkzeug.security import generate_password_hash
from backend.db import db
from backend.models import Image, User
from flask_jwt_extended import create_access_token  # moved import to top


@pytest.fixture
def user_with_token(app):
    """
    Create a user in DB and return (user, token).
    """
    with app.app_context():
        user = User(
            username="testuser",
            email="testuser@example.com",
            password_hash=generate_password_hash("mypassword"),
        )
        db.session.add(user)
        db.session.commit()

        token = create_access_token(identity={"id": user.id, "email": user.email})
        return user, token


@pytest.mark.usefixtures("function_db_setup")
def test_upload_image_success(client, user_with_token):
    user, token = user_with_token
    headers = {"Authorization": f"Bearer {token}"}

    with open("backend/tests/assets/sample_image.png", "rb") as img_file:
        data = {"file": (img_file, "sample_image.png")}
        response = client.post(
            url_for("image_routes.upload_image"),
            data=data,
            headers=headers,
            content_type="multipart/form-data",
        )
    assert response.status_code == 201
    json_data = response.get_json()
    assert "image_id" in json_data

    uploaded_image = db.session.get(Image, json_data["image_id"])
    assert uploaded_image
    assert uploaded_image.user_id == user.id


@pytest.mark.usefixtures("function_db_setup")
def test_upload_image_no_file(client, user_with_token):
    _, token = user_with_token
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        url_for("image_routes.upload_image"),
        data={},
        headers=headers,
        content_type="multipart/form-data",
    )
    assert response.status_code == 400
    assert response.json["error"] == "No selected file."


@pytest.mark.usefixtures("function_db_setup")
def test_get_image_metadata_success(client, user_with_token):
    user, token = user_with_token
    headers = {"Authorization": f"Bearer {token}"}

    image_obj = Image(filename="test.png", user_id=user.id)
    db.session.add(image_obj)
    db.session.commit()

    response = client.get(
        url_for("image_routes.get_image", image_id=image_obj.id), headers=headers
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == image_obj.id
    assert data["filename"] == "test.png"


@pytest.mark.usefixtures("function_db_setup")
def test_get_image_not_found(client, user_with_token):
    _, token = user_with_token
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(
        url_for("image_routes.get_image", image_id=9999), headers=headers
    )
    assert response.status_code == 404
    assert response.json["error"] == "Image not found."


@patch("backend.routes.image_routes.delete_file")
@pytest.mark.usefixtures("function_db_setup")
def test_delete_image_success(mock_delete_file, client, user_with_token):
    user, token = user_with_token
    headers = {"Authorization": f"Bearer {token}"}

    image_obj = Image(filename="test.png", user_id=user.id)
    db.session.add(image_obj)
    db.session.commit()

    response = client.delete(
        url_for("image_routes.delete_image", image_id=image_obj.id), headers=headers
    )
    data = response.get_json()

    assert response.status_code == 200
    assert data["message"] == "Image deleted successfully."

    deleted_image = db.session.get(Image, image_obj.id)
    assert deleted_image is None

    mock_delete_file.assert_called_once_with(user.id, "test.png")


@pytest.mark.usefixtures("function_db_setup")
def test_delete_image_not_found(client, user_with_token):
    _, token = user_with_token
    headers = {"Authorization": f"Bearer {token}"}

    response = client.delete(
        url_for("image_routes.delete_image", image_id=9999), headers=headers
    )
    assert response.status_code == 404
    assert response.json["error"] == "Image not found."

import pytest
from flask import url_for
from backend.models import Image
from backend.db import db

def test_upload_image_success(client, user_with_token):
    _, token = user_with_token
    headers = {"Authorization": f"Bearer {token}"}

    with open("backend/tests/assets/sample_image.png", "rb") as img_file:
        data = {"file": (img_file, "sample_image.png")}
        response = client.post(
            url_for("image_routes.upload_image"),
            data=data,
            headers=headers,
            content_type="multipart/form-data"
        )

    assert response.status_code == 201
    assert "image_id" in response.json

def test_upload_image_no_file(client, user_with_token):
    _, token = user_with_token
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        url_for("image_routes.upload_image"),
        data={},
        headers=headers,
        content_type="multipart/form-data"
    )

    assert response.status_code == 400
    assert response.json["error"] == "No file part in the request."

def test_get_image_metadata_success(client, user_with_token):
    _, token = user_with_token
    headers = {"Authorization": f"Bearer {token}"}

    image = Image(filename="test.png", user_id=1)
    db.session.add(image)
    db.session.commit()

    response = client.get(
        url_for("image_routes.get_image", image_id=image.id),
        headers=headers
    )

    assert response.status_code == 200
    assert response.json["id"] == image.id
    assert response.json["filename"] == "test.png"

def test_delete_image_success(client, user_with_token):
    _, token = user_with_token
    headers = {"Authorization": f"Bearer {token}"}

    image = Image(filename="test.png", user_id=1)
    db.session.add(image)
    db.session.commit()

    response = client.delete(
        url_for("image_routes.delete_image", image_id=image.id),
        headers=headers
    )

    assert response.status_code == 200
    assert response.json["message"] == "Image deleted successfully."

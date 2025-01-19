from flask import url_for
from backend.models import Image, db


def test_upload_image_success(client, user_with_token):
    """
    Test successful image upload with JWT user identification.
    """
    user, token = user_with_token
    headers = {"Authorization": f"Bearer {token}"}

    # We need an actual file in tests/assets or similar location
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

    # Verify the Image record was created in the DB
    uploaded_image_id = json_data["image_id"]
    uploaded_image = db.session.get(Image, uploaded_image_id)
    assert uploaded_image is not None
    assert uploaded_image.user_id == user.id


def test_upload_image_no_file(client, user_with_token):
    """
    Test when no file is provided in the form-data.
    """
    _, token = user_with_token
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        url_for("image_routes.upload_image"),
        data={},
        headers=headers,
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    assert response.json["error"] == "No file part in the request."


def test_get_image_metadata_success(client, user_with_token):
    """
    Test retrieving image metadata successfully.
    """
    user, token = user_with_token
    headers = {"Authorization": f"Bearer {token}"}

    # Create an image owned by the same user
    image = Image(filename="test.png", user_id=user.id)
    db.session.add(image)
    db.session.commit()

    response = client.get(
        url_for("image_routes.get_image", image_id=image.id), headers=headers
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == image.id
    assert data["filename"] == "test.png"
    assert data["uploaded_by"] == user.id


def test_get_image_not_found(client, user_with_token):
    """
    Test retrieving metadata for a non-existent image.
    """
    _, token = user_with_token
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(
        url_for("image_routes.get_image", image_id=9999), headers=headers
    )

    assert response.status_code == 404
    assert response.json["error"] == "Image not found."


def test_delete_image_success(client, user_with_token, mocker):
    """
    Test deleting an image successfully.
    """
    user, token = user_with_token
    headers = {"Authorization": f"Bearer {token}"}

    # Mock out the delete_file function to avoid actual file system operations
    mock_delete_file = mocker.patch("backend.routes.image_routes.delete_file")

    image = Image(filename="test.png", user_id=user.id)
    db.session.add(image)
    db.session.commit()

    response = client.delete(
        url_for("image_routes.delete_image", image_id=image.id), headers=headers
    )

    assert response.status_code == 200
    assert response.json["message"] == "Image deleted successfully."

    # Verify DB record is removed
    deleted_image = db.session.get(Image, image.id)
    assert deleted_image is None

    # Verify the file was "deleted"
    mock_delete_file.assert_called_once_with(user.id, "test.png")


def test_delete_image_not_found(client, user_with_token):
    """
    Test deleting a non-existent image.
    """
    _, token = user_with_token
    headers = {"Authorization": f"Bearer {token}"}

    response = client.delete(
        url_for("image_routes.delete_image", image_id=9999), headers=headers
    )

    assert response.status_code == 404
    assert response.json["error"] == "Image not found."

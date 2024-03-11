import os
import sys
import pytest
import base64

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.src.main import app

from router.auth import db


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_login(client):
    """
    Test case for successful login.

    Input:
    - client: Flask test client.

    Output:
    - None.

    Functionality:
    This function tests the login functionality by adding a user to the database with known credentials.
    It sends a POST request to the "/login" endpoint with valid login credentials.
    The response status code is checked to ensure it's 200 (OK), indicating a successful login.
    The response content is then checked to ensure it contains a "token" field.
    """
    db.append(
        {
            "emailId": "test@example.com",
            "password": "test_password",
            "calendly_personal_access_token": "test_calendly_token",
        }
    )

    credentials = {
        "email": "test@example.com",
        "password": base64.b64encode(b"test_password").decode("utf-8"),
    }

    response = client.post("/login", json=credentials)

    assert response.status_code == 200
    assert "token" in response.json


def test_login_invalid_credentials(client):
    """
    Test case for login with invalid credentials.

    Input:
    - client: Flask test client.

    Output:
    - None.

    Functionality:
    This function tests the behavior of the login endpoint when invalid credentials are provided.
    It sends a POST request to the "/login" endpoint with invalid login credentials.
    The response status code is checked to ensure it's 400 (Bad Request), indicating invalid credentials.
    The response content is then checked to ensure it contains an "error" message.
    """
    credentials = {
        "email": "nonexistent@example.com",
        "password": base64.b64encode(b"invalid_password").decode("utf-8"),
    }

    response = client.post("/login", json=credentials)

    assert response.status_code == 400
    assert "error" in response.json


def test_signup(client):
    """
    Test case for successful user signup.

    Input:
    - client: Flask test client.

    Output:
    - None.

    Functionality:
    This function tests the signup functionality by adding a new user to the database.
    It sends a POST request to the "/signup" endpoint with valid signup data.
    The response status code is checked to ensure it's 200 (OK), indicating successful signup.
    The response content is then checked to ensure it contains a "message" field.
    Finally, it checks if the new user is added to the database.
    """
    signup_data = {
        "email": "newuser@example.com",
        "password": base64.b64encode(b"new_user_password").decode("utf-8"),
        "calendly_personal_access_token": base64.b64encode(b"new_user_token").decode(
            "utf-8"
        ),
    }

    response = client.post("/signup", json=signup_data)

    assert response.status_code == 200
    assert "message" in response.json

    assert any(user["emailId"] == "newuser@example.com" for user in db)


def test_signup_missing_fields(client):
    """
    Test case for signing up with missing fields.

    Input:
    - client: Flask test client.

    Output:
    - None.

    Functionality:
    This function tests the behavior of the signup endpoint when required fields are missing.
    It sends a POST request to the "/signup" endpoint with signup data containing a missing field (calendly_personal_access_token).
    The response status code is checked to ensure it's 400 (Bad Request), indicating that the server has detected a missing field.
    The response content is then checked to ensure it contains an "error" message.
    """
    signup_data = {
        "email": "missing_fields@example.com",
        "password": base64.b64encode(b"password").decode("utf-8"),
        # "calendly_personal_access_token": Missing this field intentionally
    }

    response = client.post("/signup", json=signup_data)

    assert response.status_code == 400
    assert "error" in response.json

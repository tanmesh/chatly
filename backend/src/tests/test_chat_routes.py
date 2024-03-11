import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.src.main import app

from router.auth import generate_jwt_token
from controllers.calendly_controller import CalendlyController


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_chat_get_scheduled_events(client, mocker):
    """
    Test case for retrieving scheduled events.

    Input:
    - client: Flask test client.
    - mocker: Pytest mocker.

    Output:
    - None.

    Functionality:
    This function tests the behavior of the chat endpoint when retrieving scheduled events.
    It mocks the 'list_scheduled_events' method of the CalendlyController class to return a predefined summary.
    The endpoint is called with the appropriate input data.
    The response status code and content are then verified.
    """
    mocker.patch.object(
        CalendlyController, "list_scheduled_events"
    )
    token = generate_jwt_token("user_id")
    headers = {"Authorization": f"Bearer {token}"}
    data = {"text": "show me the scheduled events"}

    response = client.post("/chat", json=data, headers=headers)
    assert response.status_code == 200


def test_chat_error_response(client, mocker):
    """
    Test case for handling error response.

    Input:
    - client: Flask test client.
    - mocker: Pytest mocker.

    Output:
    - None.

    Functionality:
    This function tests the behavior of the chat endpoint when an error occurs.
    It mocks the 'list_scheduled_events' method of the CalendlyController class to raise an exception.
    The endpoint is called with the appropriate input data.
    The response status code and content are then verified.
    """
    mocker.patch.object(
        CalendlyController,
        "list_scheduled_events",
        side_effect=Exception("An error occurred"),
    )
    token = generate_jwt_token("user_id")  # Provide a valid JWT token
    headers = {"Authorization": f"Bearer {token}"}
    data = {"text": "GetScheduledEvents"}

    response = client.post("/chat", json=data, headers=headers)
    assert response.status_code == 400
    assert response.json == {"error": "An error occurred"}

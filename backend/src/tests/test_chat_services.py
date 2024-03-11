import os
import sys
import pytest
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from services.calendly_service import CalendlyService
from exceptions.calendly_client_exception import CalendlyClientException
from exceptions.calendly_server_exception import CalendlyServerException

user = {
    "calendly_user_url": "test_user_url",
    "calendly_personal_access_token": "test_token"
}

@pytest.fixture
def mock_response():
    response = MagicMock()
    response.status_code = 200 
    response.json.return_value = {
        "collection": [
            {"start_time": "2024-03-15T09:00:00", "end_time": "2024-03-15T10:00:00", "status": "active", "name": "Event 1", "uri": "uri1"},
            {"start_time": "2024-03-16T10:00:00", "end_time": "2024-03-16T11:00:00", "status": "active", "name": "Event 2", "uri": "uri2"}
        ]
    }
    return response

def test_list_scheduled_events_successful(mock_response):
    with patch("services.calendly_service.requests.request") as mock_request:
        mock_request.return_value = mock_response
        events = CalendlyService().list_scheduled_events(user)
        assert len(events) == 2
        assert events[0]["name"] == "Event 1"
        assert events[1]["name"] == "Event 2"

def test_list_scheduled_events_server_error(mock_response):
    with patch("services.calendly_service.requests.request") as mock_request:
        mock_response.status_code = 500
        mock_request.return_value = mock_response
        with pytest.raises(CalendlyServerException):
            CalendlyService().list_scheduled_events(user)

def test_list_scheduled_events_client_error(mock_response):
    with patch("services.calendly_service.requests.request") as mock_request:
        mock_response.status_code = 404
        mock_request.return_value = mock_response
        with pytest.raises(CalendlyClientException):
            CalendlyService().list_scheduled_events(user)

if __name__ == "__main__":
    pytest.main()

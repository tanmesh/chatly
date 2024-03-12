import requests
import json
import pytz
import logging
from retry import retry
from datetime import datetime, time, timedelta
from exceptions.calendly_client_exception import CalendlyClientException
from exceptions.calendly_server_exception import CalendlyServerException

logging.basicConfig(level=logging.DEBUG)

class CalendlyService:
    BASE_URL = "https://api.calendly.com"
    SCHEDULED_EVENT_URL = BASE_URL + "/scheduled_events"
    CANCEL_EVENT_URL = BASE_URL + "/scheduled_events/{}/cancellation"
    CREATE_EVENT_URL = BASE_URL + "/one_off_event_types"

    @retry(tries=3, delay=2, backoff=2, jitter=(1, 3), logger=logging)
    def list_scheduled_events(self, user):
        """
        Retrieves a list of scheduled events for the current user.

        Returns:
            list: A list of dictionaries containing information about scheduled events.
                Each dictionary contains the following keys:
                - 'start_time': A dictionary with keys 'day' and 'time' representing the start date and time of the event.
                - 'end_time': A dictionary with keys 'day' and 'time' representing the end date and time of the event.
                - 'status': The status of the event (e.g., 'active').
                - 'name': The name of the event.
                - 'uri': The URI of the event.

            If an error occurs during the retrieval process, an error message is returned as a string.
        """
        logging.debug("Listing all events")

        querystring = {"user": user.get_calendly_user_url()}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {user.get_calendly_personal_access_token()}",
        }

        response = requests.request(
            "GET", self.SCHEDULED_EVENT_URL, headers=headers, params=querystring
        )

        if response.status_code  >= 500:
            logging.error(
                "Failed to list events. Status code: %d", response.status_code
            )
            raise CalendlyServerException(f"Failed to list events. Status code: {response.status_code}")
        
        if response.status_code  >= 400:
            logging.error(
                "Failed to list events. Status code: %d", response.status_code
            )
            raise CalendlyClientException(f"Failed to list events. Status code: {response.status_code}")

        all_events_json = []
        for event in response.json()["collection"]:
            logging.debug(event)
            if event["status"] != "active" or event["start_time"] < datetime.now().isoformat():
                continue
            start_time = datetime.fromisoformat(event["start_time"])
            end_time = datetime.fromisoformat(event["end_time"])

            all_events_json.append(
                {
                    "start_time": {
                        "day": start_time.strftime("%Y-%m-%d"),
                        "time": self.convert_to_current_timezone(start_time.strftime("%H:%M:%S")),
                    },
                    "end_time": {
                        "day": end_time.strftime("%Y-%m-%d"),
                        "time": self.convert_to_current_timezone(end_time.strftime("%H:%M:%S")),
                    },
                    "status": event["status"],
                    "name": event["name"],
                    "uri": event["uri"],
                }
            )

        logging.debug("List all events:", all_events_json)

        return all_events_json

    @retry(tries=3, delay=2, backoff=2, jitter=(1, 3), logger=logging)
    def cancel_event(self, args, user):
        """
        Cancels the specified event.

        Args:
            args (dict): A dictionary containing information about the event to be cancelled. It should contain the following keys:
                - 'uuid': The UUID (Universally Unique Identifier) of the event to be cancelled.
                - 'reason': The reason for cancelling the event.

        Returns:
            str: A message indicating the result of the cancellation operation. If the cancellation is successful, the message will contain information about the cancelled event. If an error occurs, an error message will be returned.
        """
        logging.debug(f"Cancelling event with args: {str(args)}")

        required_args = ["day", "time", "meeting_name", "reason"]
        for arg in required_args:
            if arg not in args:
                logging.error("Missing required argument: " + args)
                raise CalendlyClientException(f"Missing required argument: {arg}")

        uuid = self.get_uuid(args, user)

        if uuid == "":
            logging.debug("No event found")
            return "No event found"

        payload = {"reason": args["reason"]}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {user.get_calendly_personal_access_token()}",
        }

        response = requests.request(
            "POST",
            self.CANCEL_EVENT_URL.format(uuid),
            json=payload,
            headers=headers,
        )

        logging.debug(response.text)
        if response.status_code  >= 500:
            logging.error(
                "Failed to cancel event. Status code: %d", response.status_code
            )
            raise CalendlyServerException(f"Failed to cancel event. Status code: {response.status_code}")

        if response.status_code  >= 400:
            logging.error(
                "Failed to cancel event. Status code: %d", response.status_code
            )
            raise CalendlyClientException(f"Failed to cancel event. Status code: {response.status_code}")
        
        return response.text

    @retry(tries=3, delay=2, backoff=2, jitter=(1, 3), logger=logging)
    def create_event(self, args, user):
        """
        Creates a new event with the specified details.

        Args:
            args (dict): A dictionary containing information about the event to be created. It should contain the following keys:
                - 'name': The name of the event.
                - 'duration': The duration of the event (in minutes).
                - 'start_date': The start date of the event (in YYYY-MM-DD format).
                - 'end_date': The end date of the event (in YYYY-MM-DD format).

        Returns:
            str: The scheduling URL of the newly created event, if the creation is successful. If an error occurs during the creation process, an error message is returned.
        """
        logging.debug(f"Creating event with args: {str(args)}")
        
        required_args = ["name", "duration", "start_date", "end_date"]
        for arg in required_args:
            if arg not in args:
                logging.error("Missing required argument: " + args)
                raise CalendlyClientException(f"Missing required argument: {arg}")

        args["start_date"] = self.get_date(args["start_date"])
        args["end_date"] = self.get_date(args["end_date"])

        payload = {
            "name": args["name"],
            "host": user.get_calendly_user_url(),
            "co_hosts": user.get_calendly_user_url(),
            "duration": args["duration"],
            "timezone": "US/Pacific",
            "date_setting": {
                "type": "date_range",
                "start_date": args["start_date"],
                "end_date": args["end_date"],
            },
            "location": {
                "kind": "physical",
                "location": "Main Office",
                "additonal_info": "string",
            },
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {user.get_calendly_personal_access_token()}",
        }

        response = requests.request(
            "POST", self.CREATE_EVENT_URL, json=payload, headers=headers
        )

        logging.debug(response)
        if response.status_code >= 500:
            logging.error(
                "Failed to create event. Status code: %d", response.status_code
            )
            raise CalendlyServerException(f"Failed to create event. Status code: {response.status_code}")

        if response.status_code >= 400:
            logging.error(
                "Failed to create event. Status code: %d", response.status_code
            )
            raise CalendlyClientException(f"Failed to create event. Status code: {response.status_code}")

        return json.loads(response.text)["resource"]["scheduling_url"]

    def get_date(self, date):
        switcher = {
            "Today": datetime.now().strftime("%d"),
            "Tomorrow": (datetime.now() + timedelta(days=1)).strftime("%d"),
            "Yesterday": (datetime.now() - timedelta(days=1)).strftime("%d"),
        }
        return switcher.get(date, date)

    def get_uuid(self, args, user):
        args["day"] = self.get_date(args["day"])

        all_events = self.list_scheduled_events(user)
        for event in all_events:
            if event["status"] != "active":
                continue
            if (
                event["start_time"]["time"] == args["time"]
                or event["start_time"]["day"] == args["day"]
                or event["name"].lower() == args["meeting_name"].lower()
            ):
                return event["uri"].split("/")[-1]
        return ""

    def convert_to_current_timezone(self, input_time_str):
        input_time_utc = time.fromisoformat(input_time_str)

        current_date = datetime.utcnow().date()
        input_datetime_utc = datetime.combine(current_date, input_time_utc)
        
        pst_timezone = pytz.timezone('US/Pacific')
        
        input_datetime_pst = input_datetime_utc.replace(tzinfo=pytz.utc).astimezone(pst_timezone)
    
        return input_datetime_pst.strftime("%H:%M:%S")
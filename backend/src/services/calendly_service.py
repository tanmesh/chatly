import requests
import json
from datetime import datetime, timedelta
import logging
from retry import retry

logging.basicConfig(level=logging.DEBUG)


# user_url = "https://api.calendly.com/users/fe8644f5-39ae-488a-af18-382f4757f0d7"
class CalendlyService:
    BASE_URL = "https://api.calendly.com"
    USER_URL = BASE_URL + "/users/{}"
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

        querystring = {"user": self.USER_URL.format(user["calendly_user_url"])}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {user['calendly_personal_access_token']}",
        }

        response = requests.request(
            "GET", self.SCHEDULED_EVENT_URL, headers=headers, params=querystring
        )

        if response.status_code  >= 300:
            logging.error(
                "Failed to list events. Status code: %d", response.status_code
            )
            return "Error listing events"

        all_events_json = []
        for event in response.json()["collection"]:

            required_events_args = ["start_time", "end_time", "status", "name", "uri"]
            for arg in required_events_args:
                if arg not in event:
                    logging.error(
                        "Missing required argument: " + arg + " in event " + event
                    )
                    continue

            if event["status"] != "active":
                continue
            start_time = datetime.fromisoformat(event["start_time"])
            end_time = datetime.fromisoformat(event["end_time"])

            all_events_json.append(
                {
                    "start_time": {
                        "day": start_time.strftime("%Y-%m-%d"),
                        "time": start_time.strftime("%H:%M:%S"),
                    },
                    "end_time": {
                        "day": end_time.strftime("%Y-%m-%d"),
                        "time": end_time.strftime("%H:%M:%S"),
                    },
                    "status": event["status"],
                    "name": event["name"],
                    "uri": event["uri"],
                }
            )

        logging.debug("List all events:", all_events_json)

        return all_events_json

    # @retry(tries=3, delay=2, backoff=2, jitter=(1, 3), logger=logging)
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
        logging.debug("Cancelling event")
        logging.debug(args)

        uuid = self.get_uuid(args, user)
        logging.debug("UUID:", uuid)
        if uuid == "":
            logging.error("No event found")
            return "No event found"

        payload = {"reason": args["reason"]}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {user['calendly_personal_access_token']}",
        }

        response = requests.request(
            "POST",
            self.CANCEL_EVENT_URL.format(uuid),
            json=payload,
            headers=headers,
        )

        if response.status_code  >= 300:
            logging.error(
                "Failed to cancel event. Status code: %d", response.status_code
            )
            return "Error cancelling event"

        logging.debug(response.text)
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
        logging.debug("Creating event")
        logging.debug(args)
        print('User:', user)

        required_args = ["name", "duration", "start_date", "end_date"]
        for arg in required_args:
            if arg not in args:
                logging.error("Missing required argument: " + args)
                return f"Missing required argument: {arg}"

        args["start_date"] = self.get_date(args["start_date"])
        args["end_date"] = self.get_date(args["end_date"])

        me = self.USER_URL.format(user["calendly_user_url"])
        payload = {
            "name": args["name"],
            "host": me,
            "co_hosts": me,
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
            "Authorization": f"Bearer {user['calendly_personal_access_token']}",
        }
        response = requests.request(
            "POST", self.CREATE_EVENT_URL, json=payload, headers=headers
        )

        logging.debug(response)
        if response.status_code != 201:
            logging.error(
                "Failed to create event. Status code: %d", response.status_code
            )
            return "Error creating event"

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
            logging.debug(
                event["start_time"]["time"],
                args["time"],
                event["start_time"]["day"],
                args["day"],
                event["name"].lower(),
                args["meeting_name"].lower(),
            )
            if (
                event["start_time"]["time"] == args["time"]
                or event["start_time"]["day"] == args["day"]
                or event["name"].lower() == args["meeting_name"].lower()
            ):
                return event["uri"].split("/")[-1]
        return ""

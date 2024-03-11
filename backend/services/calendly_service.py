import requests
import json
from datetime import datetime, timedelta
import logging
from retry import retry

logging.basicConfig(level=logging.DEBUG)


class CalendlyService:
    USER_URL = "https://api.calendly.com/users/fe8644f5-39ae-488a-af18-382f4757f0d7"

    def __init__(self, api_key):
        self.api_key = api_key

    @retry(tries=3, delay=2, backoff=2, jitter=(1, 3), logger=logging)
    def list_scheduled_events(self):
        logging.debug("Listing all events")
        url = "https://api.calendly.com/scheduled_events"

        querystring = {"user": self.USER_URL}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        all_events_json = []
        for event in response.json()["collection"]:
            logging.debug(event)
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

    def get_uuid(self, args):
        args["day"] = self.get_date(args["day"])

        all_events = self.list_scheduled_events()
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

    @retry(tries=3, delay=2, backoff=2, jitter=(1, 3), logger=logging)
    def cancel_event(self, args):
        logging.debug("Cancelling event")
        logging.debug(args)
        uuid = self.get_uuid(args)
        logging.debug("UUID:", uuid)
        if uuid == "":
            return "No event found"

        url = f"https://api.calendly.com/scheduled_events/{uuid}/cancellation"

        payload = {"reason": args["reason"]}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        logging.debug(response.text)
        return response.text

    def get_date(self, date):
        switcher = {
            "Today": datetime.now().strftime("%d"),
            "Tomorrow": (datetime.now() + timedelta(days=1)).strftime("%d"),
            "Yesterday": (datetime.now() - timedelta(days=1)).strftime("%d"),
        }
        return switcher.get(date, date)

    @retry(tries=3, delay=2, backoff=2, jitter=(1, 3), logger=logging)
    def create_event(self, args):
        logging.debug("Creating event")
        logging.debug(args)
        url = "https://api.calendly.com/one_off_event_types"

        args["start_date"] = self.get_date(args["start_date"])
        args["end_date"] = self.get_date(args["end_date"])

        payload = {
            "name": args["name"],
            "host": self.USER_URL,
            "co_hosts": [self.USER_URL],
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
            "Authorization": f"Bearer {self.api_key}",
        }

        response = requests.request("POST", url, json=payload, headers=headers)

        logging.debug(response.text)
        return json.loads(response.text)["resource"]["scheduling_url"]

import requests
import json
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)

class CalendlyService:
    USER_URL = "https://api.calendly.com/users/fe8644f5-39ae-488a-af18-382f4757f0d7"

    def __init__(self, api_key):
        self.api_key = api_key

    def list_scheduled_events(self):
        url = "https://api.calendly.com/scheduled_events"

        querystring = {"user": self.USER_URL}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        all_events_json = []
        for event in response.json()["collection"]:
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

        # logging.debug("List all events:", response.text)

        return all_events_json

    def get_uuid(self, args):
        if args["day"] in ["Today", "Tomorrow", "Yesterday"]:
            if args["day"] == "Today":
                args["day"] = datetime.now().strftime("%d")
            elif args["day"] == "Tomorrow":
                args["day"] = datetime.now().day + 1
            elif args["day"] == "Yesterday":
                args["day"] = datetime.now().day - 1

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

    def cancel_event(self, args):
        uuid = self.get_uuid(args)
        logging.debug("UUID:", uuid)
        if uuid == "":
            return "No event found"

        url = f"https://api.calendly.com/scheduled_events/{uuid}/cancellation"

        payload = {"reason": "not well"}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        # response = requests.request("POST", url, json=payload, headers=headers)
        # return response.text

        return url

    def create_event(self, args):
        logging.debug(args)
        url = "https://api.calendly.com/one_off_event_types"

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

        return json.loads(response.text)["resource"]["scheduling_url"]

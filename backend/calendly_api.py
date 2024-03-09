import requests
from os import environ as env

CALENDLY_API_KEY = env.get('CALENDLY_API_KEY')

def list_all_events():
    url = "https://api.calendly.com/scheduled_events"

    querystring = {"user":"https://api.calendly.com/users/fe8644f5-39ae-488a-af18-382f4757f0d7"}

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJraWQiOiIxY2UxZTEzNjE3ZGNmNzY2YjNjZWJjY2Y4ZGM1YmFmYThhNjVlNjg0MDIzZjdjMzJiZTgzNDliMjM4MDEzNWI0IiwidHlwIjoiUEFUIiwiYWxnIjoiRVMyNTYifQ.eyJpc3MiOiJodHRwczovL2F1dGguY2FsZW5kbHkuY29tIiwiaWF0IjoxNzA5OTYyMTQzLCJqdGkiOiIxZjNjMzJhYi00ZTQ5LTQ2ZTEtODQwNS03ZmVkYmQzMGY5MGMiLCJ1c2VyX3V1aWQiOiJmZTg2NDRmNS0zOWFlLTQ4OGEtYWYxOC0zODJmNDc1N2YwZDcifQ.-ZuvHBNcNyRt-esfUmnJ9Wc6lGa_m2YvMZDGJMA46sia4mzPFxGOmTh36FTjd7I2jmtMuROMzAomX-NzWUU17g"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print('List all events:', response.text)

    #TODO clean up the response

    return response.text


 # https://developer.calendly.com/api-docs/afb2e9fe3a0a0-cancel-event 
def cancel_event():
    url = "https://api.calendly.com/scheduled_events/f1694fab-626d-4ca0-99df-0e45f79a66ab/cancellation"

    payload = {"reason": "not well"}

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CALENDLY_API_KEY}"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    return response.text

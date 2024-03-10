import json
from os import environ as env
from flask import Blueprint, jsonify, request
from langchain_core.messages import HumanMessage
from engine.chat_engine import ChatEngine
from controllers.functions import (
    CancelEvent,
    GetScheduledEvents,
    CreateEvent,
    GeneralChat,
)
from controllers.calendly_controller import CalendlyController
from services.calendly_service import CalendlyService

chat_engine = ChatEngine(
    model="gpt-3.5-turbo-0125",
    tools=[CancelEvent, GetScheduledEvents, CreateEvent, GeneralChat],
)
llm = chat_engine.llm

chat = Blueprint("chat", __name__)

service = CalendlyService(env.get("CALENDLY_API_KEY"))
controller = CalendlyController(service)


## This is the endpoint that the frontend will call to send the input prompt.
@chat.route("/chat", methods=["POST"])
def chatz():
    try:
        text = request.get_json()["text"]
        messages = [HumanMessage(content=text)]
        output = llm.invoke(messages)

        dict_data = output.additional_kwargs
        function_name = dict_data["tool_calls"][0]["function"]["name"]
        argument_json = json.loads(dict_data["tool_calls"][0]["function"]["arguments"])

        if function_name == "GetScheduledEvents":
            return controller.list_scheduled_events(llm)
        elif function_name == "CancelEvent":
            return controller.cancel_event(argument_json)
        elif function_name == "CreateEvent":
            return controller.create_event(argument_json)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
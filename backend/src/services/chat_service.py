import json
from os import environ as env
from flask import request
from langchain_core.messages import HumanMessage
from engine.chat_engine import ChatEngine
from services.calendly_service import CalendlyService
from services.functions import (
    CancelEvent,
    GetScheduledEvents,
    CreateEvent,
    GeneralChat,
)

chat_engine = ChatEngine(
    model="gpt-3.5-turbo-0125",
    tools=[CancelEvent, GetScheduledEvents, CreateEvent],
)
llm = chat_engine.llm

chat_engine_general_chat = ChatEngine(
    model="gpt-3.5-turbo-0125",
    tools=[GeneralChat],
)


def chat_service(current_user, text, calendy_user_url_key):
    """
    Processes incoming chat requests, invokes corresponding calendar service functions,
    summarizes the results, and returns a response.

    Returns:
        tuple: A tuple containing a response type and content. The response type can be
        "response" indicating a successful response, or "error" indicating an error occurred.
        The content contains the response message or error description.
    """
    try:
        calendy_service = CalendlyService(
            env.get("CALENDLY_API_KEY"), calendy_user_url_key
        )
        
        messages = [HumanMessage(content=text)]
        output = llm.invoke(messages)

        dict_data = output.additional_kwargs
        if dict_data is None or dict_data == {}:
            return "response", output.content

        function_name = dict_data["tool_calls"][0]["function"]["name"]
        argument_json = json.loads(dict_data["tool_calls"][0]["function"]["arguments"])

        if function_name == "GetScheduledEvents":
            output_description = calendy_service.list_scheduled_events()
            summary = "Summarize the list of events"
        elif function_name == "CancelEvent":
            output_description = calendy_service.cancel_event(argument_json)
            summary = f"Link--{output_description} \n\n Summarize the cancellation of the event with the provided link."
        elif function_name == "CreateEvent":
            output_description = calendy_service.create_event(argument_json)
            summary = "Summarize the new event created"

        output = chat_engine_general_chat.llm.invoke(
            f"{output_description} \n\n {summary}"
        )
        tmp = json.loads(
            output.additional_kwargs["tool_calls"][0]["function"]["arguments"]
        )
        return "response", tmp["description"]

    except Exception as e:
        return "error", str(e)

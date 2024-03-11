from flask import request
from services.auth_service import auth_cache
from os import environ as env
from flask import Blueprint, jsonify
from services.auth_service import token_required
from services.calendly_service import CalendlyService
from services.chat_service import ChatService

chat = Blueprint("chat", __name__)


calendly_service = CalendlyService()
chat_service = ChatService(calendly_service)


## This is the endpoint that the frontend will call to send the input prompt.
@chat.route("/chat", methods=["POST"])
@token_required
def chatz(current_user):
    """
    Endpoint to handle incoming chat requests.

    Args:
        current_user: The current user authenticated by the token_required decorator.

    Returns:
        tuple: A tuple containing a JSON response and an HTTP status code.
        If the chat service returns an error, the response JSON contains an error message
        with an HTTP status code of 400. Otherwise, the response JSON contains the
        chat service response with an HTTP status code of 200.
    """
    if request.get_json() is None:
        return jsonify({"error": "No input provided"}), 400

    token = request.headers.get("Authorization")
    user = auth_cache.get(token)

    type, message = chat_service.process(request.get_json()["text"], user)

    if type == "error":
        return jsonify({"error": message}), 400
    return jsonify({"response": message}), 200

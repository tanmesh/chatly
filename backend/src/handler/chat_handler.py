from flask import request
from services.auth_service import auth_cache
from flask import Blueprint, jsonify
from services.calendly_service import CalendlyService
from services.chat_service import ChatService
from functools import wraps
import jwt
from exceptions.calendly_client_exception import CalendlyClientException
from exceptions.calendly_server_exception import CalendlyServerException

chat = Blueprint("chat", __name__)


calendly_service = CalendlyService()
chat_service = ChatService(calendly_service)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            data = jwt.decode(token, "1234", algorithms=["HS256"])
            current_user = data["user_id"]
        except:
            return jsonify({"message": "Token is invalid!"}), 401

        return f(current_user, *args, **kwargs)

    return decorated

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

    try :
        message = chat_service.process(request.get_json()["text"], user)
    except CalendlyServerException as e:
        return jsonify({"error": str(e)}), 500
    except CalendlyClientException as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"response": message}), 200
import base64
import logging
from flask import Blueprint, jsonify, request
from services.auth_service import AuthService

logging.basicConfig(level=logging.DEBUG)

def create_auth_blueprint(user_storage, auth_cache):
    auth = Blueprint("auth", __name__)

    auth_service = AuthService(user_storage, auth_cache)
    
    @auth.route("/login", methods=["POST"])
    def login():
        """
        Endpoint for user login.

        Expects JSON data with keys 'email' and 'password'.
        Returns a JSON response with a token if login is successful, or an error message otherwise.
        """
        try:
            email = request.json.get("email")
            encoded_password = request.json.get("password")
            password = base64.b64decode(encoded_password).decode("utf-8")

            logging.debug(f"Login request received {email}")

            if not email or not password:
                return jsonify({"error": "Email and password are required!"}), 400

            type, message = auth_service.login_service(email, password)

            if type == "error":
                return jsonify({"error": message}), 400
            return jsonify({"token": message}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400


    @auth.route("/signup", methods=["POST"])
    def signup():
        """
        Endpoint for user signup.

        Expects JSON data with keys 'email', 'password', and 'calendly_personal_access_token'.
        Returns a JSON response with a success message if signup is successful, or an error message otherwise.
        """
        try:    
            email = request.json.get("email")
            encoded_password = request.json.get("password")
            encoded_pat = request.json.get("calendly_personal_access_token")
            encoded_user_url = request.json.get("calendly_user_uri")

            
            try:
                password = base64.b64decode(encoded_password).decode("utf-8")
                calendly_personal_access_token = base64.b64decode(encoded_pat).decode("utf-8")    
                calendly_user_url = base64.b64decode(encoded_user_url).decode("utf-8")
            except:
                return jsonify({"error": "Unable to parse data!"}), 400

            if email is None or password is None or calendly_personal_access_token is None or calendly_user_url is None:
                return jsonify({"error": "Fields cannot be empty!"}), 400

            type, message = auth_service.signup_service(email, password, calendly_personal_access_token, calendly_user_url)

            if type == "error":
                return jsonify({"error": message}), 400
            return jsonify({"message": message}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    return auth
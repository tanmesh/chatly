import jwt
from functools import wraps
from os import environ as env
from flask import jsonify, request
from datetime import datetime, timedelta

db = [
    {
        "emailId": "tanmeshnm@gmail.com",
        "password": "admin",
        "calendly_personal_access_token": env.get("CALENDLY_API_KEY"),
    }
]


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


def generate_jwt_token(user_id):
    # Define payload (data) to be included in the token
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1),  # Token expiration time
    }

    # Generate JWT token
    token = jwt.encode(payload, "1234", algorithm="HS256")
    return token


def login_service(emailId, password):
    for it in db:
        if it["emailId"] == emailId and it["password"] == password:
            token = generate_jwt_token(emailId + password)
            return "success", token
    return "error", "Invalid email or password!"

def signup_service(emailId, password, calendly_personal_access_token):
    try:
        db.append(
            {
                "emailId": emailId,
                "password": password,
                "calendly_personal_access_token": calendly_personal_access_token,
            }
        )
        return "success", "User registered successfully!"
    except:
        return "error", "Error registering user!"
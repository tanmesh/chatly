import jwt
from functools import wraps
from os import environ as env
from flask import jsonify, request
from datetime import datetime, timedelta
from entity.user import User

db = {
    "tanmeshnm@gmail.com": User(
        "tanmeshnm@gmail.com",
        "admin",
        env.get("CALENDLY_API_KEY"),
        env.get("CALENDLY_USER_URL_KEY"),
    )
}

auth_cache = {}


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


class AuthService:
    def generate_jwt_token(self, user_id):
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(hours=1),  # Token expiration time
        }

        token = jwt.encode(payload, "1234", algorithm="HS256")
        return token

    def login_service(self, emailId, password):
        for token, user in db.items():
            print(token, user)
            if user.get_email() == emailId and user.get_password() == password:
                token = self.generate_jwt_token(emailId + password)

                print("token:", token)
                auth_cache[token] = user

                print("auth_cache:")
                print(auth_cache)
                return "success", token
        return "error", "Invalid email or password!"

    def signup_service(self, emailId, password, calendly_personal_access_token, calendly_user_url):
        try:
            user = User(
                emailId,
                password,
                calendly_personal_access_token,
                calendly_user_url,
            )

            db[emailId] = user
            return "success", "User registered successfully!"
        except:
            return "error", "Error registering user!"

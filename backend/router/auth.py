from flask import Blueprint, jsonify, request
import jwt
import base64
from datetime import datetime, timedelta
from functools import wraps

auth = Blueprint("chat", __name__)

db = [
    {
        'emailId': 'tanmeshnm@gmail.com',
        'password': 'admin'
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


@auth.route("/login", methods=["POST"])
def login():
    try:
        # Get username and password from the request
        emailId = request.json.get("email")
        encoded_password = request.json.get("password")
        password = base64.b64decode(encoded_password).decode('utf-8')

        if not emailId or not password:
            return jsonify({"error": "Email and password are required!"}), 400
        
        for it in db:
            if it['emailId'] == emailId and it['password'] == password:
                # Generate JWT token
                token = generate_jwt_token(emailId + password)
                return jsonify({"token": token}), 200
        
        return jsonify({"error": "Invalid email or password!"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@auth.route("/signup", methods=["POST"])
def signup():
    try:
        # Get username and password from the request
        emailId = request.json.get("email")
        encoded_password = request.json.get("password")
        encoded_pat = request.json.get("calendly_personal_access_token")
       
        password = base64.b64decode(encoded_password).decode('utf-8')
        calendly_personal_access_token = base64.b64decode(encoded_pat).decode('utf-8')

        if not emailId or not password or not calendly_personal_access_token:
            return jsonify({"error": "Fields cannot be empty!"}), 400
        
        db.append({
            'emailId': emailId,
            'password': password,
            'calendly_personal_access_token': calendly_personal_access_token
        })

        print(db)

        return jsonify({"message": "User registered successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

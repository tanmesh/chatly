import jwt
from datetime import datetime, timedelta
from entity.user import User

db = { }
auth_cache = {}
TOKEN_EXPIRATION_TIME = datetime.utcnow() + timedelta(hours=1)

class AuthService:
    def generate_jwt_token(self, user_id):
        payload = {
            "user_id": user_id,
            "exp": TOKEN_EXPIRATION_TIME,  # Token expiration time
        }

        token = jwt.encode(payload, "1234", algorithm="HS256")
        return token

    def login_service(self, email_id, password):
        for token, user in db.items():
            if user.get_email() == email_id and user.get_password() == password:
                token = self.generate_jwt_token(email_id + password)

                auth_cache[token] = user

                return "success", token
        return "error", "Invalid email or password!"

    def signup_service(self, email_id, password, calendly_personal_access_token, calendly_user_url):
        try:
            for _, user in db.items():
                if user.get_email() == email_id and user.get_password() == password:
                    return "error", "User already exists!"
            
            user = User(
                email_id,
                password,
                calendly_personal_access_token,
                calendly_user_url,
            )

            db[email_id] = user
            return "success", "User registered successfully!"
        except:
            return "error", "Error registering user!"

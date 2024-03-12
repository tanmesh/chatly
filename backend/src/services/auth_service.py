import jwt
import logging
from entity.user import User
from datetime import datetime, timedelta
from storage.user_storage import UserStorage
from storage.auth_cache import AuthCache

logging.basicConfig(level=logging.DEBUG)

TOKEN_EXPIRATION_TIME = datetime.utcnow() + timedelta(hours=1)

class AuthService:
    def __init__(self, user_storage: UserStorage, auth_cache: AuthCache):
        self.user_storage = user_storage
        self.auth_cache = auth_cache

    def generate_jwt_token(self, user_id):
        payload = {
            "user_id": user_id,
            "exp": TOKEN_EXPIRATION_TIME, 
        }

        token = jwt.encode(payload, "1234", algorithm="HS256")
        return token

    def login_service(self, email_id, password):
        try :
            user = self.user_storage.get_user_by_email(email_id)
            if user is None:
                raise Exception("User doesnt exist!")

            token = self.generate_jwt_token(email_id + password)
            self.auth_cache.add(token, user)

            return "success", token
        except Exception as e:
            logging.error(str(e))
            return "error", str(e)

    def signup_service(self, email_id, password, calendly_personal_access_token, calendly_user_url):
        try:
            if self.user_storage.get_user_by_email(email_id):
                raise Exception("User already exists!")
            
            user = User(
                email_id,
                password,
                calendly_personal_access_token,
                calendly_user_url,
            )

            self.user_storage.add_user(user)
            return "success", "User registered successfully!"
        except Exception as e:
            logging.error(str(e))
            return "error", str(e)

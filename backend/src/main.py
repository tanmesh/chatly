from flask import Flask
from flask_cors import CORS
from handler.auth_handler import create_auth_blueprint
from handler.chat_handler import create_chat_blueprint
from storage.user_storage import UserStorage
from storage.auth_cache import AuthCache

app = Flask(__name__)
CORS(app)

user_storage = UserStorage("user.db")
auth_cache = AuthCache()

app.register_blueprint(create_chat_blueprint(auth_cache), name='chat_blueprint')
app.register_blueprint(create_auth_blueprint(user_storage, auth_cache), name='auth_blueprint')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

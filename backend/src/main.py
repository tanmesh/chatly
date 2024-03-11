from flask import Flask
from flask_cors import CORS
from handler.auth_handler import auth
from handler.chat_handler import chat

app = Flask(__name__)
CORS(app)

app.register_blueprint(chat, name='chat_blueprint')
app.register_blueprint(auth, name='auth_blueprint')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

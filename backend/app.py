from dotenv import find_dotenv, load_dotenv
from os import environ as env
from authlib.integrations.flask_client import OAuth

from flask import Flask, jsonify, request
from flask_cors import CORS
from functions import CancelEvent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

import json

from calendly_api import list_all_events, cancel_event

app = Flask(__name__)
CORS(app)

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

OPENAI_API_KEY = env.get('OPENAI_API_KEY')

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
llm_with_tools = llm.bind_tools([CancelEvent])

@app.route('/chat', methods=['POST'])
def chat():
    try:
        text = request.get_json()['text']
        messages = [HumanMessage(content=text)]
        output = llm_with_tools.invoke(messages)

        dict_data = output.additional_kwargs
        arguments = json.loads(dict_data['tool_calls'][0]['function']['arguments'])
        get_scheduled_events = arguments['get_scheduled_events']

        if get_scheduled_events == True:
            return list_all_events()
        return f'{output}'
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

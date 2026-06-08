from flask import Flask, request, jsonify
import requests
from app.api.routes.chat import chat_router


app = Flask(__name__)

app.register_blueprint(chat_router, url_prefix="/api")

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Chatbot API is running!"})

if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=8080)
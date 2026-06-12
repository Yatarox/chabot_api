from flask import Flask, send_from_directory
from app.api.routes.chat import chat_router

app = Flask(__name__, static_folder='static')

app.register_blueprint(chat_router, url_prefix="/api")

@app.route('/')
def index():
    # Envoie le fichier index.html du dossier static
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=8080)
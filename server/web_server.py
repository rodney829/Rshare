from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from flask_httpauth import HTTPBasicAuth
import os
from werkzeug.serving import make_server
import threading

app = Flask(__name__)
auth = HTTPBasicAuth()

app.secret_key = 'supersecretkey'  # Você pode alterar essa chave para algo mais seguro

UPLOAD_FOLDER = ''
server = None

users = {
    "admin": "12345"
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/')
@auth.login_required
def index():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    arquivos = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', arquivos=arquivos)

@app.route('/upload', methods=['POST'])
@auth.login_required
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return 'File uploaded successfully'

@app.route('/uploads/<filename>')
@auth.login_required
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

class ServerThread:
    def __init__(self, app, host, port):
        self.srv = make_server(host, port, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def start(self):
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()

def iniciar_servidor_web(pasta_selecionada):
    global UPLOAD_FOLDER, server
    UPLOAD_FOLDER = pasta_selecionada
    server = ServerThread(app, '0.0.0.0', 5000)
    server.start()

def parar_servidor_web():
    global server
    if server:
        server.shutdown()
        server = None

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

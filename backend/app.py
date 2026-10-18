import hmac
from pathlib import Path

from flask import Flask, abort, jsonify, request, send_from_directory


PROJECT_DIRECTORY = Path(__file__).resolve().parent.parent
FRONTEND_DIRECTORY = PROJECT_DIRECTORY / "frontend"
DEMO_CREDENTIALS = {
    "2024001": "biohub123",
    "2024002": "biohub456",
    "2024003": "biohub789",
}
MAX_REQUEST_SIZE = 4096
STATIC_FILES = {
    "css/style.css": "css/style.css",
    "js/script.js": "js/script.js",
    "assets/logo.png": "assets/logo.png",
}

app = Flask(__name__, static_folder=None)
app.config["MAX_CONTENT_LENGTH"] = MAX_REQUEST_SIZE


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


@app.get("/")
def index():
    return send_from_directory(FRONTEND_DIRECTORY, "index.html")


@app.get("/<path:filename>")
def static_file(filename):
    file_path = STATIC_FILES.get(filename)
    if file_path is None:
        abort(404)
    return send_from_directory(FRONTEND_DIRECTORY, file_path)


@app.route("/api/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        return "", 200

    if not request.is_json:
        return jsonify(message="JSON inválido."), 400

    request_data = request.get_json(silent=True)
    if not isinstance(request_data, dict):
        return jsonify(message="JSON inválido."), 400

    matricula = request_data.get("matricula")
    password = request_data.get("password")
    if not isinstance(matricula, str) or not isinstance(password, str):
        return jsonify(message="Matrícula e senha são obrigatórias."), 400

    expected_password = DEMO_CREDENTIALS.get(matricula)
    if expected_password is None or not hmac.compare_digest(
        expected_password, password
    ):
        return jsonify(message="Matrícula ou senha inválida."), 401

    response = jsonify(message="Login realizado com sucesso!")
    response.headers["Cache-Control"] = "no-store"
    return response


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify(message="Requisição inválida."), 400


if __name__ == "__main__":
    print("Biohub disponível em http://127.0.0.1:8000")
    print("Modo demonstração: credenciais de teste estão definidas no backend.")
    app.run(host="127.0.0.1", port=8000, debug=False)

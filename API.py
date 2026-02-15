from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random
import os

# Configuração da chave de API
API_KEY = "156478"  # <--- coloque sua chave aqui

app = Flask(__name__)
CORS(app)

# Carrega intents dinamicamente
INTENTS_FILE = os.path.join(os.path.dirname(__file__), "intents.json")

def carregar_intents():
    with open(INTENTS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

intents = carregar_intents()

def buscar_resposta(mensagem):
    mensagem = mensagem.lower()
    for intent in intents:
        for pattern in intent["patterns"]:
            if pattern.lower() in mensagem:
                return random.choice(intent["responses"])
    return "🌙 Não encontrei uma resposta. Pergunte outra coisa ou tente novamente."

@app.route("/predict", methods=["POST"])
def predict():
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header != f"Bearer {API_KEY}":
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Invalid request, missing 'message'"}), 400

    mensagem = data["message"]
    resposta = buscar_resposta(mensagem)
    return jsonify({"response": resposta})

@app.route("/", methods=["GET"])
def home():
    return "🌙 API Luna de Conhecimento Ativa!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

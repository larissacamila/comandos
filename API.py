from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # <<< ISSO AQUI É O CORS

API_KEY = "156478"

INTENTS_PATH = "intents"


def carregar_intents():
    intents = []
    for arquivo in os.listdir(INTENTS_PATH):
        if arquivo.endswith(".json"):
            with open(os.path.join(INTENTS_PATH, arquivo), "r", encoding="utf-8") as f:
                dados = json.load(f)
                intents.extend(dados["intents"])
    return intents


INTENTS = carregar_intents()


@app.route("/")
def home():
    return "API de Conhecimento rodando."


@app.route("/ask", methods=["POST"])
def ask():
    chave = request.headers.get("x-api-key")
    if chave != API_KEY:
        return jsonify({"error": "Chave inválida"}), 401

    data = request.json
    texto = data.get("text", "").lower()

    for intent in INTENTS:
        for pattern in intent["patterns"]:
            if pattern in texto:
                return jsonify({
                    "response": intent["responses"][0],
                    "tag": intent["tag"]
                })

    return jsonify({
        "response": "Não encontrei uma resposta para isso ainda."
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

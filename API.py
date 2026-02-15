from flask import Flask, request, jsonify
import json
import random

app = Flask(__name__)

# Sua chave secreta
API_KEY = "156478"

# Carrega os intents do arquivo JSON
with open("intents.json", "r", encoding="utf-8") as f:
    intents = json.load(f)["intents"]

def buscar_resposta(mensagem):
    mensagem = mensagem.lower()
    for intent in intents:
        for pattern in intent["patterns"]:
            if pattern.lower() in mensagem:
                return random.choice(intent["responses"])
    return "🌙 Desculpe, não entendi. Pode reformular?"

@app.route("/predict", methods=["POST"])
def predict():
    # Verifica chave no header Authorization
    auth_header = request.headers.get("Authorization", "")
    if auth_header != f"Bearer {API_KEY}":
        return jsonify({"error": "Chave de API inválida"}), 401

    data = request.get_json()
    mensagem = data.get("message", "")
    resposta = buscar_resposta(mensagem)
    return jsonify({"response": resposta})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



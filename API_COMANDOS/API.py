from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random

app = Flask(__name__)
CORS(app)

# ---------- CHAVE DE API ----------
API_KEY = "156478"  # coloque a mesma chave nos clientes

# ---------- CARREGAR INTENTS ----------
with open("intents.json", "r", encoding="utf-8") as file:
    intents = json.load(file)["intents"]

# ---------- FUNÇÃO PARA ENCONTRAR RESPOSTA ----------
def buscar_resposta(mensagem):
    mensagem = mensagem.lower()
    for intent in intents:
        for pattern in intent["patterns"]:
            if pattern.lower() in mensagem:
                return random.choice(intent["responses"])
    return "🌙 Não entendi sua solicitação. Pode reformular?"

# ---------- ROTA PRINCIPAL ----------
@app.route("/mensagem", methods=["POST"])
def mensagem():
    data = request.get_json()

    # Verificação de API Key
    if "api_key" not in data or data["api_key"] != API_KEY:
        return jsonify({"error": "Chave de API inválida"}), 401

    mensagem_usuario = data.get("mensagem", "")
    resposta = buscar_resposta(mensagem_usuario)

    # Aqui você poderia adicionar envio para ESP32 se for comando físico
    # Exemplo: if "ligar luz" in mensagem_usuario: enviar_para_esp32("luz_on")

    return jsonify({"response": resposta})

# ---------- ROTA TESTE ----------
@app.route("/teste", methods=["GET"])
def teste():
    return jsonify({"status": "API online"})

# ---------- RODAR ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

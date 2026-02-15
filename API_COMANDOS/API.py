# app.py atualizado
from flask import Flask, request, jsonify
import json
import random
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = "156478"  # mesma chave que você colocou nos clientes

# Carrega intents
with open("intents.json", "r", encoding="utf-8") as f:
    intents_data = json.load(f)["intents"]

def buscar_resposta(mensagem):
    mensagem = mensagem.lower()
    for intent in intents_data:
        for pattern in intent["patterns"]:
            if re.search(r'\b' + re.escape(pattern.lower()) + r'\b', mensagem):
                return random.choice(intent["responses"])
    return "🌙 Não consegui processar sua solicitação."

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    
    # Verifica chave de API
    chave = data.get("api_key")
    if chave != API_KEY:
        return jsonify({"response": "❌ Chave de API inválida."}), 401
    
    mensagem = data.get("message", "")
    resposta = buscar_resposta(mensagem)
    return jsonify({"response": resposta})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

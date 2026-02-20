import json
import random
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# =============================
# CARREGAR INTENTS
# =============================
with open("intents.json", "r", encoding="utf-8") as f:
    intents = json.load(f)

# =============================
# FUNÇÃO DE RESPOSTA POR INTENT
# =============================
def responder(texto):
    texto = texto.lower()

    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            if pattern in texto:
                return random.choice(intent["responses"])

    return "🌙 Não entendi muito bem, pode explicar melhor?"

# =============================
# ROTA CHAT
# =============================
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    texto = data.get("texto", "")
    resposta = responder(texto)
    return jsonify({"resposta": resposta})

# =============================
# FRONTEND
# =============================
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

# =============================
# RUN
# =============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

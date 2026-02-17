import json
import random
import numpy as np
from flask import Flask, request, jsonify
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# =============================
# CONFIGURAÇÃO DE SEGURANÇA
# =============================
API_KEY = "luna123"

def check_api_key(req):
    key = req.headers.get("X-API-KEY")
    return key == API_KEY

# =============================
# CARREGAR INTENTS
# =============================
with open("intents.json", "r", encoding="utf-8") as file:
    data = json.load(file)

responses = {}
embeddings_db = []

# =============================
# EMBEDDING SIMPLES
# =============================
def mock_embedding(text):
    vec = [ord(c) for c in text.lower() if c.isalnum()]
    if not vec:
        vec = [0]
    vec = np.array(vec, dtype=float)
    return vec / np.linalg.norm(vec)

# =============================
# PREPARAR BASE
# =============================
for intent in data["intents"]:
    tag = intent["tag"]
    responses[tag] = intent["responses"]
    for pattern in intent["patterns"]:
        embeddings_db.append({
            "tag": tag,
            "embedding": mock_embedding(pattern)
        })

# =============================
# MEMÓRIA CURTA
# =============================
memory_server = {}

def save_memory(user_id, role, text):
    if user_id not in memory_server:
        memory_server[user_id] = []
    memory_server[user_id].append({"role": role, "text": text})
    memory_server[user_id] = memory_server[user_id][-10:]

# =============================
# RESPOSTA
# =============================
def get_response(user_input, user_memory):
    input_emb = mock_embedding(user_input).reshape(1, -1)

    best_score = -1
    best_tag = None

    for item in embeddings_db:
        vec = item["embedding"]
        min_len = min(len(vec), input_emb.shape[1])
        score = cosine_similarity(
            input_emb[:, :min_len],
            vec[:min_len].reshape(1, -1)
        )[0][0]

        if score > best_score:
            best_score = score
            best_tag = item["tag"]

    if best_score < 0.7:
        return "🌙 Não entendi muito bem, pode explicar melhor?"

    return random.choice(responses[best_tag])

# =============================
# ENDPOINT CHAT (PROTEGIDO)
# =============================
@app.route("/chat", methods=["POST"])
def chat():
    if not check_api_key(request):
        return jsonify({"error": "Acesso negado"}), 403

    data = request.get_json()
    user_message = data.get("message", "")
    user_memory_html = data.get("memory", [])
    user_id = request.remote_addr

    save_memory(user_id, "user", user_message)
    combined_memory = memory_server[user_id] + user_memory_html

    response = get_response(user_message, combined_memory)
    save_memory(user_id, "luna", response)

    return jsonify({"response": response})

# =============================
# TESTE LOCAL
# =============================
@app.route("/test")
def test():
    return "API Luna protegida 🔐"

# =============================
# RUN
# =============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

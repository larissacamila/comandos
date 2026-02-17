import json
import random
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)  # 🔥 ESSENCIAL PARA HTML LOCAL / BROWSER

# =============================
# CONFIGURAÇÃO DE SEGURANÇA
# =============================
API_KEY = "luna123"

def check_api_key(req):
    return req.headers.get("X-API-KEY") == API_KEY

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
    norm = np.linalg.norm(vec)
    return vec / norm if norm != 0 else vec

# =============================
# PREPARAR BASE
# =============================
for intent in data["intents"]:
    tag = intent["tag"]
    responses[tag] = intent.get("responses", [])
    for pattern in intent.get("patterns", []):
        embeddings_db.append({
            "tag": tag,
            "embedding": mock_embedding(pattern)
        })

# =============================
# MEMÓRIA CURTA
# =============================
memory_server = {}

def save_memory(user_id, role, text):
    if not text:
        return
    if user_id not in memory_server:
        memory_server[user_id] = []
    memory_server[user_id].append({"role": role, "text": text})
    memory_server[user_id] = memory_server[user_id][-10:]

# =============================
# RESPOSTA
# =============================
def get_response(user_input):
    if not user_input:
        return "🌙 Pode falar comigo 😊"

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

    if best_tag is None or best_score < 0.7:
        return "🌙 Não entendi muito bem, pode explicar melhor?"

    return random.choice(responses.get(best_tag, ["🌙 Ok 😊"]))

# =============================
# ENDPOINT CHAT (PROTEGIDO)
# =============================
@app.route("/chat", methods=["POST"])
def chat():
    if not check_api_key(request):
        return jsonify({"error": "Acesso negado"}), 403

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"response": "🌙 Não recebi a mensagem."})

    user_message = data.get("message", "").strip()
    user_id = request.remote_addr or "anon"

    save_memory(user_id, "user", user_message)
    response = get_response(user_message)
    save_memory(user_id, "luna", response)

    return jsonify({"response": response})

# =============================
# TESTE
# =============================
@app.route("/test")
def test():
    return jsonify({"status": "ok", "msg": "API Luna protegida 🔐"})

# =============================
# RUN
# =============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

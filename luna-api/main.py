import json
import random
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

# Carregar intents
with open("intents.json", "r", encoding="utf-8") as file:
    data = json.load(file)

patterns = []
tags = []
responses = {}

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        patterns.append(pattern.lower())
        tags.append(intent["tag"])
    responses[intent["tag"]] = intent["responses"]

# Vetorização
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(patterns)

def get_response(user_input):
    user_input = user_input.lower()
    user_vec = vectorizer.transform([user_input])

    similarities = cosine_similarity(user_vec, X)
    best_match = similarities.argmax()
    confidence = similarities[0][best_match]

    fallbacks = [
        "🌙 Não entendi muito bem sua pergunta. Você pode me dar mais detalhes?",
        "🌙 Pode explicar um pouco melhor?",
        "🌙 Acho que perdi alguma coisa 😅 pode reformular?",
        "🌙 Me conta com outras palavras?"
    ]

    if confidence < 0.3:
        return random.choice(fallbacks)

    tag = tags[best_match]
    return random.choice(responses[tag])

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    response = get_response(user_message)
    return jsonify({"response": response})

@app.route("/test")
def test():
    msg = request.args.get("msg", "")
    resposta = get_response(msg)
    return f"<h2>Luna:</h2><p>{resposta}</p>"

@app.route("/")
def index():
    return "API Luna online 🚀"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

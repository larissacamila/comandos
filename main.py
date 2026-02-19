from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "API Luna ONLINE"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    texto = data.get("texto", "")
    return jsonify({
        "resposta": f"Luna recebeu: {texto}"
    })

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

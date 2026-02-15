from flask import Flask, request, jsonify
import json
import requests
import os

app = Flask(__name__)

# --- CONFIGURAÇÕES ---
API_KEY = "156478"  # coloque sua chave aqui
ESP32_URL = "http://192.168.15.80:5000/comando"  # IP do seu ESP32# ajuste para o IP do seu ESP32

# Carregar intents
with open("intents.json", "r", encoding="utf-8") as f:
    intents = json.load(f)

# Função para buscar resposta baseada nos intents
def buscar_resposta(mensagem):
    mensagem = mensagem.lower()
    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            if pattern.lower() in mensagem:
                return intent["responses"][0]  # pega a primeira resposta
    return "🌙 Não consegui processar sua solicitação."

# Função para enviar comandos ao ESP32
def enviar_para_esp32(comando):
    try:
        response = requests.post(ESP32_URL, json={"comando": comando}, timeout=2)
        if response.status_code == 200:
            return True
    except Exception as e:
        print("Erro ao enviar para ESP32:", e)
    return False

# Rota principal da API
@app.route("/predict", methods=["POST"])
def predict():
    # Verifica chave de API
    chave = request.headers.get("Authorization")
    if not chave or chave != f"Bearer {API_KEY}":
        return jsonify({"response": "⚠️ Chave de API inválida."}), 401

    data = request.get_json()
    mensagem = data.get("message")
    if not mensagem:
        return jsonify({"response": "⚠️ Nenhuma mensagem recebida."}), 400

    resposta = buscar_resposta(mensagem)

    # Comandos conhecidos do ESP32
    comandos_esp = [
        "ligar luz", "desligar luz", "fazer café",
        "ligar pino 1", "desligar pino 1",
        "ligar pino 2", "desligar pino 2",
        "ligar pino 3", "desligar pino 3",
        "ligar pino 4", "desligar pino 4"
    ]
    if resposta in comandos_esp:
        enviado = enviar_para_esp32(resposta)
        if enviado:
            resposta += " ✅ Comando enviado ao ESP32."
        else:
            resposta += " ⚠️ Falha ao enviar comando ao ESP32."

    return jsonify({"response": resposta})

# Teste simples
@app.route("/", methods=["GET"])
def home():
    return "API da Luna está online 🌙"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



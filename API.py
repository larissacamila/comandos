# API.py
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# CONFIGURAÇÃO
ESP32_IP = "http://192.168.15.80"  # IP do ESP32
ESP32_API_KEY = "156478"   # chave do ESP32

# Função para enviar comando para o ESP32
def enviar_para_esp32(comando):
    try:
        resp = requests.post(f"{ESP32_IP}/comando", json={"comando": comando, "key": ESP32_API_KEY}, timeout=5)
        if resp.status_code == 200:
            return {"status": "sucesso", "comando": comando, "mensagem": "Comando enviado para ESP32"}
        else:
            return {"status": "erro", "mensagem": f"ESP32 respondeu: {resp.text}"}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

# Endpoint principal de comando
@app.route("/comando", methods=["POST"])
def comando():
    data = request.json
    if not data or "comando" not in data:
        return jsonify({"status": "erro", "mensagem": "Comando não fornecido"}), 400

    comando = data["comando"]
    resultado = enviar_para_esp32(comando)
    return jsonify(resultado)

# Endpoint de teste
@app.route("/", methods=["GET"])
def raiz():
    return jsonify({"mensagem": "API Luna ativa. Use /comando para enviar comandos."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



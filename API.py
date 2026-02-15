from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# IP do seu ESP32 na rede local
ESP32_IP = "192.168.15.80"

# Chave da API
API_KEY = "156478"  # Coloque aqui sua chave secreta

# Função para enviar comando para o ESP32
def enviar_comando_esp(comando):
    try:
        url = f"http://{ESP32_IP}/{comando}"  # ESP deve ter endpoints tipo /ligar_luz
        resp = requests.get(url, timeout=3)
        if resp.status_code == 200:
            return True, resp.text
        else:
            return False, f"Erro do ESP32: {resp.status_code}"
    except Exception as e:
        return False, str(e)

# Verifica chave
def checar_chave():
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        return False
    token = auth.split(" ")[1]
    return token == API_KEY

@app.route("/comando", methods=["POST"])
def comando():
    if not checar_chave():
        return jsonify({"status": "erro", "mensagem": "Chave inválida"}), 401

    data = request.json
    if not data or "comando" not in data:
        return jsonify({"status": "erro", "mensagem": "Comando não fornecido"}), 400

    comando = data["comando"]
    sucesso, resultado = enviar_comando_esp(comando)
    
    if sucesso:
        return jsonify({"status": "ok", "mensagem": f"Comando '{comando}' executado com sucesso!", "resposta_esp": resultado})
    else:
        return jsonify({"status": "erro", "mensagem": f"Falha ao executar '{comando}'", "erro": resultado}), 500

@app.route("/teste", methods=["GET"])
def teste():
    if not checar_chave():
        return jsonify({"status": "erro", "mensagem": "Chave inválida"}), 401
    return jsonify({"status": "ok", "mensagem": "API funcionando!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


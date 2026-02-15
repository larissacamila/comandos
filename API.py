from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # ✅ Permite requisições de qualquer origem

# Configurações do ESP32
ESP32_IP = "192.168.15.80"  # IP do seu ESP32
ESP32_PORT = 80             # porta do ESP32
ESP32_ENDPOINT = f"http://{ESP32_IP}:{ESP32_PORT}/comando"  # endpoint do ESP32
API_KEY = "156478"  # coloque sua chave se precisar autenticar clientes

# Função para enviar comandos ao ESP32
def enviar_para_esp32(comando: str):
    try:
        payload = {"comando": comando}
        response = requests.post(ESP32_ENDPOINT, json=payload, timeout=3)
        if response.status_code == 200:
            return True, response.text
        return False, f"Erro ESP32: {response.status_code}"
    except Exception as e:
        return False, str(e)

# Endpoint principal
@app.route('/predict', methods=['POST'])
def predict():
    auth = request.headers.get("Authorization")
    if API_KEY and auth != f"Bearer {API_KEY}":
        return jsonify({"response": "Acesso negado: chave inválida"}), 401

    data = request.get_json()
    mensagem = data.get("message", "").lower().strip()

    # Lista simples de comandos
    comandos_esp = {
        "ligar luz": "LIGAR_LUZ",
        "desligar luz": "DESLIGAR_LUZ",
        "fazer café": "FAZER_CAFE",
        "hora": "MOSTRAR_HORA",
        # alertas e outros comandos podem ser adicionados
    }

    # Se for comando do ESP, envia
    if mensagem in comandos_esp:
        sucesso, resultado = enviar_para_esp32(comandos_esp[mensagem])
        if sucesso:
            return jsonify({"response": f"🌙 Comando '{mensagem}' executado com sucesso!"})
        else:
            return jsonify({"response": f"🌙 Falha ao executar comando: {resultado}"})

    # Caso não seja comando conhecido, só responde via API de intents
    # Aqui você pode integrar seu intents.json ou outra lógica
    resposta_padrao = f"🌙 Recebi sua mensagem: {mensagem}"
    return jsonify({"response": resposta_padrao})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



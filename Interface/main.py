import requests

BASE_URL = "http://127.0.0.1:5000"


# comandos para API
def enviar_comando(opcao):
    url = f"{BASE_URL}/comando"
    try:
        response = requests.post(url, json={"opcao": opcao})
        return response.json()
    except Exception as e:
        return {"status": f"Erro de conexão: {str(e)}"}

def adicionar_sensor(nome, protocolo, tensao):
    url = f"{BASE_URL}/Sensores/Adicionar"
    dados = {
        "sensor": {
            "nome": nome,
            "protocolo": protocolo,
            "tensao": tensao
        }
    }
    try:
        response = requests.post(url, json=dados)
        return response.json()
    except Exception as e:
        return {"status": f"Erro de conexão: {str(e)}"}
import requests

API_URL = "http://127.0.0.1:5000"
TAMANHO_BUFFER_PADRAO = 1000


def post_api(rota, payload):
    try:
        resposta = requests.post(API_URL + rota, json=payload, timeout=5)
        return resposta.json()
    except Exception as erro:
        return {"sucesso": False, "mensagem": str(erro)}


def get_api(rota):
    try:
        resposta = requests.get(API_URL + rota, timeout=5)
        return resposta.json()
    except Exception as erro:
        return {"sucesso": False, "mensagem": str(erro)}


def cancelar_fluxo():
    return post_api("/Sistema/Comandos", {"comando": "cancelar_fluxo"})


def enviar_comando(comando):
    cancelar_fluxo()
    return post_api("/Sistema/Comandos", {"comando": comando})


def listar_sensores_virtuais():
    return get_api("/Sistema/SensoresVirtuais/Lista")


def adicionar_sensor_virtual(nome, protocolo, tensao):
    payload = {"nome": nome, "tensao": tensao, "protocolo": protocolo, "tamanhoBuffer": TAMANHO_BUFFER_PADRAO}
    return post_api("/Sistema/SensoresVirtuais/Adicionar", payload)


def remover_sensor_virtual(endereco):
    return post_api("/Sistema/SensoresVirtuais/Remover", {"endereco": endereco})


def simular_sensor_virtual(endereco):
    resposta_post = post_api("/Sistema/SensoresVirtuais/Simulacao", {"endereco": endereco})

    if not resposta_post.get("sucesso", False):
        return resposta_post

    return get_api("/Sistema/SensoresVirtuais/Simulacao")


def processar_sinais_virtual(endereco):
    resposta_post = post_api("/Sistema/SensoresVirtuais/ProcessamentoDeSinais", {"endereco": endereco})

    if not resposta_post.get("sucesso", False):
        return resposta_post

    return get_api("/Sistema/SensoresVirtuais/ProcessamentoDeSinais")


def ler_sensor_real():
    return get_api("/Sistema/SensorReal/Dados")


def processar_sinais_real():
    return get_api("/Sistema/SensorReal/ProcessamentoDeSinais")
from flask import Blueprint, request, jsonify
import socket
import json

routes = Blueprint("routes", __name__)

CPP_IP = "127.0.0.1"
CPP_PORT = 8080
TIMEOUT_CPP = 5

ROTA_COMANDOS = "/Sistema/Comandos"
ROTA_ADICIONAR = "/Sistema/SensoresVirtuais/Adicionar"
ROTA_REMOVER = "/Sistema/SensoresVirtuais/Remover"
ROTA_SIMULACAO = "/Sistema/SensoresVirtuais/Simulacao"
ROTA_PROCESSAMENTO = "/Sistema/SensoresVirtuais/ProcessamentoDeSinais"

estado_fluxo = {
    "rota_esperada": ROTA_COMANDOS,
    "comando_atual": None
}

topico_sensores_virtuais = {"sucesso": True, "mensagem": "Nenhum sensor virtual cadastrado.", "sensores": []}
topico_simulacao_virtual = {"sucesso": False, "mensagem": "Nenhuma simulacao realizada.", "sinal": []}
topico_processamento_virtual = {"sucesso": False, "mensagem": "Nenhum processamento realizado.", "metricas": {}, "sinais": {}}

config_sensor_real = {
    "configurado": False,
    "portaSerial": "",
    "baudRate": 115200,
    "tamanhoBuffer": 50
}

topico_sensor_real_dados = {"sucesso": False, "mensagem": "Sensor real ainda nao configurado.", "sinal": []}
topico_sensor_real_processamento = {"sucesso": False, "mensagem": "Sensor real ainda nao configurado.", "metricas": {}, "sinais": {}}


def enviar_para_cpp(payload):
    try:
        mensagem = json.dumps(payload) + "\n"

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            cliente.settimeout(TIMEOUT_CPP)
            cliente.connect((CPP_IP, CPP_PORT))
            cliente.sendall(mensagem.encode("utf-8"))

            resposta = ""
            while True:
                parte = cliente.recv(4096).decode("utf-8")

                if not parte:
                    break

                resposta += parte

                if "\n" in resposta:
                    break

        resposta = resposta.strip()

        if resposta == "":
            return {"sucesso": False, "mensagem": "C++ nao retornou resposta."}

        return json.loads(resposta)

    except socket.timeout:
        return {"sucesso": False, "mensagem": "Timeout na comunicacao com o C++."}

    except ConnectionRefusedError:
        return {"sucesso": False, "mensagem": "Nao foi possivel conectar ao servidor C++."}

    except json.JSONDecodeError:
        return {"sucesso": False, "mensagem": "Resposta do C++ nao esta em JSON valido."}

    except Exception as erro:
        return {"sucesso": False, "mensagem": str(erro)}


def voltar_para_comandos():
    estado_fluxo["rota_esperada"] = ROTA_COMANDOS
    estado_fluxo["comando_atual"] = None


def definir_proxima_rota(comando):
    if comando == "adicionar_sensor_virtual":
        return ROTA_ADICIONAR

    if comando == "abrir_remocao_sensor_virtual":
        return ROTA_REMOVER

    if comando == "abrir_simulacao_sensor_virtual":
        return ROTA_SIMULACAO

    if comando == "abrir_processamento_sensor_virtual":
        return ROTA_PROCESSAMENTO

    return None


def rota_esta_liberada(rota):
    return estado_fluxo["rota_esperada"] == rota


def atualizar_lista_sensores_virtuais():
    global topico_sensores_virtuais

    payload_cpp = {"comando": "listar_sensores_virtuais", "dados": {}}
    resposta_cpp = enviar_para_cpp(payload_cpp)

    if resposta_cpp.get("sucesso", False):
        topico_sensores_virtuais = resposta_cpp

    return resposta_cpp


def validar_config_sensor_real(dados):
    if dados is None:
        return False, "JSON invalido ou vazio."

    if "portaSerial" not in dados:
        return False, "Campo obrigatorio ausente: portaSerial"

    if "baudRate" not in dados:
        return False, "Campo obrigatorio ausente: baudRate"

    if "tamanhoBuffer" not in dados:
        return False, "Campo obrigatorio ausente: tamanhoBuffer"

    try:
        baud_rate = int(dados["baudRate"])
        tamanho_buffer = int(dados["tamanhoBuffer"])
    except (ValueError, TypeError):
        return False, "baudRate e tamanhoBuffer devem ser numericos."

    if str(dados["portaSerial"]).strip() == "":
        return False, "portaSerial nao pode ser vazia."

    if baud_rate not in [9600, 19200, 38400, 57600, 115200]:
        return False, "baudRate invalido. Use uma das opcoes: 9600, 19200, 38400, 57600 ou 115200."

    if tamanho_buffer not in [25, 50, 100]:
        return False, "tamanhoBuffer invalido. Use uma das opcoes: 25, 50 ou 100."

    return True, ""


def montar_payload_leitura_sensor_real():
    return {
        "comando": "ler_dados_sensor_real",
        "dados": {
            "portaSerial": config_sensor_real["portaSerial"],
            "baudRate": config_sensor_real["baudRate"],
            "tamanhoBuffer": config_sensor_real["tamanhoBuffer"]
        }
    }


def montar_payload_processamento_sensor_real():
    return {
        "comando": "processar_sinais_sensor_real",
        "dados": {
            "portaSerial": config_sensor_real["portaSerial"],
            "baudRate": config_sensor_real["baudRate"],
            "tamanhoBuffer": config_sensor_real["tamanhoBuffer"]
        }
    }


@routes.route("/Sistema/Comandos", methods=["POST"])
def comando():
    dados = request.get_json()

    if dados is None:
        return jsonify({"sucesso": False, "mensagem": "JSON invalido ou vazio."}), 400

    comando_recebido = dados.get("comando", "")

    if comando_recebido == "cancelar_fluxo":
        voltar_para_comandos()
        return jsonify({"sucesso": True, "mensagem": "Fluxo cancelado.", "proximaRota": ROTA_COMANDOS})

    if estado_fluxo["rota_esperada"] != ROTA_COMANDOS:
        return jsonify({
            "sucesso": False,
            "mensagem": "Existe uma acao secundaria pendente.",
            "rotaEsperada": estado_fluxo["rota_esperada"],
            "comandoAtual": estado_fluxo["comando_atual"]
        }), 409

    proxima_rota = definir_proxima_rota(comando_recebido)

    if proxima_rota is None:
        return jsonify({"sucesso": False, "mensagem": "Comando desconhecido."}), 400

    if comando_recebido in ["abrir_remocao_sensor_virtual", "abrir_simulacao_sensor_virtual", "abrir_processamento_sensor_virtual"]:
        resposta_lista = atualizar_lista_sensores_virtuais()

        if not resposta_lista.get("sucesso", False):
            return jsonify(resposta_lista), 500

    estado_fluxo["rota_esperada"] = proxima_rota
    estado_fluxo["comando_atual"] = comando_recebido

    return jsonify({
        "sucesso": True,
        "mensagem": "Comando recebido. API aguardando rota secundaria.",
        "proximaRota": proxima_rota,
        "topicoLista": "/Sistema/SensoresVirtuais/Lista" if comando_recebido != "adicionar_sensor_virtual" else None
    })


@routes.route("/Sistema/SensoresVirtuais/Lista", methods=["GET"])
def listar_sensores_virtuais():
    return jsonify(topico_sensores_virtuais)


@routes.route("/Sistema/SensoresVirtuais/Adicionar", methods=["POST"])
def adicionar_sensor():
    if not rota_esta_liberada(ROTA_ADICIONAR):
        return jsonify({"sucesso": False, "mensagem": "Rota nao liberada. Envie primeiro o comando em /Sistema/Comandos.", "rotaEsperada": estado_fluxo["rota_esperada"]}), 409

    dados = request.get_json()

    if dados is None:
        return jsonify({"sucesso": False, "mensagem": "JSON invalido ou vazio."}), 400

    campos = ["nome", "tensao", "protocolo", "tamanhoBuffer"]

    for campo in campos:
        if campo not in dados:
            return jsonify({"sucesso": False, "mensagem": f"Campo obrigatorio ausente: {campo}"}), 400

    payload_cpp = {"comando": "adicionar_sensor_virtual", "dados": dados}
    resposta_cpp = enviar_para_cpp(payload_cpp)

    if resposta_cpp.get("sucesso", False):
        atualizar_lista_sensores_virtuais()

    voltar_para_comandos()
    return jsonify(resposta_cpp)


@routes.route("/Sistema/SensoresVirtuais/Remover", methods=["POST"])
def remover_sensor():
    if not rota_esta_liberada(ROTA_REMOVER):
        return jsonify({"sucesso": False, "mensagem": "Rota nao liberada. Envie primeiro o comando em /Sistema/Comandos.", "rotaEsperada": estado_fluxo["rota_esperada"]}), 409

    dados = request.get_json()

    if dados is None:
        return jsonify({"sucesso": False, "mensagem": "JSON invalido ou vazio."}), 400

    if "endereco" not in dados:
        return jsonify({"sucesso": False, "mensagem": "Campo obrigatorio ausente: endereco"}), 400

    payload_cpp = {"comando": "remover_sensor_virtual", "dados": {"endereco": dados["endereco"]}}
    resposta_cpp = enviar_para_cpp(payload_cpp)

    if resposta_cpp.get("sucesso", False):
        atualizar_lista_sensores_virtuais()

    voltar_para_comandos()
    return jsonify(resposta_cpp)


@routes.route("/Sistema/SensoresVirtuais/Simulacao", methods=["POST"])
def selecionar_sensor_simulacao():
    global topico_simulacao_virtual

    if not rota_esta_liberada(ROTA_SIMULACAO):
        return jsonify({"sucesso": False, "mensagem": "Rota nao liberada. Envie primeiro o comando em /Sistema/Comandos.", "rotaEsperada": estado_fluxo["rota_esperada"]}), 409

    dados = request.get_json()

    if dados is None:
        return jsonify({"sucesso": False, "mensagem": "JSON invalido ou vazio."}), 400

    if "endereco" not in dados:
        return jsonify({"sucesso": False, "mensagem": "Campo obrigatorio ausente: endereco"}), 400

    payload_cpp = {"comando": "simular_sensor_virtual", "dados": {"endereco": dados["endereco"]}}
    resposta_cpp = enviar_para_cpp(payload_cpp)

    if resposta_cpp.get("sucesso", False):
        topico_simulacao_virtual = resposta_cpp

    voltar_para_comandos()
    return jsonify({"sucesso": resposta_cpp.get("sucesso", False), "mensagem": resposta_cpp.get("mensagem", ""), "topico": "/Sistema/SensoresVirtuais/Simulacao"})


@routes.route("/Sistema/SensoresVirtuais/Simulacao", methods=["GET"])
def ler_simulacao():
    return jsonify(topico_simulacao_virtual)


@routes.route("/Sistema/SensoresVirtuais/ProcessamentoDeSinais", methods=["POST"])
def selecionar_sensor_processamento():
    global topico_processamento_virtual

    if not rota_esta_liberada(ROTA_PROCESSAMENTO):
        return jsonify({"sucesso": False, "mensagem": "Rota nao liberada. Envie primeiro o comando em /Sistema/Comandos.", "rotaEsperada": estado_fluxo["rota_esperada"]}), 409

    dados = request.get_json()

    if dados is None:
        return jsonify({"sucesso": False, "mensagem": "JSON invalido ou vazio."}), 400

    if "endereco" not in dados:
        return jsonify({"sucesso": False, "mensagem": "Campo obrigatorio ausente: endereco"}), 400

    payload_cpp = {"comando": "processar_sinais_sensor_virtual", "dados": {"endereco": dados["endereco"]}}
    resposta_cpp = enviar_para_cpp(payload_cpp)

    if resposta_cpp.get("sucesso", False):
        topico_processamento_virtual = resposta_cpp

    voltar_para_comandos()
    return jsonify({"sucesso": resposta_cpp.get("sucesso", False), "mensagem": resposta_cpp.get("mensagem", ""), "topico": "/Sistema/SensoresVirtuais/ProcessamentoDeSinais"})


@routes.route("/Sistema/SensoresVirtuais/ProcessamentoDeSinais", methods=["GET"])
def ler_processamento_de_sinais():
    return jsonify(topico_processamento_virtual)


@routes.route("/Sistema/SensorReal/Dados", methods=["POST", "GET"])
def ler_dados_reais():
    global config_sensor_real
    global topico_sensor_real_dados

    if request.method == "POST":
        dados = request.get_json()
        valido, mensagem = validar_config_sensor_real(dados)

        if not valido:
            return jsonify({"sucesso": False, "mensagem": mensagem, "sinal": []}), 400

        config_sensor_real["configurado"] = True
        config_sensor_real["portaSerial"] = str(dados["portaSerial"]).strip()
        config_sensor_real["baudRate"] = int(dados["baudRate"])
        config_sensor_real["tamanhoBuffer"] = int(dados["tamanhoBuffer"])

        payload_cpp = montar_payload_leitura_sensor_real()
        resposta_cpp = enviar_para_cpp(payload_cpp)

        if resposta_cpp.get("sucesso", False):
            topico_sensor_real_dados = resposta_cpp
        else:
            topico_sensor_real_dados = {
                "sucesso": False,
                "mensagem": resposta_cpp.get("mensagem", "Erro ao ler sensor real."),
                "sinal": []
            }

        return jsonify(topico_sensor_real_dados)

    if request.method == "GET":
        if not config_sensor_real["configurado"]:
            return jsonify({
                "sucesso": False,
                "mensagem": "Sensor real ainda nao configurado. Envie primeiro portaSerial, baudRate e tamanhoBuffer.",
                "sinal": []
            }), 400

        payload_cpp = montar_payload_leitura_sensor_real()
        resposta_cpp = enviar_para_cpp(payload_cpp)

        if resposta_cpp.get("sucesso", False):
            topico_sensor_real_dados = resposta_cpp
        else:
            topico_sensor_real_dados = {
                "sucesso": False,
                "mensagem": resposta_cpp.get("mensagem", "Erro ao ler sensor real."),
                "sinal": []
            }

        return jsonify(topico_sensor_real_dados)


@routes.route("/Sistema/SensorReal/ProcessamentoDeSinais", methods=["GET"])
def ler_processamento_real():
    global topico_sensor_real_processamento

    if not config_sensor_real["configurado"]:
        return jsonify({
            "sucesso": False,
            "mensagem": "Sensor real ainda nao configurado. Configure portaSerial, baudRate e tamanhoBuffer antes de processar.",
            "metricas": {},
            "sinais": {}
        }), 400

    payload_cpp = montar_payload_processamento_sensor_real()
    resposta_cpp = enviar_para_cpp(payload_cpp)

    if resposta_cpp.get("sucesso", False):
        topico_sensor_real_processamento = resposta_cpp
    else:
        topico_sensor_real_processamento = {
            "sucesso": False,
            "mensagem": resposta_cpp.get("mensagem", "Erro ao processar sensor real."),
            "metricas": {},
            "sinais": {}
        }

    return jsonify(topico_sensor_real_processamento)

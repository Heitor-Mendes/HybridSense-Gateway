from flask import Flask, request, jsonify

import socket

app = Flask(__name__)

#Porta de escuta e envio do C++ (half-duplex)
CPP_IP = "127.0.0.1"
CPP_PORT = 8080

# Interface ➝ posta "{Comando : ValorComando}" para API ➝ C++ escuta nesse rota e internamente
# comeca a ouvir outro topico e dependendo do comando posta um JSON 
@app.route("/Sistema/Comandos", methods=["POST"])

def comando():
    pass

# Interface ➝ posta " {Endereco : Endereco, nome: nome , etc...}" ➝ C++ Adiciona no vector de sensores
@app.route("Sistema/SensoresVirtuais/Adicionar", methods = ["POST"])
def AdicionarSensor():
    pass

# C++ já tendo recebido o comando lista os sensores que será impressa para o usuario
# atraves da interface ➝ Interface posta "{endereco : endereco}" ➝ C++ procura sensor e deleta ele
@app.route("Sistema/SensoresVirtuais/Remover", methods = ["POST"])
def RemoverSensor():
    pass

# C++ já tendo recebido o comando lista os sensores que será impressa para o usuario
# atraves da interface ➝ Interface posta "{endereco : endereco}" ➝ C++ simula e posta na API
# [{"amostra1": "amostra"}, {"amostra2": "amostra"}, etc...] e a interface plota o grafico do
# sinal cru com ruido e tudo
@app.route("Sistema/SensoresVirtuais/Simulacao", methods = ["POST", "GET"])
def SelecionarSensor():
    pass

def LerSimulacao():
    pass 

# C++ já tendo recebido o comando lista os sensores que será impressa para o usuario
# atraves da interface ➝ Interface posta "{endereco : endereco}" ➝ C++ pega os dados da simulacao
# e faz  o processamento de sinais e posta um json com todos os dados a media, min, max etc devem
# ser impresso como string na tela e os vectors (sinal discretizado) deve ser retornado no msm formato
# de json q o sinal cru pq eles tbm devem ser plotados na interface
@app.route("Sistema/SensoresVirtuais/ProcessamentoDeSinais", methods = ["POST", "GET"])

def SelecionarSensor():
    pass

def LerProcessamentoDeSinais():
    pass

#(OBS: Aplicacao se restringe a apenas 1 sensor real) C++ com o comando recebido posta imediatamente
# na rota em questao um json com os dados do barramento serial parseados a interface vai ler isso
# e plotar um grafico com o sinal cru
@app.route("Sistema/SensorReal/Dados", methods = ["GET"])

def LerDadosReais():
    pass

#(OBS: Aplicacao se restringe a apenas 1 sensor real) C++ com o comando recebido e deixou armazenado
# os dados da ultima requisicao de leitura pela interface e faz o processamento de sinais desse
# "buffer" interno e posta imediatamente no mesmo formato dos dados processados para sensores virtuais
# na rota em questao um json e a inteface vai plotar os dados de vector e imprimir na tela as metricas
@app.route("Sistema/SensorReal/ProcessamentoDeSinais", methods =["GET"])

def LerProcessamentoDeSinais():
    pass
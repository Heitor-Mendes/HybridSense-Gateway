from flask import Flask, request, jsonify

import socket

app = Flask(__name__)

#Porta de escuta e envio do C++ (half-duplex)
CPP_IP = "127.0.0.1"
CPP_PORT = 8080


@app.route("/comando", methods=["POST"])

def comando():

    opcao = request.json["opcao"]

    try:

        #Cria socket
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Conecta com o C++
        cliente.connect((CPP_IP, CPP_PORT))

        #Envia a mensagem (opcao selecionada)
        cliente.send(str(opcao).encode())

        #Recebe a resposta do cliente(Devolve resposta para Interface)
        resposta = cliente.recv(1024).decode() # bloqueante ponto de atencao

        cliente.close()

        print(resposta)     #debug
        return jsonify({
            "status": resposta
        })

    except Exception as e:
        print(e)            #debug
        return jsonify({
            "status": str(e)
        })


@app.route("/Sensores/Adicionar", methods = ["POST"])
def AdicionarSensor():
    
    sensor = request.json["sensor"]

    try:

        #Cria socket
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Conecta com o C++
        cliente.connect((CPP_IP, CPP_PORT))

        #Envia a mensagem (opcao selecionada)
        cliente.send(str(sensor).encode())

        #Recebe a resposta do cliente(Devolve resposta para Interface)
        resposta = cliente.recv(1024).decode() # bloqueante ponto de atencao

        cliente.close()

        print(resposta)     # debug
        
        return jsonify({
            "status": resposta
        })

    except Exception as e:
        
        print(e)            # debug
        
        return jsonify({
            "status": str(e)
        })

app.run(port=5000)
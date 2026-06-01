from flask import Flask, request, jsonify

import socket

app = Flask(__name__)

CPP_IP = "127.0.0.1"
CPP_PORT = 8080


@app.route("/comando", methods=["POST"])

def comando():

    opcao = request.json["opcao"]

    try:

        cliente = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        cliente.connect((CPP_IP, CPP_PORT))

        cliente.send(str(opcao).encode())

        resposta = cliente.recv(1024).decode()

        cliente.close()

        return jsonify({
            "status": resposta
        })

    except Exception as e:

        return jsonify({
            "status": str(e)
        })


app.run(port=5000)
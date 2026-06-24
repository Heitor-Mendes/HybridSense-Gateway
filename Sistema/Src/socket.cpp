#include "../Include/socket.h"

#include <iostream>
#include <stdexcept>

ServidorTCP::ServidorTCP(int porta) {
    this->porta = porta;
    servidorFD = INVALID_SOCKET_VAL;

#ifdef _WIN32
    winsockInicializado = false;
    WSADATA wsa;

    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) {
        throw runtime_error("Falha no WSAStartup.");
    }

    winsockInicializado = true;
#endif
}

ServidorTCP::~ServidorTCP() {
    if (servidorFD != INVALID_SOCKET_VAL) {
        CLOSE_SOCKET(servidorFD);
        servidorFD = INVALID_SOCKET_VAL;
    }

#ifdef _WIN32
    if (winsockInicializado) {
        WSACleanup();
    }
#endif
}

void ServidorTCP::iniciar() {
    servidorFD = socket(AF_INET, SOCK_STREAM, 0);

    if (servidorFD == INVALID_SOCKET_VAL) {
        throw runtime_error("Erro ao criar socket.");
    }

    int opt = 1;
    setsockopt(servidorFD, SOL_SOCKET, SO_REUSEADDR, (const char*)&opt, sizeof(opt));

    sockaddr_in endereco{};
    endereco.sin_family = AF_INET;
    endereco.sin_port = htons(porta);
    endereco.sin_addr.s_addr = INADDR_ANY;

    if (bind(servidorFD, (sockaddr*)&endereco, sizeof(endereco)) < 0) {
        throw runtime_error("Erro no bind.");
    }

    if (listen(servidorFD, 5) < 0) {
        throw runtime_error("Erro no listen.");
    }

    cout << "Servidor TCP C++ escutando na porta " << porta << "..." << endl;
}

socket_t ServidorTCP::aceitarCliente() {
    socket_t cliente = accept(servidorFD, nullptr, nullptr);

    if (cliente == INVALID_SOCKET_VAL) {
        throw runtime_error("Erro ao aceitar cliente.");
    }

    return cliente;
}

string ServidorTCP::receberLinha(socket_t cliente) {
    string mensagem;
    char caractere;

    while (true) {
        int bytesRecebidos = recv(cliente, &caractere, 1, 0);

        if (bytesRecebidos <= 0) {
            break;
        }

        if (caractere == '\n') {
            break;
        }

        mensagem += caractere;
    }

    return mensagem;
}

int ServidorTCP::enviar(socket_t cliente, const string& mensagem) {
    int totalEnviado = 0;
    int tamanho = mensagem.size();

    while (totalEnviado < tamanho) {
        int enviados = send(cliente, mensagem.c_str() + totalEnviado, tamanho - totalEnviado, 0);

        if (enviados <= 0) {
            return enviados;
        }

        totalEnviado += enviados;
    }

    return totalEnviado;
}

int ServidorTCP::enviarLinha(socket_t cliente, const string& mensagem) {
    return enviar(cliente, mensagem + "\n");
}

void ServidorTCP::fecharCliente(socket_t cliente) {
    if (cliente != INVALID_SOCKET_VAL) {
        CLOSE_SOCKET(cliente);
    }
}
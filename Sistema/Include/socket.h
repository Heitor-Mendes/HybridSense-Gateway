#ifndef SERVIDOR_TCP_H
#define SERVIDOR_TCP_H

#include <winsock2.h>
#include <ws2tcpip.h>

typedef SOCKET socket_t;

#define CLOSE_SOCKET closesocket
#define INVALID_SOCKET_VAL INVALID_SOCKET

#include <string>

using namespace std;

class ServidorTCP {
    public:
        ServidorTCP(int porta);
        ~ServidorTCP();

        void iniciar();
        socket_t aceitarCliente();
        string receberLinha(socket_t cliente);
        int enviar(socket_t cliente, const string& mensagem);
        int enviarLinha(socket_t cliente, const string& mensagem);
        void fecharCliente(socket_t cliente);

    private:
        int porta;
        socket_t servidorFD;
        bool winsockInicializado;
};

#endif

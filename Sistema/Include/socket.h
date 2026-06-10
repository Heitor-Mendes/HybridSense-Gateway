#ifndef SOCKET_H

#define SOCKET_H

#include <iostream>
#include <string>
#include <stdexcept>


// Rodando em Linux e Windows
#ifdef _WIN32
    #include <winsock2.h>
    #include <ws2tcpip.h>
    #pragma comment(lib, "ws2_32.lib") // Linka a lib necessária no MSVC
    typedef SOCKET socket_t;
    #define INVALID_SOCKET_VAL INVALID_SOCKET
    #define CLOSE_SOCKET(s) closesocket(s)

#else
    #include <sys/socket.h>
    #include <netinet/in.h>
    #include <unistd.h>
    #include <arpa/inet.h>
    typedef int socket_t;
    #define INVALID_SOCKET_VAL -1
    #define CLOSE_SOCKET(s) close(s)
#endif

using namespace std;

class socketTCP{
    private:
        socket_t servidorFD;
        int porta;

    public:
        
        socketTCP(int);
        ~socketTCP();

        void iniciar();
        socket_t  ler();
        int enviar(int, const string&);

};

#endif
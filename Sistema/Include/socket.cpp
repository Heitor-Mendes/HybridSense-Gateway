#include "socket.h"

socketTCP::socketTCP(int p) : porta(p), servidorFD(-1) {
    #ifdef _WIN32
            WSADATA wsa;
            if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) throw std::runtime_error("Falha no WSAStartup");
    #endif
}

socketTCP::~socketTCP(){
    if (servidorFD != -1) {
        CLOSE_SOCKET(servidorFD);
    }
    
    #ifdef _WIN32

     WSACleanup();
    #endif
       
}

void socketTCP :: iniciar() {
    servidorFD = socket(AF_INET, SOCK_STREAM, 0);
        if (servidorFD == INVALID_SOCKET_VAL) throw std::runtime_error("Erro ao criar socket");

    // Permitir reuso da porta (evita erro de 'Address already in use')
    int opt = 1;    
    setsockopt(servidorFD, SOL_SOCKET, SO_REUSEADDR, (const char*)&opt, sizeof(opt));
    sockaddr_in endereco{};
    endereco.sin_family = AF_INET;
    endereco.sin_port = htons(porta);
    endereco.sin_addr.s_addr = INADDR_ANY;

    if (bind(servidorFD, (sockaddr*)&endereco, sizeof(endereco)) < 0)
        throw runtime_error("Erro no bind");

    listen(servidorFD, 5);
    cout << "Servidor escutando na porta " << porta << "..." << std::endl;
}


socket_t socketTCP::ler() {
        return accept(servidorFD, nullptr, nullptr);
}
int socketTCP ::enviar(int cliente, const string& mensagem) {
        return send(cliente, mensagem.c_str(), mensagem.size(), 0);
}
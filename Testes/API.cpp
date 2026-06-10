// servidor.cpp

#include <iostream>
#include <string>

#ifdef _WIN32
#include <winsock2.h>
#pragma comment(lib, "ws2_32.lib")
#else
#include <arpa/inet.h>
#include <unistd.h>
#endif

int main(){

#ifdef _WIN32
    WSADATA wsa;
    WSAStartup(MAKEWORD(2,2), &wsa);
#endif

    int servidor = socket(AF_INET, SOCK_STREAM, 0);

    sockaddr_in endereco{};
    endereco.sin_family = AF_INET;
    endereco.sin_port = htons(8080);
    endereco.sin_addr.s_addr = INADDR_ANY;

    bind( servidor, (sockaddr*)&endereco, sizeof(endereco));

    listen(servidor, 5);

    std::cout << "Servidor C++ iniciado\n";

    while(true){

        int cliente = accept(servidor, nullptr, nullptr);

        char buffer[1024] = {};

        recv( cliente, buffer, sizeof(buffer), 0);

        int opcao = std::stoi(buffer);

        std::string resposta;

        switch(opcao){

            case 1:
                resposta = "Executando rotina 1";
                break;

            case 2:
                resposta = "Executando rotina 2";
                break;

            case 3:
                resposta = "Executando rotina 3";
                break;

            case 4:
                resposta = "Executando rotina 4";
                break;

            case 5:
                resposta = "Executando rotina 5";
                break;

            case 6:
                resposta = "Executando rotina 6";
                break;

            case 7:
                resposta = "Executando rotina 7";
                break;

            case 8:
                resposta = "Executando rotina 8";
                break;

            default:
                resposta = "Opcao invalida";
        }

        send(cliente, resposta.c_str(), resposta.size(), 0);

#ifdef _WIN32
        closesocket(cliente);
#else
        close(cliente);
#endif
    }

#ifdef _WIN32
    WSACleanup();
#endif

    return 0;
}
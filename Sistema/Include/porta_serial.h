#ifndef PORTA_SERIAL_H
#define PORTA_SERIAL_H

#include <string>
#include <vector>

using namespace std;

#ifdef _WIN32
    #include <windows.h>
#else
    #include <termios.h>
#endif

class PortaSerial {
    public:
        PortaSerial();
        ~PortaSerial();

        bool abrir(string nomePorta, int baudRate);
        void fechar();
        bool estaAberta() const;

        string lerLinha();
        string getNomePorta() const;

        static vector<string> listarPortasDisponiveis();

    private:
        string nomePorta;
        bool aberta;

#ifdef _WIN32
        HANDLE handle;
#else
        int fd;
#endif

        bool configurarPorta(int baudRate);
};

#endif
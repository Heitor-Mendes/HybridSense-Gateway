#ifndef PORTA_SERIAL_H
#define PORTA_SERIAL_H

#include <string>
#include <windows.h>

using namespace std;

class PortaSerial {
    public:
        PortaSerial();
        ~PortaSerial();

        bool abrir(string nomePorta, int baudRate);
        void fechar();
        bool estaAberta() const;

        string lerLinha();
        string getNomePorta() const;

    private:
        string nomePorta;
        bool aberta;
        HANDLE handle;

        bool configurarPorta(int baudRate);
};

#endif

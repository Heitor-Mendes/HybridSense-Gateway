#include "porta_serial.h"

#include <stdexcept>
#include <string>

PortaSerial::PortaSerial() {
    nomePorta = "";
    aberta = false;

    handle = INVALID_HANDLE_VALUE;
}

PortaSerial::~PortaSerial() {
    fechar();
}

bool PortaSerial::abrir(string nomePorta, int baudRate) {
    fechar();

    this->nomePorta = nomePorta;

    string caminhoPorta = nomePorta;

    if (nomePorta.rfind("\\\\.\\", 0) != 0) {
        caminhoPorta = "\\\\.\\" + nomePorta;
    }

    handle = CreateFileA(caminhoPorta.c_str(), GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, 0, NULL);

    if (handle == INVALID_HANDLE_VALUE) {
        aberta = false;
        return false;
    }

    aberta = configurarPorta(baudRate);

    if (!aberta) {
        fechar();
        return false;
    }

    return true;
}

void PortaSerial::fechar() {
    if (handle != INVALID_HANDLE_VALUE) {
        CloseHandle(handle);
        handle = INVALID_HANDLE_VALUE;
    }

    aberta = false;
}

bool PortaSerial::estaAberta() const {
    return aberta;
}

string PortaSerial::getNomePorta() const {
    return nomePorta;
}

bool PortaSerial::configurarPorta(int baudRate) {
    DCB dcbSerialParams;
    ZeroMemory(&dcbSerialParams, sizeof(dcbSerialParams));
    dcbSerialParams.DCBlength = sizeof(dcbSerialParams);

    if (!GetCommState(handle, &dcbSerialParams)) {
        return false;
    }

    dcbSerialParams.BaudRate = baudRate;
    dcbSerialParams.ByteSize = 8;
    dcbSerialParams.StopBits = ONESTOPBIT;
    dcbSerialParams.Parity = NOPARITY;
    dcbSerialParams.fDtrControl = DTR_CONTROL_ENABLE;
    dcbSerialParams.fRtsControl = RTS_CONTROL_ENABLE;

    if (!SetCommState(handle, &dcbSerialParams)) {
        return false;
    }

    COMMTIMEOUTS timeouts;
    ZeroMemory(&timeouts, sizeof(timeouts));
    timeouts.ReadIntervalTimeout = 50;
    timeouts.ReadTotalTimeoutConstant = 100;
    timeouts.ReadTotalTimeoutMultiplier = 10;
    timeouts.WriteTotalTimeoutConstant = 100;
    timeouts.WriteTotalTimeoutMultiplier = 10;

    if (!SetCommTimeouts(handle, &timeouts)) {
        return false;
    }

    PurgeComm(handle, PURGE_RXCLEAR | PURGE_TXCLEAR);

    return true;
}

string PortaSerial::lerLinha() {
    if (!aberta) {
        throw runtime_error("Porta serial nao esta aberta.");
    }

    string linha;
    char c;

    DWORD bytesLidos = 0;

    while (true) {
        bool ok = ReadFile(handle, &c, 1, &bytesLidos, NULL);

        if (!ok || bytesLidos == 0) {
            break;
        }

        if (c == '\n') {
            break;
        }

        if (c != '\r') {
            linha += c;
        }
    }

    return linha;
}

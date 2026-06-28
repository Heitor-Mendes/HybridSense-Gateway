#include "porta_serial.h"

#include <stdexcept>
#include <vector>
#include <string>

#ifdef _WIN32
    #include <windows.h>
#else
    #include <fcntl.h>
    #include <unistd.h>
    #include <dirent.h>
    #include <cstring>
#endif

PortaSerial::PortaSerial() {
    nomePorta = "";
    aberta = false;

#ifdef _WIN32
    handle = INVALID_HANDLE_VALUE;
#else
    fd = -1;
#endif
}

PortaSerial::~PortaSerial() {
    fechar();
}

bool PortaSerial::abrir(string nomePorta, int baudRate) {
    fechar();

    this->nomePorta = nomePorta;

#ifdef _WIN32
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
#else
    fd = open(nomePorta.c_str(), O_RDWR | O_NOCTTY | O_SYNC);

    if (fd < 0) {
        aberta = false;
        return false;
    }

    aberta = configurarPorta(baudRate);

    if (!aberta) {
        fechar();
        return false;
    }

    return true;
#endif
}

void PortaSerial::fechar() {
#ifdef _WIN32
    if (handle != INVALID_HANDLE_VALUE) {
        CloseHandle(handle);
        handle = INVALID_HANDLE_VALUE;
    }
#else
    if (fd >= 0) {
        close(fd);
        fd = -1;
    }
#endif

    aberta = false;
}

bool PortaSerial::estaAberta() const {
    return aberta;
}

string PortaSerial::getNomePorta() const {
    return nomePorta;
}

bool PortaSerial::configurarPorta(int baudRate) {
#ifdef _WIN32
    DCB dcbSerialParams = {0};
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

    COMMTIMEOUTS timeouts = {0};
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
#else
    termios tty;

    if (tcgetattr(fd, &tty) != 0) {
        return false;
    }

    speed_t velocidade;

    switch (baudRate) {
        case 9600: velocidade = B9600; break;
        case 19200: velocidade = B19200; break;
        case 38400: velocidade = B38400; break;
        case 57600: velocidade = B57600; break;
        case 115200: velocidade = B115200; break;
        default: velocidade = B115200; break;
    }

    cfsetospeed(&tty, velocidade);
    cfsetispeed(&tty, velocidade);

    tty.c_cflag = (tty.c_cflag & ~CSIZE) | CS8;
    tty.c_iflag &= ~IGNBRK;
    tty.c_lflag = 0;
    tty.c_oflag = 0;
    tty.c_cc[VMIN] = 0;
    tty.c_cc[VTIME] = 10;

    tty.c_iflag &= ~(IXON | IXOFF | IXANY);
    tty.c_cflag |= (CLOCAL | CREAD);
    tty.c_cflag &= ~(PARENB | PARODD);
    tty.c_cflag &= ~CSTOPB;
    tty.c_cflag &= ~CRTSCTS;

    if (tcsetattr(fd, TCSANOW, &tty) != 0) {
        return false;
    }

    tcflush(fd, TCIOFLUSH);

    return true;
#endif
}

string PortaSerial::lerLinha() {
    if (!aberta) {
        throw runtime_error("Porta serial nao esta aberta.");
    }

    string linha;
    char c;

#ifdef _WIN32
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
#else
    while (true) {
        int bytesLidos = read(fd, &c, 1);

        if (bytesLidos <= 0) {
            break;
        }

        if (c == '\n') {
            break;
        }

        if (c != '\r') {
            linha += c;
        }
    }
#endif

    return linha;
}

vector<string> PortaSerial::listarPortasDisponiveis() {
    vector<string> portas;

#ifdef _WIN32
    for (int i = 1; i <= 30; i++) {
        portas.push_back("COM" + to_string(i));
    }
#else
    DIR* dir = opendir("/dev");

    if (dir == nullptr) {
        return portas;
    }

    dirent* entry;

    while ((entry = readdir(dir)) != nullptr) {
        string nome = entry->d_name;

        if (nome.rfind("ttyUSB", 0) == 0 || nome.rfind("ttyACM", 0) == 0) {
            portas.push_back("/dev/" + nome);
        }
    }

    closedir(dir);
#endif

    return portas;
}
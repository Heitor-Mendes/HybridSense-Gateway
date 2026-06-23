#include "../Include/sensor.h"

#include <stdexcept>
#include <algorithm>
#include <cctype>

Sensor::Sensor(unsigned endereco_, unsigned tamanhoBuffer_, string nome_, float tensaoDeOperacao_, ProtocoloSerial protocolo_, TipoSensor tipo_){
    
    endereco            = endereco_;
    tamanhoBuffer       = tamanhoBuffer_;
    nome                = nome_;
    tensaoDeOperacao    = tensaoDeOperacao_;
    protocolo           = protocolo_;
    tipo                = tipo_;

    buffer.reserve(tamanhoBuffer);
}

Sensor::~Sensor() {
}

unsigned Sensor::getEndereco() const {
    return endereco;
}

string Sensor::getNome() const {
    return nome;
}

float Sensor::getTensaoDeOperacao() const {
    return tensaoDeOperacao;
}

ProtocoloSerial Sensor::getProtocolo() const {
    return protocolo;
}

TipoSensor Sensor::getTipoSensor() const {
    return tipo;
}

const vector<double>& Sensor::getBuffer() const {
    return buffer;
}

double Sensor::getUltimaAmostra() const {
    if (buffer.empty()) {
        throw runtime_error("Buffer vazio. Nao existe ultima amostra.");
    }

    return buffer.back();
}

void Sensor::addAmostra(double amostra) {
    if (buffer.size() >= tamanhoBuffer) {
        buffer.erase(buffer.begin());
    }

    buffer.push_back(amostra);
}

string Sensor::protocoloToString(ProtocoloSerial protocolo) {
    switch (protocolo) {
        case ProtocoloSerial::UART:
            return "UART";

        case ProtocoloSerial::I2C:
            return "I2C";

        case ProtocoloSerial::SPI:
            return "SPI";

        case ProtocoloSerial::Unknown:
        default:
            return "Unknown";
    }
}

string Sensor::tipoToString(TipoSensor tipo) {
    switch (tipo) {
        case TipoSensor::Virtual:
            return "Virtual";

        case TipoSensor::Real:
            return "Real";

        default:
            return "Unknown";
    }
}

ProtocoloSerial Sensor::stringToProtocolo(string texto) {
    transform(texto.begin(), texto.end(), texto.begin(),
        [](unsigned char c) {
            return static_cast<char>(toupper(c));
        }
    );

    if (texto == "UART") {
        return ProtocoloSerial::UART;
    }

    if (texto == "I2C") {
        return ProtocoloSerial::I2C;
    }

    if (texto == "SPI") {
        return ProtocoloSerial::SPI;
    }

    return ProtocoloSerial::Unknown;
}

TipoSensor Sensor::stringToTipo(string texto) {
    transform(texto.begin(), texto.end(), texto.begin(), [](unsigned char c) {
                return static_cast<char>(toupper(c));
                } 
            );

    if (texto == "VIRTUAL") {
        return TipoSensor::Virtual;
    }

    if (texto == "REAL") {
        return TipoSensor::Real;
    }

    throw invalid_argument("Tipo de sensor invalido.");
}
#include "../Include/sensor.h"

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

TipoSensor Sensor::getTipoSensor() const {
    return tipo;
}

const vector<double>& Sensor::getBuffer() const {
    return buffer;
}

void Sensor::addAmostra(double amostra) {
    if (buffer.size() >= tamanhoBuffer) {
        buffer.erase(buffer.begin());
    }

    buffer.push_back(amostra);
}

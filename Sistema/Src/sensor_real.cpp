#include "sensor_real.h"

#include <stdexcept>

SensorReal::SensorReal(unsigned endereco, unsigned tamanhoBuffer, string nome, float tensaoDeOperacao) : Sensor(endereco, tamanhoBuffer, nome, tensaoDeOperacao, ProtocoloSerial::UART, TipoSensor::Real) {
    portaConfigurada = "";
    baudRateConfigurado = 0;
    configurado = false;
}

SensorReal::~SensorReal() {
    portaSerial.fechar();
}

void SensorReal::configurar(string portaSerialTexto, int baudRate) {
    if (configurado && portaSerial.estaAberta() && portaConfigurada == portaSerialTexto && baudRateConfigurado == baudRate) {
        return;
    }

    portaSerial.fechar();

    if (!portaSerial.abrir(portaSerialTexto, baudRate)) {
        throw runtime_error("Nao foi possivel abrir a porta serial: " + portaSerialTexto);
    }

    portaConfigurada = portaSerialTexto;
    baudRateConfigurado = baudRate;
    configurado = true;
}

void SensorReal::comecarAquisicao(unsigned quantidade) {
    lerAmostras(quantidade);
}

vector<double> SensorReal::lerAmostras(unsigned quantidade) {
    if (!configurado || !portaSerial.estaAberta()) {
        throw runtime_error("Sensor real ainda nao foi configurado.");
    }

    unsigned amostrasLidas = 0;
    unsigned falhasConsecutivas = 0;
    const unsigned MAX_FALHAS_CONSECUTIVAS = 50;

    while (amostrasLidas < quantidade && falhasConsecutivas < MAX_FALHAS_CONSECUTIVAS) {
        string linha = portaSerial.lerLinha();

        if (linha.empty()) {
            falhasConsecutivas++;
            continue;
        }

        if (linhaValida(linha)) {
            double valor = parseLinha(linha);
            addAmostra(valor);
            amostrasLidas++;
            falhasConsecutivas = 0;
        } else {
            falhasConsecutivas++;
        }
    }

    if (amostrasLidas == 0) {
        throw runtime_error("Nenhuma amostra valida foi recebida pela porta serial.");
    }

    return getBuffer();
}

bool SensorReal::linhaValida(const string& linha) const {
    return linha.find("HSENSE:") == 0;
}

double SensorReal::parseLinha(const string& linha) const {
    string valorTexto = linha.substr(7);
    return stod(valorTexto);
}


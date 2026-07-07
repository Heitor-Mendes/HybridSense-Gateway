#include "../Include/sensor_virtual.h"

#include <cmath>
#include <stdexcept>

SensorVirtual::SensorVirtual(unsigned endereco, unsigned tamanhoBuffer, string nome, float tensaoDeOperacao, ProtocoloSerial protocolo) : Sensor(endereco, tamanhoBuffer, nome, tensaoDeOperacao, protocolo, TipoSensor::Virtual) {
    tempo = 0.0;
    gerador = mt19937(random_device{}());
}

SensorVirtual::~SensorVirtual() {
}

void SensorVirtual::comecarAquisicao(unsigned quantidade) {
    if(quantidade == 0) {
        quantidade = AMOSTRAS_PADRAO_SIMULACAO;
    }
    simularAmostras(quantidade);
}

void SensorVirtual::simularAmostras(unsigned quantidade) {
    if (quantidade == 0) {
        throw invalid_argument("Quantidade de amostras deve ser maior que zero.");
    }

    for (unsigned indice = 0; indice < quantidade; indice++) {
        addAmostra(gerarAmostra());
    }
}

ConfiguracaoSimulacao SensorVirtual::getConfiguracao() const {
    switch (protocolo) {
        case ProtocoloSerial::UART: return {0.50, 0.35, 0.03, 0.06, 1.00, 1023.0, false};
        case ProtocoloSerial::I2C: return {0.50, 0.25, 0.02, 0.02, 0.50, 4095.0, true};
        case ProtocoloSerial::SPI: return {0.50, 0.40, 0.08, 0.01, 0.25, 65535.0, true};
        default: throw runtime_error("Protocolo desconhecido. Nao e possivel obter configuracao de simulacao.");
    }
}

double SensorVirtual::gerarAmostra() {
    ConfiguracaoSimulacao config = getConfiguracao();
    double sinal = gerarSinalAnalogico(config);

    if (config.quantizar) {
        sinal = quantizarSinal(sinal, config);
    }

    tempo += config.passoTempo;
    return limitarValor(sinal, 0.0, tensaoDeOperacao);
}

double SensorVirtual::gerarSinalAnalogico(const ConfiguracaoSimulacao& config) {
    double tensaoMaxima = tensaoDeOperacao;
    normal_distribution<double> ruido(0.0, tensaoMaxima * config.desvioRuido);
    double sinal = tensaoMaxima * config.offset + tensaoMaxima * config.amplitude * sin(2.0 * PI * config.frequencia * tempo) + ruido(gerador);
    return limitarValor(sinal, 0.0, tensaoMaxima);
}

double SensorVirtual::quantizarSinal(double sinal, const ConfiguracaoSimulacao& config) {
    double tensaoMaxima = tensaoDeOperacao;
    double valorDigital = round((sinal / tensaoMaxima) * config.resolucao);
    double valorConvertido = (valorDigital / config.resolucao) * tensaoMaxima;
    return limitarValor(valorConvertido, 0.0, tensaoMaxima);
}

double SensorVirtual::limitarValor(double valor, double minimo, double maximo) {
    if (valor < minimo) {
        return minimo;
    }

    if (valor > maximo) {
        return maximo;
    }

    return valor;
}


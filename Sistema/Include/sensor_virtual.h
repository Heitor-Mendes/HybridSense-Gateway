#ifndef SENSORVIRTUAL_H
#define SENSORVIRTUAL_H

#include "sensor.h"
#include <random>
#include <string>

using namespace std;

struct ConfiguracaoSimulacao {
    double offset;
    double amplitude;
    double frequencia;
    double desvioRuido;
    double passoTempo;
    double resolucao;
    bool quantizar;
};

class SensorVirtual : public Sensor {
    public:
        SensorVirtual(unsigned endereco, unsigned tamanhoBuffer, string nome, float tensaoDeOperacao, ProtocoloSerial protocolo);
        virtual ~SensorVirtual();

        virtual void comecarAquisicao(unsigned quantidade);

    private:
        double tempo;
        mt19937 gerador;

        static constexpr double PI = 3.14159265358979323846;

        ConfiguracaoSimulacao getConfiguracao() const;

        void simularAmostras(unsigned quantidade);
        double gerarAmostra();
        double gerarSinalAnalogico(const ConfiguracaoSimulacao& config);
        double quantizarSinal(double sinal, const ConfiguracaoSimulacao& config);
        double limitarValor(double valor, double minimo, double maximo);
};

#endif

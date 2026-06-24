#ifndef SENSOR_MANAGER_H
#define SENSOR_MANAGER_H

#include "sensor.h"
#include "sensor_virtual.h"
#include "processamento_de_sinais.h"

#include <vector>
#include <string>

using namespace std;

struct DadosSensor {
    unsigned endereco;
    string nome;
    float tensaoDeOperacao;
    string protocolo;
    string tipo;
    unsigned quantidadeAmostras;
};

struct Resultado {
    double media;
    double minimo;
    double maximo;
    double desvioPadrao;
    double razaoSinalRuido;
    vector<double> sinalOriginal;
    vector<double> mediaMovel;
    vector<double> kalman;
};

class SensorManager {
    public:
        SensorManager();
        ~SensorManager();

        unsigned adicionarSensorVirtual(string nome, float tensaoDeOperacao, ProtocoloSerial protocolo, unsigned tamanhoBuffer);
        bool removerSensor(unsigned endereco);

        vector<DadosSensor> listarSensores() const;
        vector<DadosSensor> listarSensoresVirtuais() const;

        vector<double> simularSensorVirtual(unsigned endereco);
        vector<double> getBufferSensor(unsigned endereco) const;

        Resultado processarSinais(unsigned endereco);

        void limparTodos();
        unsigned getQuantidadeSensores() const;

    private:
        vector<Sensor*> sensores;
        unsigned proximoEndereco;

        static const unsigned AMOSTRAS_PADRAO_SIMULACAO = 100;
        static const unsigned JANELA_PADRAO_MEDIA_MOVEL = 5;

        Sensor* buscarSensor(unsigned endereco) const;
        DadosSensor montarDadosSensor(const Sensor* sensor) const;
};

#endif
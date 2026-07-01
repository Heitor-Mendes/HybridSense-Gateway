#ifndef SENSOR_MANAGER_H
#define SENSOR_MANAGER_H

#include "sensor.h"
#include "sensor_virtual.h"
#include "sensor_real.h"
#include "processamento_de_sinais.h"

#include <vector>
#include <string>

using namespace std;

struct DadosSensor {
    unsigned endereco;
    string nome;
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

        vector<DadosSensor> listarSensoresVirtuais() const;

        vector<double> simularSensorVirtual(unsigned endereco);
        vector<double> getBufferSensor(unsigned endereco) const;

        Resultado processarSinais(unsigned endereco);

        vector<double> lerSensorReal(string portaSerial, int baudRate, unsigned tamanhoBuffer);
        Resultado processarSinaisSensorReal();

        void limparTodos();

    private:
        vector<Sensor*> sensores;
        SensorReal* sensorReal;

        unsigned proximoEndereco;

        string portaSerialRealAtual;
        int baudRateRealAtual;
        unsigned tamanhoBufferRealAtual;

        Sensor* buscarSensor(unsigned endereco) const;
        DadosSensor montarDadosSensor(const Sensor* sensor) const;
};

#endif
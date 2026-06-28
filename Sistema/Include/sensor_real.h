#ifndef SENSOR_REAL_H
#define SENSOR_REAL_H

#include "sensor.h"
#include "porta_serial.h"

#include <string>
#include <vector>

using namespace std;

class SensorReal : public Sensor {
    public:
        SensorReal(unsigned endereco, unsigned tamanhoBuffer, string nome, float tensaoDeOperacao);
        virtual ~SensorReal();

        void comecarAquisicao() override;
        string getDescricao() const override;

        void configurar(string portaSerial, int baudRate);
        vector<double> lerAmostras(unsigned quantidade);

    private:
        PortaSerial portaSerial;
        string portaConfigurada;
        int baudRateConfigurado;
        bool configurado;

        bool linhaValida(const string& linha) const;
        double parseLinha(const string& linha) const;
};

#endif
#ifndef SENSOR_H
#define SENSOR_H

#include <string>
#include <vector>

using namespace std;

enum class TipoSensor{
    Virtual,
    Real
};

enum class ProtocoloSerial {
    UART,
    I2C,
    SPI,
    Unknown
};

class Sensor{
    public:

        //Construtor e Destrutor
        Sensor(unsigned, unsigned, string, float, ProtocoloSerial, TipoSensor);
        virtual ~Sensor();

        // Getters
        unsigned              getEndereco()           const;
        string                getNome()               const;
        TipoSensor            getTipoSensor()         const;
        const vector<double>& getBuffer()             const;

        // Metodos
        void         addAmostra(double);
        virtual void comecarAquisicao(unsigned) = 0;

    protected:
        unsigned        endereco;
        string          nome;
        float           tensaoDeOperacao;
        ProtocoloSerial protocolo;
        TipoSensor      tipo;
        unsigned        tamanhoBuffer;
        vector<double>  buffer;

    private:
};


#endif
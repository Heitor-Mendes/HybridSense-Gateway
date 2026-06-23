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
        float                 getTensaoDeOperacao()   const;
        ProtocoloSerial       getProtocolo()          const;
        TipoSensor            getTipoSensor()         const;
        const vector<double>& getBuffer()             const;
        double                getUltimaAmostra()      const;
        virtual string        getDescricao()          const = 0;

        // Metodos
        void         addAmostra(double);
        virtual void comecarAquisicao() = 0;

        //Utilidades
        static string          protocoloToString(ProtocoloSerial);
        static string          tipoToString(TipoSensor);
        static ProtocoloSerial stringToProtocolo(string);
        static TipoSensor      stringToTipo(string);
        


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
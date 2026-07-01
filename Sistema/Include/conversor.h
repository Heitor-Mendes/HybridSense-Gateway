#ifndef CONVERSOR_H
#define CONVERSOR_H

#include "sensor_manager.h"

#include <string>
#include <vector>

using namespace std;

class TratadorDeRequisicoes {
    public:
        TratadorDeRequisicoes(SensorManager& sensorManager);
        string processar(const string& requisicaoJson);

    private:
        SensorManager& sensorManager;

        string extrairString(const string& json, const string& chave) const;
        double extrairDouble(const string& json, const string& chave) const;
        unsigned extrairUnsigned(const string& json, const string& chave) const;

        ProtocoloSerial converterProtocolo(const string& protocolo) const;

        string escaparJson(const string& texto) const;
        string vetorParaJson(const vector<double>& vetor) const;

        string respostaErro(const string& mensagem) const;
        string respostaSimples(bool sucesso, const string& mensagem) const;

        string tratarListarSensoresVirtuais();
        string tratarAdicionarSensorVirtual(const string& json);
        string tratarRemoverSensorVirtual(const string& json);
        string tratarSimularSensorVirtual(const string& json);
        string tratarProcessarSinaisSensorVirtual(const string& json);

        string tratarLerDadosSensorReal(const string& json);
        string tratarProcessarSinaisSensorReal(const string& json);
};

#endif

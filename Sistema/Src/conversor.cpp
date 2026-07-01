#include "../Include/conversor.h"

#include <stdexcept>
#include <sstream>
#include <algorithm>
#include <cctype>

TratadorDeRequisicoes::TratadorDeRequisicoes(SensorManager& sensorManager) : sensorManager(sensorManager) {
}

string TratadorDeRequisicoes::processar(const string& requisicaoJson) {
    try {
        string comando = extrairString(requisicaoJson, "comando");

        if (comando == "listar_sensores_virtuais") {
            return tratarListarSensoresVirtuais();
        }

        if (comando == "adicionar_sensor_virtual") {
            return tratarAdicionarSensorVirtual(requisicaoJson);
        }

        if (comando == "remover_sensor_virtual") {
            return tratarRemoverSensorVirtual(requisicaoJson);
        }

        if (comando == "simular_sensor_virtual") {
            return tratarSimularSensorVirtual(requisicaoJson);
        }

        if (comando == "processar_sinais_sensor_virtual") {
            return tratarProcessarSinaisSensorVirtual(requisicaoJson);
        }

        if (comando == "ler_dados_sensor_real") {
            return tratarLerDadosSensorReal(requisicaoJson);
        }

        if (comando == "processar_sinais_sensor_real") {
            return tratarProcessarSinaisSensorReal(requisicaoJson);
        }

        return respostaErro("Comando desconhecido.");
    } catch (const exception& erro) {
        return respostaErro(erro.what());
    }
}

string TratadorDeRequisicoes::tratarListarSensoresVirtuais() {
    vector<DadosSensor> sensores = sensorManager.listarSensoresVirtuais();
    string json = "{\"sucesso\":true,\"mensagem\":\"Lista de sensores virtuais carregada.\",\"sensores\":[";

    for (unsigned indice = 0; indice < sensores.size(); indice++) {
        json += "{";
        json += "\"endereco\":" + to_string(sensores[indice].endereco) + ",";
        json += "\"nome\":\"" + escaparJson(sensores[indice].nome) + "\"";
        json += "}";

        if (indice + 1 < sensores.size()) {
            json += ",";
        }
    }

    json += "]}";
    return json;
}

string TratadorDeRequisicoes::tratarAdicionarSensorVirtual(const string& json) {
    string nome = extrairString(json, "nome");
    float tensao = static_cast<float>(extrairDouble(json, "tensao"));
    string protocoloTexto = extrairString(json, "protocolo");
    unsigned tamanhoBuffer = extrairUnsigned(json, "tamanhoBuffer");

    ProtocoloSerial protocolo = converterProtocolo(protocoloTexto);
    unsigned endereco = sensorManager.adicionarSensorVirtual(nome, tensao, protocolo, tamanhoBuffer);

    return "{\"sucesso\":true,\"mensagem\":\"Sensor virtual adicionado com sucesso.\",\"endereco\":" + to_string(endereco) + "}";
}

string TratadorDeRequisicoes::tratarRemoverSensorVirtual(const string& json) {
    unsigned endereco = extrairUnsigned(json, "endereco");
    bool removido = sensorManager.removerSensor(endereco);

    if (!removido) {
        return respostaErro("Sensor nao encontrado para remocao.");
    }

    return respostaSimples(true, "Sensor virtual removido com sucesso.");
}

string TratadorDeRequisicoes::tratarSimularSensorVirtual(const string& json) {
    unsigned endereco = extrairUnsigned(json, "endereco");
    vector<double> sinal = sensorManager.simularSensorVirtual(endereco);

    string resposta = "{\"sucesso\":true,\"mensagem\":\"Simulacao realizada com sucesso.\",";
    resposta += "\"endereco\":" + to_string(endereco) + ",";
    resposta += "\"sinal\":" + vetorParaJson(sinal);
    resposta += "}";

    return resposta;
}

string TratadorDeRequisicoes::tratarProcessarSinaisSensorVirtual(const string& json) {
    unsigned endereco = extrairUnsigned(json, "endereco");
    Resultado resultado = sensorManager.processarSinais(endereco);

    string resposta = "{\"sucesso\":true,\"mensagem\":\"Processamento realizado com sucesso.\",";

    resposta += "\"metricas\":{";
    resposta += "\"media\":" + to_string(resultado.media) + ",";
    resposta += "\"minimo\":" + to_string(resultado.minimo) + ",";
    resposta += "\"maximo\":" + to_string(resultado.maximo) + ",";
    resposta += "\"desvioPadrao\":" + to_string(resultado.desvioPadrao) + ",";
    resposta += "\"razaoSinalRuido\":" + to_string(resultado.razaoSinalRuido);
    resposta += "},";

    resposta += "\"sinais\":{";
    resposta += "\"sinalOriginal\":" + vetorParaJson(resultado.sinalOriginal) + ",";
    resposta += "\"mediaMovel\":" + vetorParaJson(resultado.mediaMovel) + ",";
    resposta += "\"kalman\":" + vetorParaJson(resultado.kalman);
    resposta += "}";

    resposta += "}";

    return resposta;
}

string TratadorDeRequisicoes::tratarLerDadosSensorReal(const string& json) {
    string portaSerial = extrairString(json, "portaSerial");
    int baudRate = static_cast<int>(extrairUnsigned(json, "baudRate"));
    unsigned tamanhoBuffer = extrairUnsigned(json, "tamanhoBuffer");

    vector<double> sinal = sensorManager.lerSensorReal(portaSerial, baudRate, tamanhoBuffer);

    string resposta = "{\"sucesso\":true,\"mensagem\":\"Leitura do sensor real realizada com sucesso.\",";
    resposta += "\"portaSerial\":\"" + escaparJson(portaSerial) + "\",";
    resposta += "\"baudRate\":" + to_string(baudRate) + ",";
    resposta += "\"tamanhoBuffer\":" + to_string(tamanhoBuffer) + ",";
    resposta += "\"sinal\":" + vetorParaJson(sinal);
    resposta += "}";

    return resposta;
}

string TratadorDeRequisicoes::tratarProcessarSinaisSensorReal(const string& json) {
    string portaSerial = extrairString(json, "portaSerial");
    int baudRate = static_cast<int>(extrairUnsigned(json, "baudRate"));
    unsigned tamanhoBuffer = extrairUnsigned(json, "tamanhoBuffer");

    sensorManager.lerSensorReal(portaSerial, baudRate, tamanhoBuffer);
    Resultado resultado = sensorManager.processarSinaisSensorReal();

    string resposta = "{\"sucesso\":true,\"mensagem\":\"Processamento do sensor real realizado com sucesso.\",";

    resposta += "\"metricas\":{";
    resposta += "\"media\":" + to_string(resultado.media) + ",";
    resposta += "\"minimo\":" + to_string(resultado.minimo) + ",";
    resposta += "\"maximo\":" + to_string(resultado.maximo) + ",";
    resposta += "\"desvioPadrao\":" + to_string(resultado.desvioPadrao) + ",";
    resposta += "\"razaoSinalRuido\":" + to_string(resultado.razaoSinalRuido);
    resposta += "},";

    resposta += "\"sinais\":{";
    resposta += "\"sinalOriginal\":" + vetorParaJson(resultado.sinalOriginal) + ",";
    resposta += "\"mediaMovel\":" + vetorParaJson(resultado.mediaMovel) + ",";
    resposta += "\"kalman\":" + vetorParaJson(resultado.kalman);
    resposta += "}";

    resposta += "}";

    return resposta;
}

string TratadorDeRequisicoes::extrairString(const string& json, const string& chave) const {
    const unsigned npos = static_cast<unsigned>(string::npos);
    string alvo = "\"" + chave + "\"";
    unsigned posChave = static_cast<unsigned>(json.find(alvo));

    if (posChave == npos) {
        throw invalid_argument("Campo obrigatorio ausente: " + chave);
    }

    unsigned posDoisPontos = static_cast<unsigned>(json.find(":", posChave));

    if (posDoisPontos == npos) {
        throw invalid_argument("Formato invalido para campo: " + chave);
    }

    unsigned inicio = static_cast<unsigned>(json.find("\"", posDoisPontos + 1));

    if (inicio == npos) {
        throw invalid_argument("Campo string invalido: " + chave);
    }

    inicio++;
    string valor;

    for (unsigned indice = inicio; indice < json.size(); indice++) {
        if (json[indice] == '\\' && indice + 1 < json.size()) {
            valor += json[indice + 1];
            indice++;
            continue;
        }

        if (json[indice] == '"') {
            return valor;
        }

        valor += json[indice];
    }

    throw invalid_argument("Campo string nao finalizado: " + chave);
}

double TratadorDeRequisicoes::extrairDouble(const string& json, const string& chave) const {
    const unsigned npos = static_cast<unsigned>(string::npos);
    string alvo = "\"" + chave + "\"";
    unsigned posChave = static_cast<unsigned>(json.find(alvo));

    if (posChave == npos) {
        throw invalid_argument("Campo obrigatorio ausente: " + chave);
    }

    unsigned posDoisPontos = static_cast<unsigned>(json.find(":", posChave));

    if (posDoisPontos == npos) {
        throw invalid_argument("Formato invalido para campo: " + chave);
    }

    unsigned inicio = posDoisPontos + 1;

    while (inicio < json.size() && isspace(static_cast<unsigned char>(json[inicio]))) {
        inicio++;
    }

    unsigned fim = inicio;

    while (fim < json.size() && json[fim] != ',' && json[fim] != '}') {
        fim++;
    }

    string valor = json.substr(inicio, fim - inicio);
    return stod(valor);
}

unsigned TratadorDeRequisicoes::extrairUnsigned(const string& json, const string& chave) const {
    const unsigned npos = static_cast<unsigned>(string::npos);
    string alvo = "\"" + chave + "\"";
    unsigned posChave = static_cast<unsigned>(json.find(alvo));

    if (posChave == npos) {
        throw invalid_argument("Campo obrigatorio ausente: " + chave);
    }

    unsigned posDoisPontos = static_cast<unsigned>(json.find(":", posChave));

    if (posDoisPontos == npos) {
        throw invalid_argument("Formato invalido para campo: " + chave);
    }

    unsigned inicio = posDoisPontos + 1;

    while (inicio < json.size() && isspace(static_cast<unsigned char>(json[inicio]))) {
        inicio++;
    }

    unsigned fim = inicio;

    while (fim < json.size() && json[fim] != ',' && json[fim] != '}') {
        fim++;
    }

    string valor = json.substr(inicio, fim - inicio);
    return static_cast<unsigned>(stoul(valor));
}

ProtocoloSerial TratadorDeRequisicoes::converterProtocolo(const string& protocolo) const {
    string texto = protocolo;   
    
    transform(texto.begin(), texto.end(), texto.begin(), [](unsigned char c) {
        return static_cast<char>(toupper(c));
    });

    if (texto == "UART") {
        return ProtocoloSerial::UART;
    }

    if (texto == "I2C") {
        return ProtocoloSerial::I2C;
    }

    if (texto == "SPI") {
        return ProtocoloSerial::SPI;
    }

    return ProtocoloSerial::Unknown;
}

string TratadorDeRequisicoes::escaparJson(const string& texto) const {
    string resultado;

    for (char c : texto) {
        if (c == '"') {
            resultado += "\\\"";
        } else if (c == '\\') {
            resultado += "\\\\";
        } else if (c == '\n') {
            resultado += "\\n";
        } else if (c == '\r') {
            resultado += "\\r";
        } else {
            resultado += c;
        }
    }

    return resultado;
}

string TratadorDeRequisicoes::vetorParaJson(const vector<double>& vetor) const {
    string json = "[";

    for (unsigned indice = 0; indice < vetor.size(); indice++) {
        json += to_string(vetor[indice]);

        if (indice + 1 < vetor.size()) {
            json += ",";
        }
    }

    json += "]";
    return json;
}

string TratadorDeRequisicoes::respostaErro(const string& mensagem) const {
    return "{\"sucesso\":false,\"mensagem\":\"" + escaparJson(mensagem) + "\"}";
}

string TratadorDeRequisicoes::respostaSimples(bool sucesso, const string& mensagem) const {
    string valorSucesso = sucesso ? "true" : "false";
    return "{\"sucesso\":" + valorSucesso + ",\"mensagem\":\"" + escaparJson(mensagem) + "\"}";
}

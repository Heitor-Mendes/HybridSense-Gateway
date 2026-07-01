#include "../Include/sensor_manager.h"

#include <stdexcept>

SensorManager::SensorManager() {
    proximoEndereco = 0x001;
    sensorReal = nullptr;
    portaSerialRealAtual = "";
    baudRateRealAtual = 0;
    tamanhoBufferRealAtual = 0;
}

SensorManager::~SensorManager() {
    limparTodos();
}

unsigned SensorManager::adicionarSensorVirtual(string nome, float tensaoDeOperacao, ProtocoloSerial protocolo, unsigned tamanhoBuffer) {
    unsigned endereco = proximoEndereco;
    Sensor* sensor = new SensorVirtual(endereco, tamanhoBuffer, nome, tensaoDeOperacao, protocolo);

    sensores.push_back(sensor);
    proximoEndereco++;

    return endereco;
}

bool SensorManager::removerSensor(unsigned endereco) {
    for (unsigned indice = 0; indice < sensores.size(); indice++) {
        if (sensores[indice]->getEndereco() == endereco) {
            delete sensores[indice];
            sensores.erase(sensores.begin() + indice);
            return true;
        }
    }

    return false;
}

Sensor* SensorManager::buscarSensor(unsigned endereco) const {
    for (Sensor* sensor : sensores) {
        if (sensor->getEndereco() == endereco) {
            return sensor;
        }
    }

    return nullptr;
}

DadosSensor SensorManager::montarDadosSensor(const Sensor* sensor) const {
    DadosSensor dados;

    dados.endereco = sensor->getEndereco();
    dados.nome = sensor->getNome();

    return dados;
}

vector<DadosSensor> SensorManager::listarSensoresVirtuais() const {
    vector<DadosSensor> lista;

    for (Sensor* sensor : sensores) {
        if (sensor->getTipoSensor() == TipoSensor::Virtual) {
            lista.push_back(montarDadosSensor(sensor));
        }
    }

    return lista;
}

vector<double> SensorManager::simularSensorVirtual(unsigned endereco) {
    Sensor* sensor = buscarSensor(endereco);

    if (sensor == nullptr) {
        throw runtime_error("Sensor nao encontrado.");
    }

    if (sensor->getTipoSensor() != TipoSensor::Virtual) {
        throw runtime_error("O sensor informado nao e virtual.");
    }

    sensor->comecarAquisicao(0); // 0 indica que o sensor virtual deve usar a quantidade padrao de amostras

    return sensor->getBuffer();
}

vector<double> SensorManager::getBufferSensor(unsigned endereco) const {
    Sensor* sensor = buscarSensor(endereco);

    if (sensor == nullptr) {
        throw runtime_error("Sensor nao encontrado.");
    }

    return sensor->getBuffer();
}

Resultado SensorManager::processarSinais(unsigned endereco) {
    vector<double> dados = getBufferSensor(endereco);

    if (dados.empty()) {
        throw runtime_error("O sensor selecionado nao possui amostras no buffer.");
    }

    ProcessadorDeSinais processador;
    Resultado resultado;

    resultado.media = processador.media(dados);
    resultado.minimo = processador.minimo(dados);
    resultado.maximo = processador.maximo(dados);
    resultado.desvioPadrao = processador.desvioPadrao(dados);
    resultado.razaoSinalRuido = processador.razaoSinalRuido(dados);
    resultado.sinalOriginal = dados;
    resultado.mediaMovel = processador.mediaMovel(dados, 0);
    resultado.kalman = processador.filtroDeKalman(dados);

    return resultado;
}

vector<double> SensorManager::lerSensorReal(string portaSerial, int baudRate, unsigned tamanhoBuffer) {
    if (portaSerial.empty()) {
        throw invalid_argument("Porta serial nao pode ser vazia.");
    }

    if (baudRate <= 0) {
        throw invalid_argument("Baud rate deve ser maior que zero.");
    }

    if (tamanhoBuffer == 0) {
        throw invalid_argument("Tamanho do buffer do sensor real deve ser maior que zero.");
    }

    bool precisaRecriar = false;

    if (sensorReal == nullptr) {
        precisaRecriar = true;
    }

    if (portaSerialRealAtual != portaSerial || baudRateRealAtual != baudRate || tamanhoBufferRealAtual != tamanhoBuffer) {
        precisaRecriar = true;
    }

    if (precisaRecriar) {
        if (sensorReal != nullptr) {
            delete sensorReal;
            sensorReal = nullptr;
        }

        sensorReal = new SensorReal(0xFFF, tamanhoBuffer, "Sensor Real ESP32", 3.3f);
        portaSerialRealAtual = portaSerial;
        baudRateRealAtual = baudRate;
        tamanhoBufferRealAtual = tamanhoBuffer;
    }

    sensorReal->configurar(portaSerial, baudRate);
    sensorReal->comecarAquisicao(tamanhoBuffer);

    return sensorReal->getBuffer();
}

Resultado SensorManager::processarSinaisSensorReal() {
    if (sensorReal == nullptr) {
        throw runtime_error("Sensor real ainda nao foi configurado.");
    }

    vector<double> dados = sensorReal->getBuffer();

    if (dados.empty()) {
        throw runtime_error("O sensor real ainda nao possui amostras no buffer.");
    }

    ProcessadorDeSinais processador;
    Resultado resultado;

    resultado.media = processador.media(dados);
    resultado.minimo = processador.minimo(dados);
    resultado.maximo = processador.maximo(dados);
    resultado.desvioPadrao = processador.desvioPadrao(dados);
    resultado.razaoSinalRuido = processador.razaoSinalRuido(dados);
    resultado.sinalOriginal = dados;
    resultado.mediaMovel = processador.mediaMovel(dados, 0);
    resultado.kalman = processador.filtroDeKalman(dados);

    return resultado;
}

void SensorManager::limparTodos() {
    for (Sensor* sensor : sensores) {
        delete sensor;
    }

    sensores.clear();

    if (sensorReal != nullptr) {
        delete sensorReal;
        sensorReal = nullptr;
    }

    proximoEndereco = 0x001;
    portaSerialRealAtual = "";
    baudRateRealAtual = 0;
    tamanhoBufferRealAtual = 0;
}


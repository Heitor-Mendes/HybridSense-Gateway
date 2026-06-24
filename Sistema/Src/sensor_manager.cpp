#include "../Include/sensor_manager.h"

#include <stdexcept>

SensorManager::SensorManager() {
    proximoEndereco = 0x001;
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
    dados.tensaoDeOperacao = sensor->getTensaoDeOperacao();
    dados.protocolo = sensor->protocoloToString(sensor->getProtocolo());
    dados.tipo = sensor->tipoToString(sensor->getTipoSensor());
    dados.quantidadeAmostras = sensor->getBuffer().size();

    return dados;
}

vector<DadosSensor> SensorManager::listarSensores() const {
    vector<DadosSensor> lista;

    for (Sensor* sensor : sensores) {
        lista.push_back(montarDadosSensor(sensor));
    }

    return lista;
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

    SensorVirtual* sensorVirtual = dynamic_cast<SensorVirtual*>(sensor);

    if (sensorVirtual == nullptr) {
        throw runtime_error("Falha ao converter Sensor para SensorVirtual.");
    }

    sensorVirtual->simularAmostras(AMOSTRAS_PADRAO_SIMULACAO);

    return sensorVirtual->getBuffer();
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
    resultado.mediaMovel = processador.mediaMovel(dados, JANELA_PADRAO_MEDIA_MOVEL);
    resultado.kalman = processador.filtroDeKalman(dados);

    return resultado;
}

void SensorManager::limparTodos() {
    for (Sensor* sensor : sensores) {
        delete sensor;
    }

    sensores.clear();
    proximoEndereco = 0x001;
}

unsigned SensorManager::getQuantidadeSensores() const {
    return sensores.size();
}
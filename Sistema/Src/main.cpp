#include <iostream>
#include <iomanip>
#include <memory>
#include <vector>
#include <limits>

#include "../Include/sensorVirtual.h"
#include "../Include/processamentoDeSinais.h"

using namespace std;

void limparEntrada() {
    cin.clear();
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
}

ProtocoloSerial escolherProtocolo() {
    int opcao;

    cout << "\nEscolha o protocolo:" << endl;
    cout << "1 -> UART" << endl;
    cout << "2 -> I2C" << endl;
    cout << "3 -> SPI" << endl;
    cout << "Opcao: ";
    cin >> opcao;

    switch (opcao) {
        case 1: return ProtocoloSerial::UART;
        case 2: return ProtocoloSerial::I2C;
        case 3: return ProtocoloSerial::SPI;
        default: return ProtocoloSerial::Unknown;
    }
}

void imprimirBuffer(const vector<double>& dados) {
    if (dados.empty()) {
        cout << "\nBuffer vazio." << endl;
        return;
    }

    cout << "\n===== DADOS DO BUFFER =====" << endl;

    for (unsigned i = 0; i < dados.size(); i++) {
        cout << "Amostra " << setw(3) << i + 1 << " -> " << fixed << setprecision(4) << dados[i] << " V" << endl;
    }
}

void imprimirVetor(const string& titulo, const vector<double>& dados) {
    cout << "\n===== " << titulo << " =====" << endl;

    for (unsigned i = 0; i < dados.size(); i++) {
        cout << "Amostra " << setw(3) << i + 1 << " -> " << fixed << setprecision(4) << dados[i] << " V" << endl;
    }
}

void menuSimulacao(unique_ptr<SensorVirtual>& sensorAtual) {
    unsigned endereco;
    unsigned tamanhoBuffer;
    unsigned quantidadeAmostras;
    string nome;
    float tensaoDeOperacao;

    limparEntrada();

    cout << "\n===== SIMULACAO DE SENSOR VIRTUAL =====" << endl;

    cout << "Endereco do sensor: ";
    cin >> endereco;

    limparEntrada();

    cout << "Nome do sensor: ";
    getline(cin, nome);

    cout << "Tensao de operacao em V: ";
    cin >> tensaoDeOperacao;

    cout << "Tamanho maximo do buffer: ";
    cin >> tamanhoBuffer;

    cout << "Quantidade de amostras para simular: ";
    cin >> quantidadeAmostras;

    ProtocoloSerial protocolo = escolherProtocolo();

    if (protocolo == ProtocoloSerial::Unknown) {
        cout << "\nProtocolo invalido. Simulacao cancelada." << endl;
        return;
    }

    sensorAtual = make_unique<SensorVirtual>(endereco, tamanhoBuffer, nome, tensaoDeOperacao, protocolo);
    sensorAtual->simularAmostras(quantidadeAmostras);

    cout << "\nSensor criado e simulado com sucesso." << endl;
    cout << sensorAtual->getDescricao() << endl;

    imprimirBuffer(sensorAtual->getBuffer());
}

void menuAnalise(const unique_ptr<SensorVirtual>& sensorAtual) {
    if (!sensorAtual) {
        cout << "\nNenhum sensor foi simulado ainda. Use a opcao 1 primeiro." << endl;
        return;
    }

    const vector<double>& dados = sensorAtual->getBuffer();

    if (dados.empty()) {
        cout << "\nO sensor existe, mas o buffer esta vazio." << endl;
        return;
    }

    ProcessadorDeSinais processador;

    cout << "\n===== ANALISE DE SINAIS =====" << endl;
    cout << sensorAtual->getDescricao() << endl;

    cout << "\n===== METRICAS =====" << endl;
    cout << "Media: " << fixed << setprecision(4) << processador.media(dados) << " V" << endl;
    cout << "Minimo: " << fixed << setprecision(4) << processador.minimo(dados) << " V" << endl;
    cout << "Maximo: " << fixed << setprecision(4) << processador.maximo(dados) << " V" << endl;
    cout << "Desvio padrao: " << fixed << setprecision(4) << processador.desvioPadrao(dados) << " V" << endl;
    cout << "Razao sinal-ruido: " << fixed << setprecision(4) << processador.razaoSinalRuido(dados) << endl;
    cout << "Ultima amostra: " << fixed << setprecision(4) << sensorAtual->getUltimaAmostra() << " V" << endl;

    unsigned janela;

    cout << "\nJanela da media movel: ";
    cin >> janela;

    vector<double> dadosMediaMovel = processador.mediaMovel(dados, janela);
    vector<double> dadosKalman = processador.filtroDeKalman(dados);

    imprimirVetor("SINAL ORIGINAL", dados);
    imprimirVetor("MEDIA MOVEL", dadosMediaMovel);
    imprimirVetor("FILTRO DE KALMAN", dadosKalman);
}

int main() {
    unique_ptr<SensorVirtual> sensorAtual = nullptr;
    int opcao;

    cout << fixed << setprecision(4);

    do {
        cout << "\n==============================" << endl;
        cout << "      HYBRID SENSE GATEWAY     " << endl;
        cout << "==============================" << endl;
        cout << "1 -> Simulacao de sensor virtual" << endl;
        cout << "2 -> Analise de sinais" << endl;
        cout << "0 -> Sair" << endl;
        cout << "Opcao: ";
        cin >> opcao;

        try {
            switch (opcao) {
                case 1: menuSimulacao(sensorAtual); break;
                case 2: menuAnalise(sensorAtual); break;
                case 0: cout << "\nEncerrando programa..." << endl; break;
                default: cout << "\nOpcao invalida." << endl; break;
            }
        } catch (const exception& erro) {
            cout << "\nErro: " << erro.what() << endl;
        }

    } while (opcao != 0);

    return 0;
}
#include <iostream>
#include <vector>

#include "porta_serial.h"

using namespace std;

int main() {

    vector<string> portas = PortaSerial::listarPortasDisponiveis();

    if (portas.empty()) {
        cout << "Nenhuma porta serial encontrada." << endl;
        return 1;
    }

    cout << "===================================" << endl;
    cout << " Portas Seriais Encontradas" << endl;
    cout << "===================================" << endl;

    for (unsigned i = 0; i < portas.size(); i++) {
        cout << "[" << i << "] " << portas[i] << endl;
    }

    unsigned indicePorta;

    cout << endl;
    cout << "Selecione a porta: ";
    cin >> indicePorta;

    if (indicePorta >= portas.size()) {
        cout << "Indice invalido." << endl;
        return 1;
    }

    int baudRate;

    cout << "Informe o baud rate: ";
    cin >> baudRate;

    string portaSelecionada = portas[indicePorta];

    PortaSerial serial;

    cout << endl;
    cout << "Abrindo " << portaSelecionada << " @ " << baudRate << " baud..." << endl;

    if (!serial.abrir(portaSelecionada, baudRate)) {
        cout << "Falha ao abrir a porta." << endl;
        return 1;
    }

    cout << "Porta aberta com sucesso." << endl;
    cout << "Pressione CTRL+C para encerrar." << endl;
    cout << endl;

    while (true) {

        string linha = serial.lerLinha();

        if (!linha.empty()) {
            cout << linha << endl;
        }
    }

    return 0;
}
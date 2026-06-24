#include <iostream>

#include "../Include/socket.h"
#include "../Include/sensor_manager.h"
#include "../Include/conversor.h"

using namespace std;

int main() {
    try {
        SensorManager sensorManager;
        TratadorDeRequisicoes tratador(sensorManager);
        ServidorTCP servidor(8080);

        servidor.iniciar();

        while (true) {
            socket_t cliente = servidor.aceitarCliente();
            string requisicao = servidor.receberLinha(cliente);

            cout << "JSON recebido da API: " << requisicao << endl;

            string resposta = tratador.processar(requisicao);

            cout << "JSON enviado para API: " << resposta << endl;

            servidor.enviarLinha(cliente, resposta);
            servidor.fecharCliente(cliente);
        }
    } catch (const exception& erro) {
        cerr << "Erro no servidor C++: " << erro.what() << endl;
        return 1;
    }

    return 0;
}
#include "../Include/processamento_de_sinais.h"

#include <cmath>
#include <stdexcept>

ProcessadorDeSinais::ProcessadorDeSinais() {
    x = 0.0;
    p = 1.0;
    q = 0.01;
    r = 0.1;
    k = 0.0;

    kalmanInicializado = false;
}

ProcessadorDeSinais::ProcessadorDeSinais(double q_, double r_) {
    x = 0.0;
    p = 1.0;
    q = q_;
    r = r_;
    k = 0.0;
    kalmanInicializado = false;

    if (q < 0.0) {
        q = 0.01;
    }

    if (r <= 0.0) {
        r = 0.1;
    }
}

vector<double> ProcessadorDeSinais::mediaMovel(const vector<double>& dados, unsigned janela) const {
    
    if (dados.empty()) {
        throw invalid_argument("Nao e possivel calcular media movel com vetor vazio.");
    }

    if (janela == 0) {
        janela = JANELA_MEDIA_MOVEL_PADRAO;
    }

    vector<double> resultado;
    resultado.reserve(dados.size());

    for (unsigned indiceA = 0; indiceA < dados.size(); indiceA++) {
        double soma     = 0.0;
        unsigned inicio = 0;

        if (indiceA + 1 > janela) {
            inicio = indiceA + 1 - janela;
        }

        for (unsigned indiceB = inicio; indiceB <= indiceA; indiceB++) {
            soma += dados[indiceB];
        }

        resultado.push_back(soma / (indiceA - inicio + 1));
    }

    return resultado;
}

vector<double> ProcessadorDeSinais::filtroDeKalman(const vector<double>& dados) {
    
    if (dados.empty()) {
        throw invalid_argument("Nao eh possivel aplicar filtro de Kalman com vetor vazio.");
    }

    vector<double> resultado;
    resultado.reserve(dados.size());

    if (!kalmanInicializado) {
        x = dados[0];
        p = 1.0;
        kalmanInicializado = true;
    }

    for (unsigned indice = 0; indice < dados.size(); indice++) {
        p = p + q;
        k = p / (p + r);
        x = x + k * (dados[indice] - x);
        p = (1.0 - k) * p;
        resultado.push_back(x);
    }

    return resultado;
}

double ProcessadorDeSinais::media(const vector<double>& dados) const {
    if (dados.empty()) {
        throw invalid_argument("Nao e possivel calcular media com vetor vazio.");
    }

    double soma = 0.0;

    for (double valor : dados) {
        soma += valor;
    }

    return soma / dados.size();
}

double ProcessadorDeSinais::minimo(const vector<double>& dados) const {
    if (dados.empty()) {
        throw invalid_argument("Nao e possivel calcular minimo com vetor vazio.");
    }

    double menor = dados[0];

    for (double valor : dados) {
        if (valor < menor) {
            menor = valor;
        }
    }

    return menor;
}

double ProcessadorDeSinais::maximo(const vector<double>& dados) const {
    if (dados.empty()) {
        throw invalid_argument("Nao e possivel calcular maximo com vetor vazio.");
    }

    double maior = dados[0];

    for (double valor : dados) {
        if (valor > maior) {
            maior = valor;
        }
    }

    return maior;
}

double ProcessadorDeSinais::desvioPadrao(const vector<double>& dados) const {
    if (dados.empty()) {
        throw invalid_argument("Nao e possivel calcular desvio padrao com vetor vazio.");
    }

    double mediaResultado = media(dados);
    double soma           = 0.0;

    for (double valor : dados) {
        soma += pow(valor - mediaResultado, 2.0);
    }

    return sqrt(soma / dados.size());
}

double ProcessadorDeSinais::razaoSinalRuido(const vector<double>& dados) const {
    if (dados.empty()) {
        throw invalid_argument("Nao e possivel calcular razao sinal-ruido com vetor vazio.");
    }

    double mediaResultado = media(dados);
    double ruido = desvioPadrao(dados);

    if (ruido == 0.0) {
        return INFINITO;
    }

    return abs(mediaResultado) / ruido;
}

void ProcessadorDeSinais::configurarKalman(double q_, double r_) {
    if (q < 0.0) {
        q = 0.01;
    }

    if (r <= 0.0) {
        r = 0.1;
    }

    q = q_;
    r = r_;
}

void ProcessadorDeSinais::resetarKalman() {
    x = 0.0;
    p = 1.0;
    k = 0.0;
    kalmanInicializado = false;
}
#ifndef PROCESSAMENTO_DE_SINAIS_H
#define PROCESSAMENTO_DE_SINAIS_H

#include <vector>
#include <limits>
using namespace std;

const double INFINITO  = numeric_limits<double>::infinity();

class ProcessadorDeSinais {
    public:
        ProcessadorDeSinais();
        ProcessadorDeSinais(double q, double r);

        vector<double> mediaMovel(const vector<double>&, unsigned)  const;
        vector<double> filtroDeKalman(const vector<double>&);
        double         media (const vector<double>&)                const;
        double         minimo(const vector<double>&)                const;
        double         maximo(const vector<double>&)                const;
        double         desvioPadrao(const vector<double>&)          const;
        double         razaoSinalRuido(const vector<double>&)       const;

        void configurarKalman(double q, double r);
        void resetarKalman();

    private:
        double x; // Estado estimado
        double p; // Incerteza da estimativa
        double q; // Ruido do processo
        double r; // Ruido da medicao
        double k; // Ganho de Kalman

        bool kalmanInicializado;
        
        // Ponto de personalizacao futuramente
        static const unsigned JANELA_MEDIA_MOVEL_PADRAO = 5;
        static const unsigned AMOSTRAS_PADRAO_SIMULACAO = 100;
        
        
};

#endif
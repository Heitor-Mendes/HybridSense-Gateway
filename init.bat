@echo off
echo ===========================================
echo 1. Compilando o codigo C++...
echo ===========================================
mingw32-make

:: Verifica se o executavel foi gerado com sucesso antes de continuar
if not exist programa.exe (
    echo.
    echo [ERRO] O programa.exe nao foi gerado. Verifique os erros de compilacao acima.
    pause
    exit /b
)

echo.
echo ===========================================
echo 2. Iniciando o programa C++ (programa.exe)...
echo ===========================================
:: 'start' abre o seu programa C++ em uma janela separada
start "Programa C++" programa.exe

echo.
echo ===========================================
echo 3. Iniciando os servicos em Python...
echo ===========================================
:: Abre a API em outra janela
start "API Python" python API/main.py

:: Abre a Interface em outra janela
start "Interface Python" python Interface/windows2.py

echo.
echo ===========================================
echo Todos os processos foram iniciados!
echo ===========================================
pause
@echo off

echo ===========================================
echo Limpando arquivos gerados...
echo ===========================================

if exist obj (
    rmdir /s /q obj
    echo Pasta obj removida.
)

if exist programa.exe (
    del /q programa.exe
    echo programa.exe removido.
)

echo.
echo Limpeza concluida.
pause
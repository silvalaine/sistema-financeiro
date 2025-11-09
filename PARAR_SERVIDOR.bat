@echo off
echo ========================================
echo PARANDO SERVIDOR NA PORTA 5000
echo ========================================
echo.

echo Procurando processos na porta 5000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do (
    echo Encontrado processo PID: %%a
    echo Parando processo...
    taskkill /PID %%a /F
    echo Processo parado!
)

echo.
echo ========================================
echo Pronto! A porta 5000 esta livre agora.
echo ========================================
echo.
pause


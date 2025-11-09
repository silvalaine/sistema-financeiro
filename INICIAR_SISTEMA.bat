@echo off
chcp 65001 >nul
echo ========================================
echo SISTEMA FINANCEIRO - INICIAR SERVIDOR
echo ========================================
echo.

REM Verificar se a porta 5000 está em uso
echo Verificando porta 5000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING 2^>nul') do (
    echo [AVISO] Porta 5000 esta em uso pelo processo %%a
    echo Parando processo anterior...
    taskkill /PID %%a /F >nul 2>&1
    timeout /t 2 >nul
)

echo.
echo Iniciando servidor...
echo.
echo ========================================
echo SERVIDOR INICIADO!
echo ========================================
echo.
echo Acesse no navegador:
echo   http://localhost:5000
echo.
echo Mantenha esta janela aberta enquanto usar o sistema.
echo Pressione CTRL+C para parar o servidor.
echo.
echo ========================================
echo.

python app.py

pause


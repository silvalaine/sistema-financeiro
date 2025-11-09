@echo off
echo ========================================
echo INICIANDO SISTEMA FINANCEIRO
echo ========================================
echo.
echo Verificando dependencias...
python diagnostico.py
echo.
echo ========================================
echo Iniciando servidor...
echo ========================================
echo.
echo O servidor estara disponivel em:
echo http://localhost:5000
echo.
echo Pressione CTRL+C para parar o servidor
echo.
python app.py
pause


@echo off
echo ========================================
echo    Instalador - Pre-Vendas WhatsApp
echo ========================================
echo.
echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Baixe em: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python encontrado!
echo.
echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo ========================================
echo    Instalacao concluida!
echo ========================================
echo.
echo Para executar o app, rode: python app.py
echo Ou clique duas vezes em "executar.bat"
echo.
pause

@echo off
echo ========================================
echo   Criando executavel (.exe)
echo ========================================
echo.
echo Instalando PyInstaller...
pip install pyinstaller

echo.
echo Gerando executavel...
pyinstaller --onefile --windowed --name "PreVendas-WhatsApp" --icon=NONE app.py

echo.
echo ========================================
echo   Executavel criado com sucesso!
echo ========================================
echo.
echo O arquivo esta em: dist\PreVendas-WhatsApp.exe
echo.
pause

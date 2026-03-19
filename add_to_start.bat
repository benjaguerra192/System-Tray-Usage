@echo off

set RUTA=%~dp0
set DESTINO=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\start_monitor.bat

echo @echo off > "%DESTINO%"
echo cd /d "%RUTA%" >> "%DESTINO%"
echo pythonw monitor_systray.py >> "%DESTINO%"

echo.
echo Ready, It will start with windows.
pause

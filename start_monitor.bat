@echo off
echo Insalling dependencies
pip install pystray psutil pillow --quiet
echo.
echo Installing...
pythonw systray_monitor.py

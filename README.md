# Taskbar Tray Usage

A lightweight system monitor that lives in your system tray.

## Features

- RAM usage monitoring
- CPU usage display
- Disk space tracking
- Runs silently in system tray
- Starts automatically with Windows

## Installation

1. Install Python 3.8+
2. Install dependencies: `pip install -r requirements.txt`
3. Run `install_startup.bat` as Administrator to enable auto-start
4. Run `start_tray_manager.bat` to launch

## Files

| File | Purpose |
|------|---------|
| `tray_manager.py` | Main application |
| `start_tray_manager.bat` | Launch script |
| `install_startup.bat` | Enable auto-start with Windows |
| `config.json` | User settings |

## Usage

- Left click: Show detailed stats
- Right click: Menu (Settings / Exit)

## Requirements

- Windows 10/11
- Python 3.8+
- psutil, pystray, Pillow

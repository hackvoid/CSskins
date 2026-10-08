@echo off
:: Request Admin Privileges to allow hotkeys to work
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :run
) else (
    echo Requesting Administrator permissions...
    powershell -Command "Start-Process -FilePath '%0' -Verb RunAs"
    exit
)

:run
:: Set the working directory to the folder containing this batch file
cd /d "%~dp0"

echo Checking and installing dependencies...
pip install PyQt6 pywin32 psutil keyboard >nul 2>&1

echo Launching Overlay...
python overlay.py

@echo off
echo ========================================================
echo Building Overlay Executable...
echo ========================================================

echo 1. Installing required Python libraries...
pip install PyQt6 pywin32 psutil keyboard pyinstaller

echo.
echo 2. Compiling overlay.py into an executable...
pyinstaller --noconsole --onefile --icon=NONE overlay.py

echo.
echo ========================================================
echo Build Complete! 
echo.
echo IMPORTANT NEXT STEPS:
echo 1. Open the newly created "dist" folder.
echo 2. Move your "ak47.png" image inside that "dist" folder (the .exe needs it).
echo 3. Right-click "overlay.exe" and select "Run as administrator".
echo ========================================================
pause

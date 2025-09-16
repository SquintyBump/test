@echo off
echo ===================================================
echo  Setting up virtual environment...
echo ===================================================
call venv\Scripts\activate

echo ===================================================
echo  Building the executable with PyInstaller...
echo ===================================================
pyinstaller run.spec

echo ===================================================
echo  Build complete!
echo  You can find the executable in the 'dist' folder.
echo ===================================================
pause

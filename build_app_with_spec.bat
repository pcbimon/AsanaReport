@echo off
echo Building Asana Report Desktop App...

REM Ensure PyInstaller is installed
pip install pyinstaller>=6.0.0

REM Run PyInstaller using the spec file
pyinstaller AsanaReportApp.spec --clean

echo Build completed. The executable is in the dist/AsanaReportApp directory.
pause

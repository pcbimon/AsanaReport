@echo off
echo ===============================================
echo Asana Report Desktop App - Setup Dependencies
echo ===============================================

echo Installing required packages...
pip install -r requirements.txt

echo.
echo Dependencies installed successfully!
echo.
echo To build the Windows desktop app, run:
echo python build_windows_app.py
echo.
echo To run the web version, run:
echo streamlit run app.py
echo.
pause

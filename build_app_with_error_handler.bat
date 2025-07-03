@echo off
echo Building Asana Report Desktop App with Error Handler...

REM Create a spec file first
pyinstaller --name=AsanaReportApp ^
    --onedir ^
    --noconsole ^
    --clean ^
    --hidden-import=importlib.metadata ^
    --hidden-import=importlib.resources ^
    --hidden-import=streamlit ^
    --collect-all=streamlit ^
    --collect-all=importlib.metadata ^
    --add-data "modules;modules" ^
    --add-data "static;static" ^
    --add-data "Task.py;." ^
    --add-data "task_template.json;." ^
    desktop_app_error_handler.py

echo Build completed. The executable is in the dist/AsanaReportApp directory.
pause

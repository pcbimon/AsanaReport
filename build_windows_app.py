import PyInstaller.__main__
import os
import sys

# Get the absolute path to the script's directory
base_path = os.path.dirname(os.path.abspath(__file__))

# Define paths
desktop_app_path = os.path.join(base_path, "desktop_app.py")
icon_path = os.path.join(base_path, "static", "icon.ico")

# Check if icon exists, if not, create an empty list
icon_option = ["--icon", icon_path] if os.path.exists(icon_path) else []

# Define arguments for PyInstaller
args = [
    desktop_app_path,
    "--name=AsanaReportApp",
    "--onedir",
    "--noconsole",
    "--clean",
    "--add-data", f"{os.path.join(base_path, 'modules')}{os.pathsep}modules",
    "--add-data", f"{os.path.join(base_path, 'static')}{os.pathsep}static",
    "--add-data", f"{os.path.join(base_path, 'Task.py')}{os.pathsep}.",
    "--add-data", f"{os.path.join(base_path, 'task_template.json')}{os.pathsep}."
]

# Add icon if it exists
if icon_option:
    args.extend(icon_option)

# Run PyInstaller
PyInstaller.__main__.run(args)

print("Build completed. The executable is in the dist/AsanaReportApp directory.")

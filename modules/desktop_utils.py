import os
import sys
import platform
import subprocess
from pathlib import Path

def get_application_path():
    """Get the application path, whether running from PyInstaller or not."""
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle (PyInstaller)
        return Path(sys._MEIPASS)
    else:
        # If running in a normal Python environment
        return Path(os.path.abspath(os.path.dirname(__file__)))

def is_packaged_app():
    """Check if app is running as a packaged application."""
    # ตรวจสอบว่ากำลังรันเป็น PyInstaller package หรือไม่
    is_frozen = getattr(sys, 'frozen', False)
    
    # ถ้ามีการกำหนดตัวแปรสภาพแวดล้อม STREAMLIT_DESKTOP_MODE=1 
    # ให้ถือว่ากำลังรันในโหมด desktop แม้จะไม่ได้ package ด้วย PyInstaller
    force_desktop_mode = os.environ.get("STREAMLIT_DESKTOP_MODE") == "1"
    
    return is_frozen or force_desktop_mode

def get_resource_path(relative_path):
    """Get the path to a resource, whether running from PyInstaller or not."""
    base_path = get_application_path()
    return os.path.join(base_path, relative_path)

def get_os_type():
    """Returns the OS type (Windows, macOS, or Linux)."""
    system = platform.system()
    if system == "Darwin":
        return "macOS"
    elif system == "Windows":
        return "Windows"
    elif system == "Linux":
        return "Linux"
    else:
        return "Unknown"

def open_file_explorer(path):
    """Opens the file explorer at the specified path."""
    os_type = get_os_type()
    path = os.path.normpath(path)
    
    if os_type == "Windows":
        os.startfile(path)
    elif os_type == "macOS":
        subprocess.run(["open", path])
    elif os_type == "Linux":
        subprocess.run(["xdg-open", path])

def get_file_source_type(file_source):
    """
    ตรวจสอบประเภทของ file_source ว่าเป็น path จากการเลือกไฟล์หรือเป็น uploaded file
    
    Args:
        file_source: ไฟล์ที่ได้จาก create_file_uploader_with_dialog
        
    Returns:
        source_type: ประเภทของ file_source ("path", "uploaded", หรือ None)
        filename: ชื่อไฟล์ (ไม่รวม path) หรือ None
    """
    if file_source is None:
        return None, None
    
    if isinstance(file_source, str):
        # กรณีเป็น path จาก file dialog
        return "path", os.path.basename(file_source)
    else:
        # กรณีเป็น uploaded file
        return "uploaded", file_source.name

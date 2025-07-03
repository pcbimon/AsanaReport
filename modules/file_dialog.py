import streamlit as st
import os
import tkinter as tk
from tkinter import filedialog
import platform

def select_file_dialog(initial_dir=None, file_types=(("JSON files", "*.json"), ("All files", "*.*"))):
    """
    Opens a file selection dialog and returns the selected file path.
    This is used when the app is running as a desktop application.
    
    Args:
        initial_dir: The initial directory to open the dialog in
        file_types: A tuple of tuples with file type descriptions and patterns
        
    Returns:
        The selected file path or None if cancelled
    """
    # Hide the main Tkinter window
    root = tk.Tk()
    root.withdraw()
    
    # Make it rise above all windows (needed on some platforms)
    root.attributes('-topmost', True)
    
    # Set initial directory
    if initial_dir is None:
        # Use home directory as default
        initial_dir = os.path.expanduser("~")
    
    # Show the file dialog
    file_path = filedialog.askopenfilename(
        initialdir=initial_dir,
        title="เลือกไฟล์ JSON",
        filetypes=file_types
    )
    
    # Destroy the root window
    root.destroy()
    
    # Return the selected file path (or empty string if canceled)
    return file_path if file_path else None

def create_file_uploader_with_dialog(label, type=None, accept_multiple_files=False, help=None, initial_dir=None, key=None, is_desktop=False):
    """
    Creates a file uploader with a fallback file dialog for desktop apps.
    
    Args:
        label: The label to display for the file uploader
        type: The file types to accept
        accept_multiple_files: Whether to allow multiple files
        help: Help text for the uploader
        initial_dir: The initial directory for the file dialog
        key: Optional key for Streamlit component
        is_desktop: Whether the app is running as a desktop app
        
    Returns:
        The uploaded file or selected file path
    """
    # ถ้าเป็นแอป Desktop ให้แสดงทั้งตัวอัปโหลดและปุ่มเลือกไฟล์
    if is_desktop:
        # Create columns for the standard uploader and the file dialog button
        col1, col2 = st.columns([3, 1])
        
        # Use the standard streamlit uploader
        with col1:
            uploaded_file = st.file_uploader(label, type=type, accept_multiple_files=accept_multiple_files, help=help, key=f"uploader_{key}")
        
        # Add a button to use file dialog (for desktop app)
        with col2:
            use_dialog = st.button("📂 เลือกไฟล์จากเครื่อง", help="เลือกไฟล์จากเครื่องคอมพิวเตอร์", key=f"dialog_btn_{key}")
        
        # If the dialog button is clicked, open the file dialog
        if use_dialog:
            file_path = select_file_dialog(initial_dir=initial_dir)
            if file_path:
                # Display the selected file
                st.success(f"เลือกไฟล์: {os.path.basename(file_path)}")
                return file_path
    else:
        # ถ้าไม่ใช่ Desktop app ให้แสดงเฉพาะตัวอัปโหลดปกติ
        uploaded_file = st.file_uploader(label, type=type, accept_multiple_files=accept_multiple_files, help=help, key=f"uploader_{key}")
    
    return uploaded_file

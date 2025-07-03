"""
PyInstaller hook for Streamlit

This hook ensures all Streamlit dependencies are properly collected
"""

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect all Streamlit data files
datas = collect_data_files('streamlit')

# Make sure to collect all submodules
hiddenimports = collect_submodules('streamlit')

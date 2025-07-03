"""
PyInstaller hook for Plotly

This hook ensures all Plotly JSON data files are properly collected
"""

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect all Plotly data files
datas = collect_data_files('plotly')

# Make sure to collect all submodules
hiddenimports = collect_submodules('plotly')

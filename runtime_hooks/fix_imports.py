"""
Runtime hook to fix common import issues with Plotly and Streamlit
"""

import os
import sys
import inspect
from pathlib import Path


def _add_to_path(module_name, path_list):
    """Add module paths to sys.path if they exist"""
    for p in path_list:
        if isinstance(p, str) and os.path.exists(p):
            if p not in sys.path:
                sys.path.insert(0, p)
                return True
    return False


# Fix Plotly validators.json location
def setup_plotly():
    try:
        import plotly
        # Get the actual location of plotly
        plotly_dir = os.path.dirname(inspect.getfile(plotly))
        
        # The validators file should be here
        validators_file = os.path.join(plotly_dir, 'validators', '_validators.json')
        
        # If it doesn't exist, we need to check alternate locations
        if not os.path.exists(validators_file):
            # Try looking in _internal directory
            base_dir = os.path.dirname(os.path.dirname(plotly_dir))
            alt_validators_file = os.path.join(base_dir, 'plotly', 'validators', '_validators.json')
            
            if os.path.exists(alt_validators_file):
                # Create the destination directory if it doesn't exist
                os.makedirs(os.path.join(plotly_dir, 'validators'), exist_ok=True)
                
                # Copy the file to where plotly expects it
                import shutil
                shutil.copy2(alt_validators_file, validators_file)
        
        # Also check for the schema
        schema_file = os.path.join(plotly_dir, 'package_data', 'plot-schema.json')
        if not os.path.exists(schema_file):
            alt_schema_file = os.path.join(base_dir, 'plotly', 'package_data', 'plot-schema.json')
            if os.path.exists(alt_schema_file):
                os.makedirs(os.path.join(plotly_dir, 'package_data'), exist_ok=True)
                import shutil
                shutil.copy2(alt_schema_file, schema_file)
    except Exception as e:
        print(f"Error setting up Plotly: {e}")


# Make sure importlib.metadata can find packages
def setup_importlib_metadata():
    try:
        import importlib.metadata
        import importlib.resources
    except ImportError:
        pass


# Call setup functions
setup_plotly()
setup_importlib_metadata()

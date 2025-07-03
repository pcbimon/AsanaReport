import sys
import os
import traceback

# Handle importlib.metadata issues that can occur in PyInstaller builds
try:
    import importlib.metadata
except ImportError:
    pass

# Fix Plotly validators.json issue
def fix_plotly_validators():
    try:
        # Try to set up Plotly's file paths
        import plotly
        plotly_dir = os.path.dirname(os.path.dirname(plotly.__file__))
        
        # Check if we're in a PyInstaller bundle
        if hasattr(sys, '_MEIPASS'):
            # Look for validators in the PyInstaller _MEIPASS location
            base_dir = sys._MEIPASS
            
            # Check if validators exist in plotly package
            validators_path = os.path.join(plotly_dir, 'plotly', 'validators', '_validators.json')
            if not os.path.exists(validators_path):
                # Try to find the validators in the PyInstaller bundle
                alternate_path = os.path.join(base_dir, 'plotly', 'validators', '_validators.json')
                if os.path.exists(alternate_path):
                    # Create the directory if it doesn't exist
                    os.makedirs(os.path.dirname(validators_path), exist_ok=True)
                    # Copy the file to where plotly expects it
                    import shutil
                    shutil.copy2(alternate_path, validators_path)
    except Exception as e:
        print(f"Warning: Failed to fix Plotly validators: {e}")

# Try to fix Plotly before importing Streamlit
fix_plotly_validators()

try:
    # Make sure plotly is ready before importing streamlit
    try:
        import plotly
        import plotly.graph_objs as go
    except Exception as e:
        print(f"Warning: Issue with Plotly import: {e}")
    
    # Now import streamlit
    import streamlit.web.bootstrap
except ImportError as e:
    print(f"Error importing Streamlit: {e}")
    print("Make sure Streamlit is properly installed and packaged.")
    traceback.print_exc()
    
    # Try to show a GUI error message
    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", f"Failed to start application: {e}")
        root.destroy()
    except:
        pass
    
    sys.exit(1)

# Get the absolute path to the current script's directory
app_path = os.path.dirname(os.path.abspath(__file__))

# Get the main app.py file path
main_script_path = os.path.join(app_path, "app.py")

# Run the Streamlit app with correct parameters
streamlit.web.bootstrap.run(
    main_script_path=main_script_path,
    is_hello=False,
    args=[],
    flag_options={}
)

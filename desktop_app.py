import sys
import os

# Handle importlib.metadata issues that can occur in PyInstaller builds
try:
    import importlib.metadata
except ImportError:
    pass

try:
    import streamlit.web.bootstrap
except ImportError as e:
    print(f"Error importing Streamlit: {e}")
    print("Make sure Streamlit is properly installed and packaged.")
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

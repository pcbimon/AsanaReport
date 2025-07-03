import streamlit.web.bootstrap
import sys
import os

# Get the absolute path to the current script's directory
app_path = os.path.dirname(os.path.abspath(__file__))

# Set up arguments for the Streamlit app
args = []

# Add the main app.py file as the first argument
args.append(os.path.join(app_path, "app.py"))

# Run the Streamlit app
streamlit.web.bootstrap.run(args, "", "", "", "")

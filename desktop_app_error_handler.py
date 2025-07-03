import os
import sys
import traceback
import tempfile
import datetime

def run_app_with_error_handling():
    try:
        # Try to import streamlit after handling importlib.metadata
        try:
            import importlib.metadata
        except ImportError:
            pass

        import streamlit.web.bootstrap

        # Get the absolute path to the current script's directory
        app_path = os.path.dirname(os.path.abspath(__file__))

        # Set up arguments for the Streamlit app
        args = []

        # Add the main app.py file as the first argument
        args.append(os.path.join(app_path, "app.py"))

        # Run the Streamlit app
        streamlit.web.bootstrap.run(args, "", "", "", "")
    except Exception as e:
        # Create an error log
        error_log_dir = os.path.join(tempfile.gettempdir(), "AsanaReportApp")
        os.makedirs(error_log_dir, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        error_log_path = os.path.join(error_log_dir, f"error_log_{timestamp}.txt")
        
        with open(error_log_path, "w") as f:
            f.write(f"Error occurred at {datetime.datetime.now()}\n\n")
            f.write(f"Exception: {str(e)}\n\n")
            f.write("Traceback:\n")
            f.write(traceback.format_exc())
            f.write("\n\nSystem Information:\n")
            f.write(f"Python version: {sys.version}\n")
            f.write(f"Platform: {sys.platform}\n")
            
            # Try to get installed packages
            try:
                import pkg_resources
                f.write("\nInstalled packages:\n")
                for pkg in pkg_resources.working_set:
                    f.write(f"{pkg.key}=={pkg.version}\n")
            except:
                f.write("Could not retrieve package information\n")
        
        # Show error message in a simple GUI
        try:
            import tkinter as tk
            from tkinter import messagebox
            
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            
            messagebox.showerror(
                "Asana Report App Error",
                f"An error occurred while starting the application:\n\n{str(e)}\n\n"
                f"An error log has been created at:\n{error_log_path}\n\n"
                "Please include this log file when reporting the issue."
            )
            
            root.destroy()
        except:
            # If tkinter fails, try to show console message
            print(f"ERROR: {str(e)}")
            print(f"Error log created at: {error_log_path}")
            input("Press Enter to exit...")
        
        sys.exit(1)

if __name__ == "__main__":
    run_app_with_error_handling()

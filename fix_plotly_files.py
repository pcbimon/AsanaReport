import os
import sys
import shutil
import glob

def fix_plotly_validators():
    """
    This script manually fixes the Plotly validators.json issue
    Run this after building the PyInstaller package if you still see the error
    """
    try:
        # Determine the dist directory
        dist_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist', 'AsanaReportApp')
        
        if not os.path.exists(dist_dir):
            print(f"Error: Distribution directory not found at {dist_dir}")
            return False
        
        # Find plotly validators in the distribution
        plotly_validators = glob.glob(os.path.join(dist_dir, '**', 'plotly', 'validators', '_validators.json'), recursive=True)
        
        if not plotly_validators:
            print("Error: Could not find plotly validators in the distribution")
            return False
        
        source_validator = plotly_validators[0]
        print(f"Found validator at: {source_validator}")
        
        # Find all plotly packages in the distribution
        plotly_packages = glob.glob(os.path.join(dist_dir, '**', 'plotly', '__init__.py'), recursive=True)
        
        if not plotly_packages:
            print("Error: Could not find plotly packages in the distribution")
            return False
        
        # For each plotly package, make sure it has the validators
        for plotly_init in plotly_packages:
            plotly_dir = os.path.dirname(plotly_init)
            target_validator_dir = os.path.join(plotly_dir, 'validators')
            target_validator_file = os.path.join(target_validator_dir, '_validators.json')
            
            if not os.path.exists(target_validator_file):
                print(f"Fixing missing validator in: {plotly_dir}")
                os.makedirs(target_validator_dir, exist_ok=True)
                shutil.copy2(source_validator, target_validator_file)
        
        # Also check for the schema file
        plotly_schemas = glob.glob(os.path.join(dist_dir, '**', 'plotly', 'package_data', 'plot-schema.json'), recursive=True)
        
        if plotly_schemas:
            source_schema = plotly_schemas[0]
            print(f"Found schema at: {source_schema}")
            
            for plotly_init in plotly_packages:
                plotly_dir = os.path.dirname(plotly_init)
                target_schema_dir = os.path.join(plotly_dir, 'package_data')
                target_schema_file = os.path.join(target_schema_dir, 'plot-schema.json')
                
                if not os.path.exists(target_schema_file):
                    print(f"Fixing missing schema in: {plotly_dir}")
                    os.makedirs(target_schema_dir, exist_ok=True)
                    shutil.copy2(source_schema, target_schema_file)
        
        print("Plotly files fix completed successfully")
        return True
        
    except Exception as e:
        print(f"Error fixing plotly files: {e}")
        return False

if __name__ == "__main__":
    if fix_plotly_validators():
        print("Fix applied successfully. Try running the application now.")
    else:
        print("Failed to apply the fix. Please check the error messages above.")

#!/usr/bin/env python3
"""
Dashboard - CustomTkinter macOS Application
Main entry point for the Dashboard application.
"""

import sys
import os
from pathlib import Path

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative
    return Path(__file__).parent / relative


# Add the app directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the main Dashboard window
from app.ui.main_window import Dashboard


# -----------------------------
# Resource Path Handling for PyInstaller
# -----------------------------
def resource_path(relative_path: str) -> Path:
    """
    Get absolute path to resource, works for dev and for PyInstaller.
    PyInstaller creates a temp folder and stores path in _MEIPASS
    """
    if hasattr(sys, '_MEIPASS'):
        # Running in PyInstaller bundle
        base_path = Path(sys._MEIPASS)
    else:
        # Running in normal Python environment
        base_path = Path(__file__).parent
    
    return base_path / relative_path


# Set up resource paths for the application
os.environ['RESOURCE_BASE'] = str(resource_path(''))


# -----------------------------
# Main Application Entry
# -----------------------------
def main():
    """
    Main entry point for the Dashboard application.
    """
    try:
        # Create and run the Dashboard
        app = Dashboard()
        
        # Handle graceful exit
        app.protocol("WM_DELETE_WINDOW", app.on_closing)
        
        # Start the application main loop
        app.mainloop()
        
    except Exception as e:
        # Handle any startup errors
        print(f"Error starting Dashboard: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

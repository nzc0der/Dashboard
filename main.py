import os
import sys

# Ensure we can import from the app directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.ui.main_window import ZenithOS

if __name__ == "__main__":
    app = ZenithOS()
    try:
        app.mainloop()
    except KeyboardInterrupt:
        print("\nExiting application...")
        sys.exit(0)
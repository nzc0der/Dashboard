import customtkinter as ctk
from datetime import datetime
from app.ui.styles import Styles

class ClockWidget(ctk.CTkFrame):
    """
    Displays current time, date, and day of the week.
    Updates every second.
    """
    
    def __init__(self, parent):
        super().__init__(parent, **Styles.FRAME_CONFIG)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Time Label (Big)
        self.time_lbl = ctk.CTkLabel(
            self, 
            text="00:00", 
            font=("Roboto Medium", 64),
            text_color="white"
        )
        self.time_lbl.pack(pady=(20, 0))

        # Date Label (Medium)
        self.date_lbl = ctk.CTkLabel(
            self, 
            text="Loading Date...", 
            font=("Roboto", 16),
            text_color="#a0a0a0"
        )
        self.date_lbl.pack(pady=(0, 20))

        # Start the update loop
        self.update_clock()

    def update_clock(self):
        try:
            now = datetime.now()
            # Format: 12:45 PM
            current_time = now.strftime("%I:%M %p")
            # Format: Monday, January 01
            current_date = now.strftime("%A, %B %d, %Y")
            
            if self.time_lbl.cget("text") != current_time:
                self.time_lbl.configure(text=current_time)
            
            if self.date_lbl.cget("text") != current_date:
                self.date_lbl.configure(text=current_date)
        except Exception as e:
            # Handle potential tkinter destroyed error
            print(f"Clock Update Error: {e}")
            return

        # Schedule next update in 500ms to be snappy
        self.after(500, self.update_clock)

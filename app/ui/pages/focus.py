import customtkinter as ctk
from app.ui.styles import Styles

class FocusPage(ctk.CTkFrame):
    """
    Distraction-Free Focus Zone.
    """
    def __init__(self, parent, db):
        super().__init__(parent, fg_color="transparent")
        
        # Center Content
        # self.pack(fill="both", expand=True) <--- REMOVED

        
        # Header
        self.header = ctk.CTkLabel(
            self, 
            text="Deep Focus Mode", 
            font=Styles.H1, 
            text_color="white"
        )
        self.header.pack(pady=40)
        
        # Timer (Pomodoro Style)
        self.timer_frame = ctk.CTkFrame(self, fg_color=Styles.BG_CARD, corner_radius=100, width=300, height=300)
        self.timer_frame.pack(pady=20)
        
        self.timer_lbl = ctk.CTkLabel(
            self.timer_frame, 
            text="25:00", 
            font=("SF Pro Display", 80, "bold"),
            text_color=Styles.BLUE
        )
        self.timer_lbl.place(relx=0.5, rely=0.5, anchor="center")
        
        # Controls
        self.btn_start = ctk.CTkButton(
            self, 
            text="Start Focus", 
            width=200, height=50, 
            corner_radius=25, 
            fg_color=Styles.BLUE, 
            font=("Arial", 18, "bold")
        )
        self.btn_start.pack(pady=30)
        
        # Bottom Quote
        self.quote = ctk.CTkLabel(
            self, 
            text='"Success is the sum of small efforts, repeated day in and day out."', 
            font=("SF Pro Text", 16, "italic"),
            text_color=Styles.TEXT_SEC
        )
        self.quote.pack(pady=20)

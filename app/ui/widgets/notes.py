import customtkinter as ctk
from app.ui.styles import Styles

class NotesWidget(ctk.CTkFrame):
    """
    Minimalist Notes Card.
    """
    def __init__(self, parent, db):
        super().__init__(parent, fg_color=Styles.BG_CARD, corner_radius=Styles.RADIUS_L)
        self.db = db
        
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            self.header_frame, 
            text="Logs", 
            font=Styles.H3, 
            text_color="white"
        ).pack(side="left")
        
        # Save Indicator
        self.save_lbl = ctk.CTkLabel(
            self.header_frame, 
            text="SAVED", 
            font=Styles.CAPTION, 
            text_color=Styles.GREEN
        )
        self.save_lbl.pack(side="right")

        # Text Area
        self.txt = ctk.CTkTextbox(
            self, 
            font=Styles.BODY, 
            fg_color=Styles.BG_CARD_HOVER, 
            text_color=Styles.TEXT_MAIN,
            corner_radius=Styles.RADIUS_M,
            border_width=0,
            wrap="word"
        )
        self.txt.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Load
        self.txt.insert("0.0", db.get_notes())
        self.txt.bind("<KeyRelease>", self.save)

    def save(self, event=None):
        content = self.txt.get("0.0", "end")
        self.db.set_notes(content)
        self.save_lbl.configure(text="SAVING...", text_color=Styles.YELLOW)
        self.after(1000, lambda: self.save_lbl.configure(text="SAVED", text_color=Styles.GREEN))

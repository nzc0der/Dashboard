import customtkinter as ctk
from app.core.data_manager import DataManager
from app.ui.styles import Styles

class NotesWidget(ctk.CTkFrame):
    """
    Apple Notes Style (Yellow/Textured or just Dark Grey)
    """
    def __init__(self, parent, db: DataManager):
        # Card style
        super().__init__(parent, **Styles.CARD_CONFIG)
        self.db = db
        
        # Header (Looks like paper header)
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            self.header_frame, 
            text="Notes", 
            font=Styles.FONT_HEADER, 
            text_color="#FFD60A" # Apple Notes Yellow text for header
        ).pack(side="left")
        
        # Save Icon (Floppy disk or checkmark)
        self.save_btn = ctk.CTkButton(
            self.header_frame, 
            text="Save", 
            width=60, height=30, 
            corner_radius=15, 
            fg_color="transparent", 
            text_color="#FFD60A",
            hover_color="#333",
            command=self.manual_save
        )
        self.save_btn.pack(side="right")

        # Text Area (Textured look simulation via color)
        self.textbox = ctk.CTkTextbox(
            self, 
            font=("SF Pro Text", 16), 
            wrap="word", 
            fg_color="#1C1C1E", 
            text_color="#E5E5EA",
            corner_radius=15,
            border_width=0
        )
        self.textbox.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Load Content
        initial_text = self.db.get_notes()
        self.textbox.insert("0.0", initial_text)

        # Auto-save binding
        self.textbox.bind("<KeyRelease>", self.auto_save)

    def manual_save(self):
        self.save_data()
        self.save_btn.configure(text="Saved!")
        self.after(2000, lambda: self.save_btn.configure(text="Save"))

    def auto_save(self, event=None):
        self.save_data()
        if self.save_btn.cget("text") != "Saving...":
            self.save_btn.configure(text="Saving...")
            self.after(1000, lambda: self.save_btn.configure(text="Save"))

    def save_data(self):
        content = self.textbox.get("0.0", "end")
        self.db.set_notes(content)

import customtkinter as ctk
from app.core.data_manager import DataManager

class NotesWidget(ctk.CTkFrame):
    def __init__(self, parent, db: DataManager):
        super().__init__(parent, corner_radius=15, fg_color="#1a1a1a")
        self.db = db
        
        self.header = ctk.CTkLabel(self, text="LOGS & NOTES", font=("Arial", 16, "bold"), anchor="w")
        self.header.pack(fill="x", pady=10, padx=15)

        self.textbox = ctk.CTkTextbox(self, font=("Consolas", 14), wrap="word", fg_color="#2b2b2b", text_color="#d0d0d0")
        self.textbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Load Content
        initial_text = self.db.get_notes()
        self.textbox.insert("0.0", initial_text)

        # Auto-save binding (every key release)
        self.textbox.bind("<KeyRelease>", self.auto_save)

        # Status Bar
        self.status = ctk.CTkLabel(self, text="Saved", text_color="gray", font=("Arial", 10), anchor="e")
        self.status.pack(side="bottom", fill="x", padx=10, pady=2)

    def auto_save(self, event=None):
        content = self.textbox.get("0.0", "end")
        self.db.set_notes(content)
        self.status.configure(text="Saving...")
        self.after(1000, lambda: self.status.configure(text="Saved"))

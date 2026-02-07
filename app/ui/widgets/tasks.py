import customtkinter as ctk
from app.ui.styles import Styles

class TaskManagerWidget(ctk.CTkFrame):
    """
    Minimalist Checklist Card.
    """
    def __init__(self, parent, db):
        super().__init__(parent, fg_color=Styles.BG_CARD, corner_radius=Styles.RADIUS_L)
        self.db = db
        
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            self.header_frame, 
            text="Objectives", 
            font=Styles.H3, 
            text_color="white"
        ).pack(side="left")
        
        # Add (Circle)
        self.add_btn = ctk.CTkButton(
            self.header_frame, 
            text="+", 
            width=30, height=30, 
            corner_radius=15, 
            fg_color=Styles.PRIMARY, 
            hover_color="#0062CC",
            font=("Arial", 18),
            command=self.show_add
        )
        self.add_btn.pack(side="right")

        # Input (Floating)
        self.input_entry = ctk.CTkEntry(
            self, 
            placeholder_text="Add item...",
            height=40,
            corner_radius=Styles.RADIUS_M,
            border_width=0,
            fg_color=Styles.BG_CARD_HOVER,
            text_color="white",
            placeholder_text_color=Styles.TEXT_SEC
        )
        self.input_entry.pack(fill="x", padx=20, pady=(0, 10))
        self.input_entry.bind("<Return>", self.add_task)

        # List
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", label_text=None)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 20))

        self.refresh_ui()

    def show_add(self):
        self.input_entry.focus_set()

    def add_task(self, event=None):
        text = self.input_entry.get().strip()
        if text:
            self.db.add_task(text)
            self.input_entry.delete(0, "end")
            self.refresh_ui()

    def refresh_ui(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        tasks = self.db.get_tasks()
        sorted_tasks = sorted(tasks, key=lambda x: x["done"])

        if not tasks:
            ctk.CTkLabel(self.scroll_frame, text="All objectives complete.", text_color=Styles.TEXT_SEC).pack(pady=40)
            return

        for t in sorted_tasks:
            self.build_row(t)

    def build_row(self, task):
        row = ctk.CTkFrame(self.scroll_frame, fg_color="transparent", height=40)
        row.pack(fill="x", pady=2, padx=5)
        
        # Checkbox
        is_done = task["done"]
        chk_color = Styles.SECONDARY if is_done else Styles.BORDER_COLOR
        
        chk = ctk.CTkButton(
            row, 
            text="✓" if is_done else "", 
            width=24, height=24, 
            corner_radius=12,
            fg_color=chk_color, 
            hover_color=chk_color,
            font=("Arial", 14, "bold"),
            command=lambda id=task["id"]: self.toggle(id)
        )
        chk.pack(side="left", padx=10)
        
        # Text
        text_color = Styles.TEXT_SEC if is_done else "white"
        font = (Styles.FONT_FAMILY, 14, "overstrike") if is_done else Styles.BODY
        
        lbl = ctk.CTkLabel(row, text=task["text"], font=font, text_color=text_color, anchor="w")
        lbl.pack(side="left", fill="x", expand=True)
        
        # Delete
        del_btn = ctk.CTkButton(
            row, 
            text="✕", 
            width=24, height=24, 
            fg_color="transparent", 
            text_color="#FF3B30", 
            hover_color=Styles.BG_CARD_HOVER,
            command=lambda id=task["id"]: self.delete(id)
        )
        del_btn.pack(side="right")

    def toggle(self, id):
        self.db.toggle_task(id)
        self.refresh_ui()

    def delete(self, id):
        self.db.delete_task(id)
        self.refresh_ui()

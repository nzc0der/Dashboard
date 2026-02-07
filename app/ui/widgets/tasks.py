import customtkinter as ctk
from app.core.data_manager import DataManager
from app.ui.styles import Styles

class TaskManagerWidget(ctk.CTkFrame):
    """
    Premium Task List.
    iOS Reminders style.
    """
    def __init__(self, parent, db: DataManager):
        # Card style
        super().__init__(parent, **Styles.CARD_CONFIG)
        self.db = db
        
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            self.header_frame, 
            text="Objectives", 
            font=Styles.FONT_HEADER, 
            text_color="white"
        ).pack(side="left")
        
        # Add Button (Circular)
        self.add_btn = ctk.CTkButton(
            self.header_frame, 
            text="+", 
            width=30, height=30, 
            corner_radius=15, 
            fg_color="#0A84FF", 
            hover_color="#007AFF",
            font=("Arial", 18),
            command=self.show_add_dialog
        )
        self.add_btn.pack(side="right")

        # Input Field (Hidden by default, or just inline at top)
        self.input_var = ctk.StringVar()
        self.input_entry = ctk.CTkEntry(
            self, 
            textvariable=self.input_var,
            placeholder_text="Add new task...",
            height=40,
            corner_radius=12,
            border_width=0,
            fg_color="#2C2C2E",
            text_color="white",
            placeholder_text_color="#636366"
        )
        self.input_entry.pack(fill="x", padx=20, pady=(0, 10))
        self.input_entry.bind("<Return>", self.add_task)

        # List Area
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", label_text=None)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 20))

        self.refresh_ui()

    def show_add_dialog(self):
        self.input_entry.focus_set()

    def add_task(self, event=None):
        text = self.input_var.get().strip()
        if text:
            self.db.add_task(text)
            self.input_var.set("")
            self.refresh_ui()

    def refresh_ui(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        tasks = self.db.get_tasks()
        if not tasks:
            ctk.CTkLabel(self.scroll_frame, text="All objectives complete.", text_color="gray").pack(pady=40)
            return

        sorted_tasks = sorted(tasks, key=lambda x: x["done"])

        for t in sorted_tasks:
            self.build_task_row(t)

    def build_task_row(self, task):
        # Row Container
        bg_color = "transparent"
        text_color = "white" if not task["done"] else "#555"
        font = Styles.FONT_BODY if not task["done"] else (Styles.FONT_BODY[0], Styles.FONT_BODY[1], "overstrike")
        
        row = ctk.CTkFrame(self.scroll_frame, fg_color="transparent", height=40)
        row.pack(fill="x", pady=5, padx=5)
        
        # Check Circle (Custom Button)
        chk_color = "#3A3A3C" # Empty circle grey
        if task["done"]:
            chk_color = "#30D158" # Green
            
        chk_btn = ctk.CTkButton(
            row, 
            text="✓" if task["done"] else "", 
            width=24, height=24, 
            corner_radius=12,
            fg_color=chk_color, 
            hover_color="#32D74B",
            font=("Arial", 12, "bold"),
            command=lambda tid=task["id"]: self.toggle_task(tid)
        )
        chk_btn.pack(side="left", padx=(5, 10))

        # Text
        lbl_text = task["text"]
        lbl = ctk.CTkLabel(
            row, 
            text=lbl_text, 
            anchor="w", 
            font=font, 
            text_color=text_color
        )
        lbl.pack(side="left", fill="x", expand=True)

        # Delete (Only on hover? Or explicit button)
        # Explicit small 'x'
        del_btn = ctk.CTkButton(
            row, 
            text="✕", 
            width=24, height=24, 
            fg_color="transparent", 
            text_color="#FF453A", 
            hover_color="#3A3A3C",
            command=lambda tid=task["id"]: self.delete_task(tid)
        )
        del_btn.pack(side="right")

        # Separator Line
        separator = ctk.CTkFrame(self.scroll_frame, height=1, fg_color="#3A3A3C")
        separator.pack(fill="x", padx=10, pady=(0, 5))

    def toggle_task(self, task_id):
        self.db.toggle_task(task_id)
        self.refresh_ui()

    def delete_task(self, task_id):
        self.db.delete_task(task_id)
        self.refresh_ui()

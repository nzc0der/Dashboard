import customtkinter as ctk
import time
from app.core.data_manager import DataManager

class TaskManagerWidget(ctk.CTkFrame):
    def __init__(self, parent, db: DataManager):
        super().__init__(parent, corner_radius=15, fg_color="#1a1a1a")
        self.db = db
        
        # Header
        header = ctk.CTkLabel(self, text="MISSION OBJECTIVES", font=("Arial", 16, "bold"), anchor="w")
        header.pack(fill="x", pady=10, padx=15)

        # Input Area (Floating Action Bar style)
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.entry = ctk.CTkEntry(
            input_frame, 
            placeholder_text="Enter new objective...",
            height=35,
            border_width=0,
            fg_color="#2b2b2b"
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.entry.bind("<Return>", self.add_task)
        
        add_btn = ctk.CTkButton(
            input_frame, 
            text="+", 
            width=35, height=35, 
            fg_color="#1f6aa5", 
            command=self.add_task
        )
        add_btn.pack(side="right")

        # Scrollable List
        # Using a canvas or scrollable frame
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", label_text=None)
        self.scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.refresh_ui()

    def add_task(self, event=None):
        text = self.entry.get()
        if text.strip():
            self.db.add_task(text)
            self.entry.delete(0, "end")
            self.refresh_ui()

    def delete_task(self, task_id):
        self.db.delete_task(task_id)
        self.refresh_ui()

    def toggle_task(self, task_id):
        self.db.toggle_task(task_id)
        self.refresh_ui()

    def refresh_ui(self):
        # Prevent flickering by maybe checking diffs, but full rebuild is easier for small lists
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        tasks = self.db.get_tasks()
        
        if not tasks:
            ctk.CTkLabel(self.scroll_frame, text="All objectives complete.", text_color="gray").pack(pady=20)
            return

        # Sort tasks: incomplete first
        sorted_tasks = sorted(tasks, key=lambda x: x["done"])

        for t in sorted_tasks:
            self.build_task_row(t)

    def build_task_row(self, task):
        # Row Container
        bg_color = "#1f1f1f" if not task["done"] else "#121212"
        text_color = "white" if not task["done"] else "#555"
        font = ("Arial", 13) if not task["done"] else ("Arial", 13, "overstrike")
        
        row = ctk.CTkFrame(self.scroll_frame, fg_color=bg_color, corner_radius=8, height=45)
        row.pack(fill="x", pady=3, padx=2)
        
        # Checkbox (Custom fake checkbox)
        chk_text = "chk" if not task["done"] else "chk_active"
        # Using a button as checkbox for style
        chk_btn = ctk.CTkButton(
            row, 
            text="✓" if task["done"] else "",
            width=24, height=24,
            corner_radius=12,
            fg_color="#333" if not task["done"] else "#1f6aa5",
            hover_color="#444",
            command=lambda tid=task["id"]: self.toggle_task(tid)
        )
        chk_btn.pack(side="left", padx=10, pady=8)

        # Task Text
        lbl_text = task["text"][:40] + "..." if len(task["text"]) > 40 else task["text"]
        lbl = ctk.CTkLabel(row, text=lbl_text, anchor="w", font=font, text_color=text_color)
        lbl.pack(side="left", fill="x", expand=True, padx=5)

        # Delete Button (Hidden by default or always visible?)
        # Let's make it always visible for simplicity
        del_btn = ctk.CTkButton(
            row, 
            text="✕", 
            width=25, height=25, 
            fg_color="transparent", 
            hover_color="#800000", 
            text_color="#ff5555",
            command=lambda tid=task["id"]: self.delete_task(tid)
        )
        del_btn.pack(side="right", padx=5)

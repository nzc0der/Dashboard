import customtkinter as ctk
import webbrowser
from app.ui.styles import Styles

class QuickLinksWidget(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, height=100, corner_radius=15, fg_color="#1a1a1a")
        
        # Grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        links = [
            ("YouTube", "https://youtube.com", "#FF0000"),
            ("Gmail", "https://mail.google.com", "#DB4437"),
            ("GitHub", "https://github.com", "#FFFFFF"),
            ("ChatGPT", "https://chat.openai.com", "#10a37f"),
            ("Reddit", "https://reddit.com", "#FF4500")
        ]

        for idx, (name, url, color) in enumerate(links):
            btn = ctk.CTkButton(
                self, 
                text=name, 
                width=100, 
                height=40,
                corner_radius=20,
                fg_color="#2b2b2b", 
                border_width=1,
                border_color="#333",
                hover_color=color, # Accent color on hover
                text_color="white",
                font=("Arial", 12, "bold"),
                command=lambda u=url: webbrowser.open(u)
            )
            btn.grid(row=0, column=idx, padx=10, pady=15, sticky="ew")

        # Custom Link Adder (future)
        # self.add_btn = ctk.CTkButton(self, text="+", width=30, height=30, fg_color="transparent", border_width=1, border_color="gray")
        # self.add_btn.grid(row=0, column=5, padx=10)

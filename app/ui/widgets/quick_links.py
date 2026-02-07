import customtkinter as ctk
import webbrowser
from app.ui.styles import Styles

class QuickLinksWidget(ctk.CTkFrame):
    """
    iOS Home Screen Style Dock.
    """
    def __init__(self, parent):
        # Semi-transparent dock at bottom
        super().__init__(parent, fg_color="#1C1C1E", corner_radius=35, height=90)
        
        # Grid
        self.pack_propagate(False) # Keep fixed height
        
        links = [
            ("YouTube", "https://youtube.com", "#FF0000", "▶"),
            ("Gmail", "https://mail.google.com", "#EA4335", "✉"),
            ("GitHub", "https://github.com", "#181717", "G"),
            ("ChatGPT", "https://chat.openai.com", "#10a37f", "🤖"),
            ("Reddit", "https://reddit.com", "#FF4500", "R")
        ]
        
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=20, pady=10)

        for name, url, color, icon in links:
            btn = self._create_app_icon(container, name, url, color, icon)
            btn.pack(side="left", padx=15, expand=True)

    def _create_app_icon(self, parent, name, url, color, icon_char):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        
        # App Icon (Rounded Square)
        btn = ctk.CTkButton(
            frame, 
            text=icon_char, 
            width=50, height=50, 
            corner_radius=14, # Apple App Icon shape
            fg_color=color, 
            hover_color=color, # Maybe slightly lighter
            font=("Arial", 24, "bold"),
            command=lambda u=url: webbrowser.open(u)
        )
        btn.pack()
        
        # Label (Hidden or small below?)
        # Let's keep it minimal - just icon usually, but for clarity maybe label
        # Ideally hover shows label
        
        return frame

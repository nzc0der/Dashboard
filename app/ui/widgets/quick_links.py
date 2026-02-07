import customtkinter as ctk
import os
from PIL import Image
from app.ui.styles import Styles

class QuickLinksWidget(ctk.CTkFrame):
    """
    iOS Home Screen Style Dock with support for custom icons.
    """
    def __init__(self, parent):
        super().__init__(parent, fg_color=Styles.BG_CARD, corner_radius=Styles.RADIUS_L)
        
        self.pack_propagate(False) # Keep fixed height
        
        # Paths for icons
        self.icon_dir = os.path.join("assets", "icons", "links")
        
        self.links = [
            ("GitHub", "https://github.com", "#211F1F"),
            ("Notion", "https://notion.so", "#000000"),
            ("Gmail", "https://mail.google.com", "#EA4335"),
            ("ChatGPT", "https://chat.openai.com", "#10a37f"),
            ("YouTube", "https://youtube.com", "#FF0000"),
        ]
        
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=30, pady=20)

        for name, url, color in self.links:
            btn = self._create_link_button(container, name, url, color)
            btn.pack(side="left", padx=15, expand=True)

    def _create_link_button(self, parent, name, url, color):
        # Look for custom icon (png preferred for PIL, svg if library available)
        icon_path_png = os.path.join(self.icon_dir, f"{name.lower()}.png")
        icon_path_jpg = os.path.join(self.icon_dir, f"{name.lower()}.jpg")
        
        img = None
        if os.path.exists(icon_path_png):
            img = ctk.CTkImage(light_image=Image.open(icon_path_png), dark_image=Image.open(icon_path_png), size=(40, 40))
        elif os.path.exists(icon_path_jpg):
            img = ctk.CTkImage(light_image=Image.open(icon_path_jpg), dark_image=Image.open(icon_path_jpg), size=(40, 40))

        # Create Button
        btn = ctk.CTkButton(
            parent, 
            text=name[:2] if not img else "", 
            image=img,
            width=60, height=60, 
            corner_radius=18, # Squircle
            fg_color=color, 
            hover_color=color,
            font=("SF Pro Display", 24, "bold"),
            command=lambda u=url: self.open(u)
        )
        return btn

    def open(self, url):
        import webbrowser
        webbrowser.open(url)

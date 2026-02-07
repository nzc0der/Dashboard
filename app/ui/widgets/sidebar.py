import customtkinter as ctk
from app.ui.styles import Styles

class Sidebar(ctk.CTkFrame):
    """
    Advanced Sidebar with visual indicators.
    """
    def __init__(self, parent, nav_callback):
        super().__init__(parent, fg_color=Styles.BG_SIDEBAR, width=90, corner_radius=0)
        self.nav_callback = nav_callback
        self.active_btn = None
        self.buttons = {}

        # 1. Logo
        self.logo = ctk.CTkLabel(
            self, 
            text="⌘", # Command Icon (Mac style)
            font=(Styles.FONT_FAMILY, 36),
            text_color=Styles.TEXT_MAIN
        )
        self.logo.pack(pady=(40, 50))

        # 2. Nav Items
        items = [
            ("house.fill", "Home", "home", "🏠"),
            ("bolt.fill", "Focus", "focus", "⚡"),
            ("play.rectangle.fill", "Media", "media", "▶"),
            ("gear", "Settings", "settings", "⚙️")
        ]

        # Container for nav to center it vertically if needed
        self.nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.nav_frame.pack(fill="x", expand=True, anchor="n")

        for _, name, pid, icon in items:
            btn = self._make_btn(icon, pid)
            btn.pack(pady=12)
            self.buttons[pid] = btn
            
        # 3. User Avatar (Bottom)
        self.avatar = ctk.CTkButton(
            self, 
            text="KD", 
            width=44, height=44, 
            corner_radius=22, 
            fg_color="#333", 
            hover_color="#444",
            font=("Arial", 16, "bold"),
            command=lambda: print("Profile Clicked")
        )
        self.avatar.pack(side="bottom", pady=40)

        self.set_active("home")

    def _make_btn(self, icon, pid):
        # Apply Styles.SIDEBAR_BTN configuration
        btn = ctk.CTkButton(
            self.nav_frame, 
            text=icon, 
            command=lambda: self.nav_callback(pid),
            **Styles.SIDEBAR_BTN
        )
        return btn

    def set_active(self, page_id):
        for pid, btn in self.buttons.items():
            if pid == page_id:
                btn.configure(
                    fg_color=Styles.PRIMARY, 
                    text_color="white",
                    hover_color=Styles.PRIMARY_HOVER
                )
            else:
                btn.configure(
                    fg_color=Styles.SIDEBAR_BTN["fg_color"], 
                    text_color=Styles.SIDEBAR_BTN["text_color"],
                    hover_color=Styles.SIDEBAR_BTN["hover_color"]
                )

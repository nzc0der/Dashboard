import customtkinter as ctk

from app.core import settings
from app.core.data_manager import DataManager

# Navigation
from app.ui.widgets.sidebar import Sidebar

# Pages
from app.ui.pages.home import HomePage
from app.ui.pages.focus import FocusPage
from app.ui.pages.media import MediaPage

class ZenithOS(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Config ---
        self.title(f"{settings.APP_NAME}")
        self.geometry("1400x900")
        self.minsize(1000, 700)
        
        # --- Theme ---
        ctk.set_appearance_mode(settings.THEME_MODE)
        self.configure(fg_color="#000000") # Pure Black (OLED)

        # --- Data & State ---
        self.db = DataManager(settings.DATA_FILE)
        self.current_page = None

        # --- Layout ---
        self.grid_columnconfigure(0, weight=0, minsize=90) # Sidebar
        self.grid_columnconfigure(1, weight=1)             # Content
        self.grid_rowconfigure(0, weight=1)

        # 1. Sidebar (Persistent)
        self.sidebar = Sidebar(self, nav_callback=self.navigate_to)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # 2. Content Container
        self.content_area = ctk.CTkFrame(self, fg_color="transparent")
        self.content_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.content_area.grid_columnconfigure(0, weight=1)
        self.content_area.grid_rowconfigure(0, weight=1)

        # 3. Initialize Pages Cache (Lazy loading possible, but let's pre-load for speed)
        self.pages = {
            "home": HomePage(self.content_area, self.db),
            "focus": FocusPage(self.content_area, self.db),
            "media": MediaPage(self.content_area),
            "settings": self._create_placeholder("Settings")
        }

        # Start at Home
        self.navigate_to("home")


    def navigate_to(self, page_id):
        # Update Sidebar State
        self.sidebar.set_active(page_id)

        # Hide current page
        if self.current_page:
            self.current_page.grid_forget()

        # Show new page
        if page_id in self.pages:
            new_page = self.pages[page_id]
            new_page.grid(row=0, column=0, sticky="nsew")
            self.current_page = new_page
        else:
            print(f"Page {page_id} not found!")

    def _create_placeholder(self, title):
        frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        lbl = ctk.CTkLabel(frame, text=title, font=("Arial", 32, "bold"))
        lbl.pack(expand=True)
        return frame

    def on_closing(self):
        self.db.save()
        self.destroy()

if __name__ == "__main__":
    app = ZenithOS()
    # Handle graceful exit
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()

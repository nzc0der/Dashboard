import customtkinter as ctk
from PIL import Image

from app.core import settings
from app.core.data_manager import DataManager
from app.ui.styles import Styles

# Widgets
from app.ui.widgets.clock import ClockWeatherWidget
from app.ui.widgets.music import MusicPlayerWidget
from app.ui.widgets.system_monitor import SystemMonitorWidget
from app.ui.widgets.tasks import TaskManagerWidget
from app.ui.widgets.notes import NotesWidget
from app.ui.widgets.quick_links import QuickLinksWidget

class ZenithOS(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Config
        self.title(f"{settings.APP_NAME}")
        self.geometry("1400x900") # Larger window for 'Desktop' feel
        
        # Theme
        ctk.set_appearance_mode(settings.THEME_MODE)
        self.configure(fg_color="#000000") # Pure Black Background

        # Data
        self.db = DataManager(settings.DATA_FILE)

        # Layout: Grid System (Bento Box)
        # Left Sidebar (Navigation/Status) | Main Workspace (Cards)
        
        self.grid_columnconfigure(0, weight=0, minsize=80) # Sidebar
        self.grid_columnconfigure(1, weight=1) # Main
        self.grid_rowconfigure(0, weight=1)

        # === 1. SIDEBAR (Left) ===
        self.sidebar = ctk.CTkFrame(self, fg_color="#101010", width=80, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Sidebar Icons (Text for now, FontAwesome ideally)
        icons = ["🏠", "⚡", "🎵", "⚙️"]
        for i, ico in enumerate(icons):
            btn = ctk.CTkButton(
                self.sidebar, 
                text=ico, 
                width=50, height=50, 
                corner_radius=15, 
                fg_color="transparent", 
                hover_color="#333",
                font=("Arial", 24)
            )
            btn.pack(pady=20 if i == 0 else 10)

        # === 2. MAIN WORKSPACE (Right) ===
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        
        # Grid within Main Area
        # 3 Columns
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_columnconfigure(1, weight=1)
        self.main_area.grid_columnconfigure(2, weight=1)
        self.main_area.grid_rowconfigure(0, weight=0) # Header Row
        self.main_area.grid_rowconfigure(1, weight=1) # Main Content

        # --- HEADER ROW (Welcome + Quick Glances) ---
        # Large Clock Card (Spans 2 columns)
        self.card_clock = ClockWeatherWidget(self.main_area)
        self.card_clock.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        
        # System status (Right column)
        self.card_sys = SystemMonitorWidget(self.main_area)
        self.card_sys.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        # --- CONTENT ROW ---
        # Tasks (Left 2 columns)
        self.card_tasks = TaskManagerWidget(self.main_area, self.db)
        self.card_tasks.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        # Notes (Right column)
        self.card_notes = NotesWidget(self.main_area, self.db)
        self.card_notes.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

        # --- BOTTOM ROW (Music + Links) ---
        self.main_area.grid_rowconfigure(2, weight=0)
        
        # Quick Links
        self.card_links = QuickLinksWidget(self.main_area)
        self.card_links.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        # Music (Simple floating bar style)
        self.music_bar = MusicPlayerWidget(self.main_area)
        self.music_bar.grid(row=2, column=2, sticky="ew", padx=10, pady=10)


    def on_closing(self):
        self.db.save()
        self.destroy()

if __name__ == "__main__":
    app = ZenithOS()
    app.mainloop()

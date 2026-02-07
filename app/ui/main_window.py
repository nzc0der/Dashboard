import customtkinter as ctk
import os
from PIL import Image

from app.core import settings
from app.core.data_manager import DataManager
from app.ui.styles import Styles

# Widgets
from app.ui.widgets.top_bar import TopBarWidget
from app.ui.widgets.clock import ClockWidget
from app.ui.widgets.music import MusicPlayerWidget
from app.ui.widgets.system_monitor import SystemMonitorWidget
from app.ui.widgets.tasks import TaskManagerWidget
from app.ui.widgets.notes import NotesWidget
from app.ui.widgets.quick_links import QuickLinksWidget

class ZenithOS(ctk.CTk):
    """
    Main application window for Zenith OS Dashboard.
    coordinates all UI components and services.
    """
    
    def __init__(self):
        super().__init__()

        # --- Base Configuration ---
        self.title(f"{settings.APP_NAME} v{settings.APP_VERSION}")
        self.geometry("1200x800")
        
        # Theme Setup
        ctk.set_appearance_mode(settings.THEME_MODE)
        ctk.set_default_color_theme(settings.COLOR_THEME) # or a custom json path

        # Data Backend
        self.db = DataManager(settings.DATA_FILE)

        # Layout Configuration
        # 2 Columns (Left Sidebar/Main, Right Widgets) ?
        # Or keeping the grid from before?
        
        # Let's try a sophisticated grid
        # Row 0: Top Bar
        # Row 1: Dashboard Content
        # Row 2: Footer
        
        self.grid_rowconfigure(0, weight=0) # Top Bar fixed
        self.grid_rowconfigure(1, weight=1) # Main Content
        self.grid_columnconfigure(0, weight=1)

        # --- 1. Top Bar ---
        self.top_bar = TopBarWidget(self)
        self.top_bar.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

        # --- 2. Main Content Area ---
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        # Configure Main Content Grid
        # Col 0: Quick Info & Clock (Left)
        # Col 1: Workspace (Tasks & Notes) (Center)
        # Col 2: System Status (Right)
        
        self.main_content.grid_columnconfigure(0, weight=1) # Left
        self.main_content.grid_columnconfigure(1, weight=2) # Center (Wider)
        self.main_content.grid_columnconfigure(2, weight=1) # Right
        self.main_content.grid_rowconfigure(0, weight=1)

        # === LEFT PANEL ===
        self.left_panel = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.left_panel.grid_rowconfigure(2, weight=1) # Spacer push up

        # Clock
        self.clock = ClockWidget(self.left_panel)
        self.clock.pack(fill="x", pady=(0, 15))
        
        # Quick Links (Moved to Left Panel for better access)
        self.links = QuickLinksWidget(self.left_panel)
        self.links.pack(fill="x", pady=(0, 15))

        # Music Player
        self.music = MusicPlayerWidget(self.left_panel)
        self.music.pack(fill="x", pady=(0, 15))


        # === CENTER PANEL ===
        self.center_panel = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.center_panel.grid(row=0, column=1, sticky="nsew", padx=10)
        self.center_panel.grid_rowconfigure(0, weight=1)
        self.center_panel.grid_rowconfigure(1, weight=1)
        self.center_panel.grid_columnconfigure(0, weight=1)

        # Tasks
        self.tasks = TaskManagerWidget(self.center_panel, self.db)
        self.tasks.grid(row=0, column=0, sticky="nsew", pady=(0, 10))

        # Notes
        self.notes = NotesWidget(self.center_panel, self.db)
        self.notes.grid(row=1, column=0, sticky="nsew", pady=(10, 0))


        # === RIGHT PANEL ===
        self.right_panel = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.right_panel.grid(row=0, column=2, sticky="nsew", padx=(10, 0))
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(0, weight=1)

        # System Monitor
        self.sys_mon = SystemMonitorWidget(self.right_panel)
        self.sys_mon.pack(fill="both", expand=True)

        # Add a placeholder for future widgets (e.g. Stocks)
        # self.stocks = StockWidget(self.right_panel)
        # self.stocks.pack(...)

        
    def on_closing(self):
        """Handle application shutdown."""
        # Save data
        self.db.save()
        # Destroy
        self.destroy()

if __name__ == "__main__":
    app = ZenithOS()
    app.mainloop()

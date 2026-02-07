import customtkinter as ctk
from app.ui.styles import Styles
from app.ui.widgets.clock import ClockWeatherWidget
from app.ui.widgets.music import MusicPlayerWidget
from app.ui.widgets.system_monitor import SystemMonitorWidget
from app.ui.widgets.tasks import TaskManagerWidget
from app.ui.widgets.notes import NotesWidget
from app.ui.widgets.quick_links import QuickLinksWidget

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent, fg_color="transparent")
        
        # Grid Configuration: Bento Box
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1) # Clock Row
        self.grid_rowconfigure(1, weight=2) # Task/Notes Row
        self.grid_rowconfigure(2, weight=0) # Dock Row

        # --- Row 0 ---
        # Clock Weather (Wider)
        self.clock = ClockWeatherWidget(self)
        self.clock.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=(0, 10), pady=10)
        
        # System Monitor
        self.sys = SystemMonitorWidget(self)
        self.sys.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        # --- Row 1 ---
        # Task List (Tall)
        self.tasks = TaskManagerWidget(self, db)
        self.tasks.grid(row=1, column=0, columnspan=1, sticky="nsew", padx=(0, 10), pady=10)

        # Note Pad (Tall)
        self.notes = NotesWidget(self, db)
        self.notes.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=10, pady=10)

        # --- Row 2 ---
        # Quick Links
        self.links = QuickLinksWidget(self)
        self.links.grid(row=2, column=0, columnspan=2, sticky="ew", padx=(0, 10), pady=10)
        
        # Music Player
        self.music = MusicPlayerWidget(self)
        self.music.grid(row=2, column=2, sticky="ew", padx=10, pady=10)

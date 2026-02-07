import customtkinter as ctk
from app.services.system_service import SystemService
from app.ui.styles import Styles

class SystemMonitorWidget(ctk.CTkFrame):
    """
    Compact System Stats Card.
    """
    def __init__(self, parent):
        # Card style
        super().__init__(parent, **Styles.CARD_CONFIG)
        
        self.stats = SystemService()
        self.stats.add_callback(self.update_ui)
        self.stats.start_polling()
        
        # Header
        self.lbl_title = ctk.CTkLabel(self, text="System Status", font=Styles.FONT_SUBHEADER, text_color=Styles.TEXT_SUB)
        self.lbl_title.pack(pady=(15, 10), padx=15, anchor="w")

        # Grid for gauges
        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(fill="both", expand=True, padx=15, pady=5)
        
        # CPU
        self.cpu_bar = self._create_bar(self.grid_frame, "CPU", "#FF3B30") # Apple Red
        self.cpu_bar.pack(fill="x", pady=5)
        
        # RAM
        self.ram_bar = self._create_bar(self.grid_frame, "RAM", "#30D158") # Apple Green
        self.ram_bar.pack(fill="x", pady=5)
        
        # Disk
        self.disk_bar = self._create_bar(self.grid_frame, "SSD", "#0A84FF") # Apple Blue
        self.disk_bar.pack(fill="x", pady=5)

    def _create_bar(self, parent, label, color):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        
        # Label Row
        lbl_frame = ctk.CTkFrame(frame, fg_color="transparent")
        lbl_frame.pack(fill="x")
        
        ctk.CTkLabel(lbl_frame, text=label, font=Styles.FONT_SMALL, text_color="#8E8E93").pack(side="left")
        percent_lbl = ctk.CTkLabel(lbl_frame, text="0%", font=Styles.FONT_SMALL, text_color="white")
        percent_lbl.pack(side="right")
        
        # Progress Bar
        bar = ctk.CTkProgressBar(frame, height=6, corner_radius=3, progress_color=color, fg_color="#333")
        bar.pack(fill="x", pady=(2, 0))
        bar.set(0)
        
        # Store refs
        frame.percent_lbl = percent_lbl
        frame.bar = bar
        return frame

    def update_ui(self, stats):
        try:
            self.cpu_bar.bar.set(stats["cpu_percent"] / 100)
            self.cpu_bar.percent_lbl.configure(text=f"{int(stats['cpu_percent'])}%")
            
            self.ram_bar.bar.set(stats["ram_percent"] / 100)
            self.ram_bar.percent_lbl.configure(text=f"{int(stats['ram_percent'])}%")
            
            self.disk_bar.bar.set(stats["disk_percent"] / 100)
            self.disk_bar.percent_lbl.configure(text=f"{int(stats['disk_percent'])}%")
        except:
            pass

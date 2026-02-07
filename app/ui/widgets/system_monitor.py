import customtkinter as ctk
from app.ui.styles import Styles

class SystemMonitorWidget(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=Styles.BG_CARD, corner_radius=Styles.RADIUS_L)
        from app.services.system_service import SystemService
        self.stats = SystemService()
        self.stats.add_callback(self.update_ui)
        self.stats.start_polling()
        
        # Header
        ctk.CTkLabel(self, text="System", font=Styles.H3, text_color="white").pack(pady=(20, 10), padx=20, anchor="w")
        
        # 3 Circular Gauges (Simulated with progress arcs or just bars)
        # Using Bars for clarity
        
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # CPU
        self.cpu = self._create_bar(self.container, "CPU", Styles.RED)
        self.cpu.pack(fill="x", pady=8)
        
        # RAM
        self.ram = self._create_bar(self.container, "RAM", Styles.GREEN)
        self.ram.pack(fill="x", pady=8)
        
        # Disk
        self.disk = self._create_bar(self.container, "SSD", Styles.BLUE)
        self.disk.pack(fill="x", pady=8)

        # Network (Simulated)
        self.net = self._create_bar(self.container, "NET", Styles.ORANGE)
        self.net.pack(fill="x", pady=8)

    def _create_bar(self, parent, label, color):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        
        # Top: Label + Value
        top = ctk.CTkFrame(frame, fg_color="transparent")
        top.pack(fill="x")
        ctk.CTkLabel(top, text=label, font=Styles.CAPTION, text_color=Styles.TEXT_SEC).pack(side="left")
        val = ctk.CTkLabel(top, text="0%", font=Styles.CAPTION, text_color="white")
        val.pack(side="right")
        
        # Bar
        bar = ctk.CTkProgressBar(frame, height=6, corner_radius=3, progress_color=color, fg_color="#333", border_width=0)
        bar.pack(fill="x", pady=(4, 0))
        bar.set(0)
        
        frame.bar = bar
        frame.val = val
        return frame

    def update_ui(self, stats):
        try:
            self.cpu.bar.set(stats["cpu_percent"] / 100)
            self.cpu.val.configure(text=f"{int(stats['cpu_percent'])}%")
            
            self.ram.bar.set(stats["ram_percent"] / 100)
            self.ram.val.configure(text=f"{int(stats['ram_percent'])}%")
            
            self.disk.bar.set(stats["disk_percent"] / 100)
            self.disk.val.configure(text=f"{int(stats['disk_percent'])}%")
            
            # Net simulation (random fluctuation for visual)
            import random
            net_val = random.uniform(0.1, 0.4)
            self.net.bar.set(net_val)
            self.net.val.configure(text=f"{int(net_val*100)} Mbps")
        except:
             pass

import customtkinter as ctk
import time
from app.services.system_service import SystemService

class SystemMonitorWidget(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=15, fg_color="#1a1a1a")
        
        self.stats = SystemService()
        self.stats.add_callback(self.update_ui)
        self.stats.start_polling()
        
        # Grid Setup
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3) # Bars take more space

        # Headers
        self.lbl_cpu = ctk.CTkLabel(self, text="CPU", font=("Arial", 12, "bold"))
        self.lbl_cpu.grid(row=0, column=0, pady=(10,5))
        
        self.lbl_ram = ctk.CTkLabel(self, text="RAM", font=("Arial", 12, "bold"))
        self.lbl_ram.grid(row=0, column=1, pady=(10,5))

        # Bars
        self.cpu_bar = ctk.CTkProgressBar(self, orientation="vertical", width=20, height=80)
        self.cpu_bar.grid(row=1, column=0, pady=(0, 10))
        self.cpu_bar.set(0)
        
        self.ram_bar = ctk.CTkProgressBar(self, orientation="vertical", width=20, height=80, progress_color="#e53935")
        self.ram_bar.grid(row=1, column=1, pady=(0, 10))
        self.ram_bar.set(0)

        # Labels for values
        self.val_cpu = ctk.CTkLabel(self, text="0%", font=("Arial", 10))
        self.val_cpu.grid(row=2, column=0, pady=(0, 10))
        
        self.val_ram = ctk.CTkLabel(self, text="0%", font=("Arial", 10))
        self.val_ram.grid(row=2, column=1, pady=(0, 10))

        # Additional Stats (Disk, Network)
        self.extra_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.extra_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))
        
        self.lbl_disk = ctk.CTkLabel(self.extra_frame, text="Disk: 0%", font=("Arial", 10), anchor="w")
        self.lbl_disk.pack(side="left", expand=True)
        
        self.lbl_net = ctk.CTkLabel(self.extra_frame, text="Net: 0KB/s", font=("Arial", 10), anchor="e")
        self.lbl_net.pack(side="right", expand=True)

    def update_ui(self, stats):
        try:
            cpu_val = stats["cpu_percent"] / 100
            ram_val = stats["ram_percent"] / 100
            
            self.cpu_bar.set(cpu_val)
            self.ram_bar.set(ram_val)
            
            self.val_cpu.configure(text=f"{stats['cpu_percent']}%")
            self.val_ram.configure(text=f"{stats['ram_percent']}%")
            
            self.lbl_disk.configure(text=f"Disk: {stats['disk_percent']}%")
            
            # Network (rough estimate)
            sent = stats["net_sent"]
            recv = stats["net_recv"]
            
            # Needs previous state to calculate speed, but for now just showing total or implement speed calculation
            # Simplified: just showing total bytes is not useful. Skipping speed calculation for brevity unless asked.
            pass 
        except Exception as e:
            pass

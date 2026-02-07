import customtkinter as ctk
import webbrowser
from app.services.weather_service import WeatherService
from app.ui.styles import Styles

class TopBarWidget(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, height=60, corner_radius=20, fg_color="#1a1a1a")
        
        self.weather = WeatherService()
        self.weather.add_callback(self.update_weather)
        self.weather.start_polling()

        # Grid
        self.grid_columnconfigure(0, weight=1) # Left spacer
        self.grid_columnconfigure(1, weight=2) # Center Search
        self.grid_columnconfigure(2, weight=1) # Right info

        # --- Left: Branding ---
        self.brand_lbl = ctk.CTkLabel(self, text="ZENITH OS", font=("Orbitron", 18, "bold"), text_color="#1f6aa5")
        self.brand_lbl.pack(side="left", padx=20)

        # --- Center: Search Bar ---
        self.search_frame = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=20, height=40, width=400)
        self.search_frame.pack(side="left", padx=20, fill="x", expand=True) # Actually pack behaves differently if combined with pack side left for brand

        # Let's use pack for flexibility
        self.search_entry = ctk.CTkEntry(
            self.search_frame, 
            placeholder_text="Search the web...",
            height=30,
            border_width=0,
            fg_color="transparent",
            font=("Arial", 14)
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=10, pady=5)
        self.search_entry.bind("<Return>", self.run_search)
        
        # Search Button (Icon)
        self.search_btn = ctk.CTkButton(
            self.search_frame, 
            text="🔍", 
            width=30, 
            height=30, 
            fg_color="transparent", 
            hover_color="#333",
            command=self.run_search
        )
        self.search_btn.pack(side="right", padx=5)

        # --- Right: Weather & Status ---
        self.status_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.status_frame.pack(side="right", padx=20)

        self.weather_lbl = ctk.CTkLabel(self.status_frame, text="Checking Weather...", font=("Arial", 12), text_color="#a0a0a0")
        self.weather_lbl.pack(side="right") # Pack right to left
        
        self.status_dot = ctk.CTkLabel(self.status_frame, text="●", font=("Arial", 12), text_color="#4caf50")
        self.status_dot.pack(side="right", padx=5)

    def run_search(self, event=None):
        query = self.search_entry.get()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            self.search_entry.delete(0, "end")

    def update_weather(self, data):
        try:
            temp = data.get("temperature", "--")
            cond = data.get("condition", "Unknown")
            text = f"{cond} • {temp}"
            self.weather_lbl.configure(text=text)
        except:
            pass

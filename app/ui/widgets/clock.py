import customtkinter as ctk
from datetime import datetime
from app.ui.styles import Styles
from app.services.weather_service import WeatherService

class ClockWeatherWidget(ctk.CTkFrame):
    """
    Combines Clock and Weather into a single premium card.
    Inspired by iOS Lock Screen.
    """
    
    def __init__(self, parent):
        # Merge card style with transparent background for clock area
        super().__init__(parent, fg_color="transparent", corner_radius=0)
        
        self.weather_service = WeatherService()
        self.weather_service.add_callback(self.update_weather)
        self.weather_service.start_polling()

        # Layout: Left (Clock), Right (Weather)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        # Container
        self.container = ctk.CTkFrame(self, **Styles.CARD_CONFIG)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_columnconfigure(0, weight=1)

        # Time (Huge)
        self.time_lbl = ctk.CTkLabel(
            self.container, 
            text="00:00", 
            font=("SF Pro Display", 96, "bold"),
            text_color="white"
        )
        self.time_lbl.pack(pady=(30, 0))

        # Date (Medium)
        self.date_lbl = ctk.CTkLabel(
            self.container, 
            text="Loading Date", 
            font=("SF Pro Text", 24, "bold"),
            text_color="#8E8E93" # Secondary text color
        )
        self.date_lbl.pack(pady=(0, 20))

        # Weather Section (Divider)
        self.weather_frame = ctk.CTkFrame(self.container, fg_color="#2C2C2E", height=60, corner_radius=15)
        self.weather_frame.pack(fill="x", padx=20, pady=20)
        
        self.temp_lbl = ctk.CTkLabel(self.weather_frame, text="--°", font=("SF Pro Display", 24, "bold"), text_color="white")
        self.temp_lbl.pack(side="left", padx=20)

        self.cond_lbl = ctk.CTkLabel(self.weather_frame, text="Loading...", font=("SF Pro Text", 16), text_color="#D1D1D6")
        self.cond_lbl.pack(side="right", padx=20)

        self.update_clock()

    def update_clock(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M") # 24h format looks cleaner usually, or "%I:%M"
        current_date = now.strftime("%A, %B %d")
        
        if self.time_lbl.cget("text") != current_time:
            self.time_lbl.configure(text=current_time)
        if self.date_lbl.cget("text") != current_date:
            self.date_lbl.configure(text=current_date)
            
        self.after(1000, self.update_clock)

    def update_weather(self, data):
        try:
            temp = data.get("temperature", "--")
            cond = data.get("condition", "Unknown")
            self.temp_lbl.configure(text=temp)
            self.cond_lbl.configure(text=cond)
        except:
            pass

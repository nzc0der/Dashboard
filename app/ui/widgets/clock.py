import customtkinter as ctk
from datetime import datetime
from app.ui.styles import Styles
from app.services.weather_service import WeatherService

class ClockWeatherWidget(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=Styles.BG_CARD, corner_radius=Styles.RADIUS_L)
        
        self.weather_service = WeatherService()
        self.weather_service.add_callback(self.update_weather)
        self.weather_service.start_polling()

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left: Huge Clock
        self.clock_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.clock_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
        
        self.time_lbl = ctk.CTkLabel(
            self.clock_frame, 
            text="00:00", 
            font=("SF Pro Display", 110, "bold"),
            text_color="white",
            anchor="w"
        )
        self.time_lbl.pack(anchor="w")
        
        self.date_lbl = ctk.CTkLabel(
            self.clock_frame, 
            text="Monday, January 1", 
            font=("SF Pro Display", 28, "bold"),
            text_color=Styles.TEXT_SEC, # Grey
            anchor="w"
        )
        self.date_lbl.pack(anchor="w", pady=(5, 0))

        # Right: Weather
        self.weather_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.weather_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        
        # Weather Icon (Emoji for now, could be image)
        self.weather_icon = ctk.CTkLabel(
            self.weather_frame, 
            text="☁️", 
            font=("Apple Color Emoji", 80), # Use Apple Emoji font
            anchor="e"
        )
        self.weather_icon.pack(side="top", anchor="e")
        
        self.temp_lbl = ctk.CTkLabel(
            self.weather_frame, 
            text="--°", 
            font=("SF Pro Display", 48, "bold"),
            text_color="white",
            anchor="e"
        )
        self.temp_lbl.pack(side="top", anchor="e")
        
        self.cond_lbl = ctk.CTkLabel(
            self.weather_frame, 
            text="Loading...", 
            font=("SF Pro Display", 20),
            text_color=Styles.TEXT_SEC,
            anchor="e"
        )
        self.cond_lbl.pack(side="top", anchor="e")

        self.update_clock()

    def update_clock(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M")
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
            
            # Map condition to emoji
            icon = "🌤️"
            c = cond.lower()
            if "rain" in c: icon = "🌧️"
            elif "cloud" in c: icon = "☁️"
            elif "sun" in c or "clear" in c: icon = "☀️"
            elif "snow" in c: icon = "❄️"
            elif "thunder" in c: icon = "⛈️"
            
            self.temp_lbl.configure(text=temp)
            self.cond_lbl.configure(text=cond)
            self.weather_icon.configure(text=icon)
        except:
            pass

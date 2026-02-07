import urllib.request
import json
import threading
import time
from datetime import datetime, timedelta
from app.core import settings


class WeatherService:
    """
    Fetches weather data from Open-Meteo API.
    Does not require an API key.
    Runs asynchronously to prevent UI blocking.
    """
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    def __init__(self, lat=settings.WEATHER_LAT, lon=settings.WEATHER_LON):
        self.lat = lat
        self.lon = lon
        self.current_weather = {
            "temperature": "--",
            "condition": "Loading...",
            "wind_speed": "--",
            "humidity": "--",
            "last_updated": None
        }
        self.running = False
        self.update_interval = 600 # 10 minutes
        self.callbacks = []

    def set_location(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.fetch_now()

    def add_callback(self, func):
        """Register a function to be called when weather updates."""
        self.callbacks.append(func)

    def start_polling(self):
        """Starts the background thread for weather updates."""
        if not self.running:
            self.running = True
            thread = threading.Thread(target=self._poll_loop, daemon=True)
            thread.start()

    def fetch_now(self):
        """Force an immediate update."""
        threading.Thread(target=self._fetch_data, daemon=True).start()

    def _poll_loop(self):
        while self.running:
            self._fetch_data()
            time.sleep(self.update_interval)

    def _fetch_data(self):
        try:
            url = f"{self.BASE_URL}?latitude={self.lat}&longitude={self.lon}&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"
            
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'ZenithOS/2.0'}
            )
            
            import ssl
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    self._process_data(data)
                else:
                    print(f"[WeatherService] API Returned status: {response.status}")
                    
        except Exception as e:
            print(f"[WeatherService] Error fetching weather: {e}")
            self.current_weather["condition"] = "Offline"
            self._notify()

    def _process_data(self, data):
        if "current_weather" in data:
            cw = data["current_weather"]
            temp = cw.get("temperature")
            wind = cw.get("windspeed")
            code = cw.get("weathercode")
            
            condition = self._get_condition_text(code)
            
            self.current_weather = {
                "temperature": f"{temp}°C",
                "condition": condition,
                "wind_speed": f"{wind} km/h",
                "humidity": "N/A", # api simple vs detailed
                "last_updated": datetime.now().strftime("%H:%M")
            }
            self._notify()

    def _notify(self):
        """Update all registered listeners."""
        for func in self.callbacks:
            try:
                func(self.current_weather)
            except Exception as e:
                print(f"[WeatherService] Callback error: {e}")

    def _get_condition_text(self, code):
        """Maps WMO weather codes to human readable text."""
        # WMO Weather interpretation codes (WW)
        if code == 0: return "Clear Sky"
        if code in [1, 2, 3]: return "Partly Cloudy"
        if code in [45, 48]: return "Foggy"
        if code in [51, 53, 55]: return "Drizzle"
        if code in [61, 63, 65]: return "Rain"
        if code in [71, 73, 75]: return "Snow"
        if code in [80, 81, 82]: return "Rain Showers"
        if code in [95, 96, 99]: return "Thunderstorm"
        return "Unknown"

"""Weather service for fetching and managing weather data."""

import certifi
import json
import logging
import ssl
import threading
import time
import urllib.error
import urllib.request
from datetime import datetime
from typing import Callable, Dict, Any, Optional, List

from app.core import settings

# Configure logging
logger = logging.getLogger(__name__)


class WeatherService:
    """
    Fetches weather data from Open-Meteo API.
    Does not require an API key.
    Runs asynchronously to prevent UI blocking.
    
    Attributes:
        lat (float): Latitude for weather location
        lon (float): Longitude for weather location
        current_weather (Dict[str, Any]): Current weather data
        running (bool): Whether the polling thread is active
        update_interval (int): Seconds between updates
    """
    
    BASE_URL: str = "https://api.open-meteo.com/v1/forecast"
    DEFAULT_TIMEOUT: int = 10
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 2  # seconds
    
    def __init__(
        self, 
        lat: float = settings.WEATHER_LAT, 
        lon: float = settings.WEATHER_LON
    ) -> None:
        """Initialize the weather service.
        
        Args:
            lat: Latitude for weather location
            lon: Longitude for weather location
        """
        self.lat: float = lat
        self.lon: float = lon
        self.current_weather: Dict[str, Any] = {
            "temperature": "--",
            "condition": "Loading...",
            "wind_speed": "--",
            "humidity": "--",
            "last_updated": None
        }
        self.running: bool = False
        self.update_interval: int = 600  # 10 minutes
        self.callbacks: List[Callable[[Dict[str, Any]], None]] = []
        
        # Thread safety
        self._lock = threading.Lock()
        self._poll_thread: Optional[threading.Thread] = None

    def set_location(self, lat: float, lon: float) -> None:
        """Update the weather location and fetch new data.
        
        Args:
            lat: New latitude
            lon: New longitude
        """
        with self._lock:
            self.lat = lat
            self.lon = lon
        self.fetch_now()

    def add_callback(self, func: Callable[[Dict[str, Any]], None]) -> None:
        """Register a function to be called when weather updates.
        
        Args:
            func: Callback function that accepts weather data dict
        """
        with self._lock:
            self.callbacks.append(func)
        logger.debug(f"Added weather callback: {func.__name__}")

    def remove_callback(self, func: Callable[[Dict[str, Any]], None]) -> None:
        """Unregister a callback function.
        
        Args:
            func: Callback function to remove
        """
        with self._lock:
            if func in self.callbacks:
                self.callbacks.remove(func)
                logger.debug(f"Removed weather callback: {func.__name__}")

    def start_polling(self) -> None:
        """Starts the background thread for weather updates."""
        if not self.running:
            self.running = True
            self._poll_thread = threading.Thread(
                target=self._poll_loop, 
                daemon=True,
                name="WeatherPollingThread"
            )
            self._poll_thread.start()
            logger.info("Weather polling started")

    def stop_polling(self) -> None:
        """Stops the background polling thread."""
        if self.running:
            self.running = False
            logger.info("Weather polling stopped")

    def fetch_now(self) -> None:
        """Force an immediate weather update in a background thread."""
        thread = threading.Thread(
            target=self._fetch_data, 
            daemon=True,
            name="WeatherFetchThread"
        )
        thread.start()
        logger.debug("Immediate weather fetch triggered")

    def get_current_weather(self) -> Dict[str, Any]:
        """Get a thread-safe copy of current weather data.
        
        Returns:
            Dictionary containing current weather information
        """
        with self._lock:
            return self.current_weather.copy()

    def _poll_loop(self) -> None:
        """Main polling loop that runs in background thread."""
        # Fetch immediately on start
        self._fetch_data()
        
        while self.running:
            time.sleep(self.update_interval)
            if self.running:  # Check again in case stopped during sleep
                self._fetch_data()

    def _fetch_data(self) -> None:
        """Fetch weather data from API with retry logic."""
        for attempt in range(self.MAX_RETRIES):
            try:
                data = self._make_api_request()
                self._process_data(data)
                return  # Success, exit retry loop
                
            except urllib.error.HTTPError as e:
                logger.warning(
                    f"HTTP error fetching weather (attempt {attempt + 1}/{self.MAX_RETRIES}): "
                    f"{e.code} - {e.reason}"
                )
                
            except urllib.error.URLError as e:
                logger.warning(
                    f"Network error fetching weather (attempt {attempt + 1}/{self.MAX_RETRIES}): {e.reason}"
                )
                
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON response from weather API: {e}")
                break  # Don't retry on JSON errors
                
            except Exception as e:
                logger.error(f"Unexpected error fetching weather: {e}", exc_info=True)
                
            # Wait before retrying (exponential backoff)
            if attempt < self.MAX_RETRIES - 1:
                delay = self.RETRY_DELAY * (2 ** attempt)
                time.sleep(delay)
        
        # All retries failed
        self._set_offline_status()

    def _make_api_request(self) -> Dict[str, Any]:
        """Make the actual HTTP request to the weather API.
        
        Returns:
            Parsed JSON response from API
            
        Raises:
            urllib.error.HTTPError: On HTTP errors
            urllib.error.URLError: On network errors
            json.JSONDecodeError: On invalid JSON response
        """
        with self._lock:
            lat, lon = self.lat, self.lon
        
        url = (
            f"{self.BASE_URL}"
            f"?latitude={lat}"
            f"&longitude={lon}"
            f"&current_weather=true"
            f"&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"
        )
        
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Dashboard/2.0',
                'Accept': 'application/json'
            }
        )
        
        # Use certifi's CA bundle for SSL verification
        ctx = ssl.create_default_context(cafile=certifi.where())
        
        with urllib.request.urlopen(req, context=ctx, timeout=self.DEFAULT_TIMEOUT) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                logger.debug(f"Weather data fetched successfully for ({lat}, {lon})")
                return data
            else:
                raise urllib.error.HTTPError(
                    url, response.status, f"Unexpected status: {response.status}", 
                    response.headers, None
                )

    def _process_data(self, data: Dict[str, Any]) -> None:
        """Process API response and update current weather.
        
        Args:
            data: Parsed JSON response from weather API
        """
        if "current_weather" not in data:
            logger.warning("API response missing 'current_weather' field")
            return
            
        cw = data["current_weather"]
        temp = cw.get("temperature")
        wind = cw.get("windspeed")
        code = cw.get("weathercode")
        
        if temp is None or wind is None or code is None:
            logger.warning("Incomplete weather data received")
            return
        
        condition = self._get_condition_text(code)
        
        # Extract humidity from hourly data if available
        humidity = "N/A"
        if "hourly" in data and "relativehumidity_2m" in data["hourly"]:
            hourly_humidity = data["hourly"]["relativehumidity_2m"]
            if hourly_humidity and len(hourly_humidity) > 0:
                humidity = f"{hourly_humidity[0]}%"
        
        weather_data = {
            "temperature": f"{temp}°C",
            "condition": condition,
            "wind_speed": f"{wind} km/h",
            "humidity": humidity,
            "last_updated": datetime.now().strftime("%H:%M")
        }
        
        with self._lock:
            self.current_weather = weather_data
        
        self._notify()
        logger.info(f"Weather updated: {temp}°C, {condition}")

    def _set_offline_status(self) -> None:
        """Update weather status to offline after failed fetches."""
        with self._lock:
            self.current_weather["condition"] = "Offline"
        self._notify()
        logger.error("Weather service is offline")

    def _notify(self) -> None:
        """Notify all registered callbacks with updated weather data."""
        with self._lock:
            weather_data = self.current_weather.copy()
            callbacks = self.callbacks.copy()
        
        for func in callbacks:
            try:
                func(weather_data)
            except Exception as e:
                logger.error(f"Error in weather callback {func.__name__}: {e}", exc_info=True)

    def _get_condition_text(self, code: int) -> str:
        """Maps WMO weather codes to human readable text.
        
        Args:
            code: WMO weather code
            
        Returns:
            Human-readable weather condition string
        """
        # WMO Weather interpretation codes (WW)
        condition_map = {
            0: "Clear Sky",
            1: "Partly Cloudy", 2: "Partly Cloudy", 3: "Partly Cloudy",
            45: "Foggy", 48: "Foggy",
            51: "Drizzle", 53: "Drizzle", 55: "Drizzle",
            61: "Rain", 63: "Rain", 65: "Rain",
            71: "Snow", 73: "Snow", 75: "Snow",
            80: "Rain Showers", 81: "Rain Showers", 82: "Rain Showers",
            95: "Thunderstorm", 96: "Thunderstorm", 99: "Thunderstorm"
        }
        
        return condition_map.get(code, f"Unknown ({code})")

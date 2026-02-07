import os

# Application Settings
APP_NAME = "Zenith OS"
APP_VERSION = "2.0.0"
APP_AUTHOR = "Commander"

# Path configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_FILE = os.path.join(BASE_DIR, "titanium_data.json")

# Theme configuration
THEME_MODE = "Dark"
COLOR_THEME = "blue"

# UI Constants
FONT_FAMILY = "Roboto"
FONT_SIZE_SMALL = 12
FONT_SIZE_REGULAR = 14
FONT_SIZE_LARGE = 18
FONT_SIZE_XLARGE = 24
FONT_SIZE_XXLARGE = 48


COLOR_PRIMARY = "#0A84FF" # iOS Blue
COLOR_SECONDARY = "#1C1C1E" # Apple Dark Gray (Cards)
COLOR_BACKGROUND = "#000000" # Pure Black (OLED)
COLOR_TEXT_PRIMARY = "#FFFFFF"
COLOR_TEXT_SECONDARY = "#8E8E93" # iOS Gray Text
COLOR_ACCENT = "#30D158" # iOS Green
COLOR_Success = "#30D158"
COLOR_WARNING = "#FFD60A"
COLOR_BORDER = "#38383A" # Subtle border for glass effect

# Features
ENABLE_SPOTIFY = True
ENABLE_WEATHER = True
ENABLE_SYSTEM_MONITOR = True

# Weather Location (Ormond, Melbourne)
WEATHER_LAT = -37.9038
WEATHER_LON = 145.0396

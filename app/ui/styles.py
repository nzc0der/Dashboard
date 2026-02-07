from app.core import settings

class Styles:
    """
    Ultra-Premium Design System.
    """
    
    # --- Palette ---
    # Backgrounds
    BG_APP = "#000000"       # OLED Black
    BG_SIDEBAR = "#09090b"   # Zinc-950
    BG_CARD = "#121212"      # Surface 1 (Material) / Zinc-900
    BG_CARD_HOVER = "#1E1E1E"
    
    # Accents (Apple Human Interface Guidelines)
    BLUE = "#007AFF"
    GREEN = "#34C759"
    INDIGO = "#5856D6"
    ORANGE = "#FF9500"
    PINK = "#FF2D55"
    PURPLE = "#AF52DE"
    RED = "#FF3B30"
    TEAL = "#5AC8FA"
    YELLOW = "#FFCC00"
    
    # Text
    TEXT_MAIN = "#FFFFFF"
    TEXT_SEC = "#8E8E93" # Zinc-500
    TEXT_TER = "#48484A" # Zinc-700
    
    # Borders
    BORDER_COLOR = "#27272A" # Zinc-800
    
    # --- Tokens ---
    RADIUS_S = 8
    RADIUS_M = 16
    RADIUS_L = 24
    RADIUS_XL = 32
    
    FONT_FAMILY = "SF Pro Display" # Fallback handled by system usually, or Arial
    
    # Fonts
    H1 = (FONT_FAMILY, 32, "bold")
    H2 = (FONT_FAMILY, 24, "bold")
    H3 = (FONT_FAMILY, 18, "bold")
    BODY = (FONT_FAMILY, 14)
    CAPTION = (FONT_FAMILY, 12)
    MONO = ("JetBrains Mono", 13)

    # --- Component Configs ---
    
    CARD = {
        "fg_color": BG_CARD,
        "corner_radius": RADIUS_L,
        "border_width": 1,
        "border_color": BORDER_COLOR
    }
    
    BUTTON_ICON = {
        "fg_color": "transparent",
        "text_color": TEXT_SEC,
        "hover_color": "#27272A",
        "corner_radius": RADIUS_M,
        "width": 50,
        "height": 50,
        "font": (FONT_FAMILY, 20)
    }

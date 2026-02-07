from app.core import settings

class Styles:
    """
    Ultra-Premium Design System.
    Inspired by Apple Human Interface Guidelines & Modern Glassmorphism.
    """
    
    # --- Palette ---
    
    # Backgrounds
    BG_APP = "#000000"       # Pure Black (OLED)
    BG_SIDEBAR = "#000000"   # Blend with App BG
    
    # Cards (Surface Colors)
    # Using slightly lighter shades for depth
    BG_CARD = "#141414"      # Slightly off-black
    BG_CARD_HOVER = "#1C1C1E" # Lighter interaction state
    BG_INPUT = "#1C1C1E"
    
    # Accents (Vibrant & Neon)
    PRIMARY = "#0A84FF"      # iOS Blue
    PRIMARY_HOVER = "#0071E3"
    
    SECONDARY = "#30D158"    # iOS Green
    DANGER = "#FF453A"       # iOS Red
    WARNING = "#FFD60A"      # iOS Yellow
    
    # Gradients (Simulated via solid accents for now)
    ACCENT_1 = "#BF5AF2"     # Purple
    ACCENT_2 = "#5E5CE6"     # Indigo
    
    # Text
    TEXT_MAIN = "#FFFFFF"            # White
    TEXT_SEC = "#8E8E93"             # Secondary Label (Grey)
    TEXT_TER = "#48484A"             # Tertiary Label (Darker Grey)
    TEXT_HIGHLIGHT = "#64D2FF"       # Light Blue
    
    # Borders
    BORDER_COLOR = "#222222"         # Very subtle border
    BORDER_FOCUS = "#333333"
    
    # --- Tokens ---
    
    # Corner Radius (Generous for modern feel)
    RADIUS_S = 10
    RADIUS_M = 18
    RADIUS_L = 28
    RADIUS_XL = 40
    
    # Fonts
    # Prefer System Fonts that look good on Mac
    FONT_FAMILY = "SF Pro Display" 
    FONT_MONO = "SF Mono"

    # Font Presets
    H1 = (FONT_FAMILY, 36, "bold")
    H2 = (FONT_FAMILY, 28, "bold")
    H3 = (FONT_FAMILY, 22, "bold")
    BODY = (FONT_FAMILY, 15)
    BODY_BOLD = (FONT_FAMILY, 15, "bold")
    CAPTION = (FONT_FAMILY, 13)
    MONO = (FONT_MONO, 13)

    # --- Component Configs ---
    
    # Standard Card
    CARD = {
        "fg_color": BG_CARD,
        "corner_radius": RADIUS_L,
        "border_width": 1,
        "border_color": BORDER_COLOR
    }
    
    # Highlighted Card (Active)
    CARD_ACTIVE = {
        "fg_color": "#1A1A1A",
        "corner_radius": RADIUS_L,
        "border_width": 1,
        "border_color": "#333333"
    }

    # Sidebar Button
    SIDEBAR_BTN = {
        "fg_color": "transparent",
        "text_color": TEXT_SEC,
        "hover_color": "#1A1A1A",
        "corner_radius": RADIUS_M,
        "width": 50,
        "height": 50,
        "font": (FONT_FAMILY, 22)
    }

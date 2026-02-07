from app.core import settings

class Styles:
    """
    Apple/Samsung inspired design system.
    Focus on hierarchy, whitespace, and rounded corners.
    """
    
    # Colors
    BACKGROUND = settings.COLOR_BACKGROUND
    CARD_BG = settings.COLOR_SECONDARY
    PRIMARY = settings.COLOR_PRIMARY
    TEXT_MAIN = settings.COLOR_TEXT_PRIMARY
    TEXT_SUB = settings.COLOR_TEXT_SECONDARY
    BORDER = settings.COLOR_BORDER
    ACCENT = settings.COLOR_ACCENT
    WARNING = settings.COLOR_WARNING
    
    # Dimensions
    CORNER_RADIUS = 24  # Large radius (Apple style)
    PADDING_SMALL = 8
    PADDING_MEDIUM = 16
    PADDING_LARGE = 24
    
    # Fonts (San Francisco / Roboto style)
    FONT_FAMILY = "SF Pro Display" if "SF Pro Display" else "Arial" # Fallback
    
    FONT_CLOCK_HUGE = (FONT_FAMILY, 82, "bold")
    FONT_CLOCK_DATE = (FONT_FAMILY, 18, "bold")
    
    FONT_HEADER = (FONT_FAMILY, 22, "bold")
    FONT_SUBHEADER = (FONT_FAMILY, 14, "bold")
    FONT_BODY = (FONT_FAMILY, 14)
    FONT_SMALL = (FONT_FAMILY, 12)
    
    # Widget Configurations
    
    # "Glass" Card Style
    CARD_CONFIG = {
        "corner_radius": CORNER_RADIUS,
        "fg_color": CARD_BG,
        "border_width": 1, 
        "border_color": BORDER
    }
    
    BUTTON_PRIMARY = {
        "corner_radius": 20,
        "fg_color": PRIMARY,
        "hover_color": "#007AFF", # Slightly lighter blue
        "text_color": "white",
        "font": (FONT_FAMILY, 14, "bold"),
        "height": 40
    }

    BUTTON_GHOST = {
        "corner_radius": 20,
        "fg_color": "transparent",
        "hover_color": "#2C2C2E",
        "text_color": PRIMARY,
        "font": (FONT_FAMILY, 14),
        "height": 40
    }

    ENTRY_CONFIG = {
        "corner_radius": 12,
        "fg_color": "#2C2C2E", # Search field grey
        "border_width": 0,
        "text_color": "white",
        "placeholder_text_color": "#636366",
        "font": (FONT_FAMILY, 14)
    }

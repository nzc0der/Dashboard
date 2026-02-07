import customtkinter as ctk
import subprocess
import os
from app.ui.styles import Styles
from datetime import datetime

class QuickActionsWidget(ctk.CTkFrame):
    """
    Quick Actions Dock - macOS system shortcuts and utilities
    """
    def __init__(self, parent):
        super().__init__(parent, fg_color=Styles.BG_CARD, corner_radius=Styles.RADIUS_L)
        
        self.pack_propagate(False)
        
        # Quick actions with icons (using emoji for now, can be replaced with actual icons)
        self.actions = [
            ("Calculator", "🧮", self.open_calculator, "#FF9500"),
            ("Terminal", "⌨️", self.open_terminal, "#34C759"),
            ("Screenshot", "📸", self.take_screenshot, "#5856D6"),
            ("Finder", "📁", self.open_finder, "#007AFF"),
            ("Safari", "🧭", self.open_safari, "#006CFF"),
            ("Notes", "📝", self.open_notes_app, "#FFD60A"),
            ("Settings", "⚙️", self.open_system_settings, "#8E8E93")
        ]
        
        # Horizontal container
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True, fill="both", padx=20, pady=15)
        
        # Center the buttons
        self.button_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.button_frame.pack(expand=True)
        
        for name, icon, command, color in self.actions:
            btn_container = ctk.CTkFrame(self.button_frame, fg_color="transparent")
            btn_container.pack(side="left", padx=8, pady=5)
            
            # Icon button
            btn = ctk.CTkButton(
                btn_container,
                text=icon,
                width=60,
                height=60,
                corner_radius=16,
                fg_color=color,
                hover_color=self._darken_color(color),
                font=("SF Pro Display", 32),
                command=command
            )
            btn.pack()
            
            # Label below
            label = ctk.CTkLabel(
                btn_container,
                text=name,
                font=("SF Pro Display", 11),
                text_color=Styles.TEXT_SEC
            )
            label.pack(pady=(4, 0))
    
    def _darken_color(self, hex_color):
        """Darken a hex color slightly for hover effect"""
        # Remove # and convert to RGB
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Darken by 20%
        r = int(r * 0.8)
        g = int(g * 0.8)
        b = int(b * 0.8)
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def open_calculator(self):
        """Open macOS Calculator app"""
        try:
            subprocess.Popen(["open", "-a", "Calculator"])
        except Exception as e:
            print(f"Failed to open Calculator: {e}")
    
    def open_terminal(self):
        """Open macOS Terminal app"""
        try:
            subprocess.Popen(["open", "-a", "Terminal"])
        except Exception as e:
            print(f"Failed to open Terminal: {e}")
    
    def take_screenshot(self):
        """Take a screenshot using macOS screencapture"""
        try:
            # Interactive screenshot (click to select area)
            subprocess.Popen(["screencapture", "-i"])
        except Exception as e:
            print(f"Failed to take screenshot: {e}")
    
    def open_finder(self):
        """Open Finder"""
        try:
            subprocess.Popen(["open", "-a", "Finder"])
        except Exception as e:
            print(f"Failed to open Finder: {e}")
    
    def open_safari(self):
        """Open Safari browser"""
        try:
            subprocess.Popen(["open", "-a", "Safari"])
        except Exception as e:
            print(f"Failed to open Safari: {e}")
    
    def open_notes_app(self):
        """Open macOS Notes app"""
        try:
            subprocess.Popen(["open", "-a", "Notes"])
        except Exception as e:
            print(f"Failed to open Notes: {e}")
    
    def open_system_settings(self):
        """Open System Settings/Preferences"""
        try:
            # Try macOS Ventura+ first, then fall back to older versions
            subprocess.Popen(["open", "-a", "System Settings"])
        except:
            try:
                subprocess.Popen(["open", "-a", "System Preferences"])
            except Exception as e:
                print(f"Failed to open System Settings: {e}")

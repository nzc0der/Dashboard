import customtkinter as ctk
import threading
import time
from app.services.spotify_service import SpotifyService
from app.ui.styles import Styles

class MusicPlayerWidget(ctk.CTkFrame):
    """
    Minimalist Music Bar.
    Looks like a dynamic island or floating pill.
    """
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self.spotify = SpotifyService()
        self.spotify.add_callback(self.update_ui)
        self.spotify.start_polling()
        
        # Pill Container
        self.container = ctk.CTkFrame(
            self, 
            corner_radius=30, 
            # fg_color="#1C1C1E", # Dark Apple
            fg_color="#0A0A0A", # Even darker for contrast
            border_width=1,
            border_color="#333"
        )
        self.container.pack(fill="x", expand=True, padx=10, pady=5)
        
        # Art Proxy (Circle)
        self.art_placeholder = ctk.CTkButton(
            self.container, 
            text="♫", 
            width=40, height=40, 
            corner_radius=20, 
            fg_color="#333", 
            hover=False,
            font=("SF Pro Text", 18)
        )
        self.art_placeholder.pack(side="left", padx=15, pady=10)

        # Info Stack
        self.info_stack = ctk.CTkFrame(self.container, fg_color="transparent")
        self.info_stack.pack(side="left", fill="both", expand=True, pady=10)
        
        self.title_lbl = ctk.CTkLabel(
            self.info_stack, 
            text="Waiting for Music...", 
            font=("SF Pro Display", 14, "bold"), 
            anchor="w"
        )
        self.title_lbl.pack(fill="x")
        
        self.artist_lbl = ctk.CTkLabel(
            self.info_stack, 
            text="Spotify Integration", 
            font=("SF Pro Text", 12), 
            text_color="gray", 
            anchor="w"
        )
        self.artist_lbl.pack(fill="x")

        # Controls (Minimal Icons)
        self.controls = ctk.CTkFrame(self.container, fg_color="transparent")
        self.controls.pack(side="right", padx=15)
        
        self.btn_prev = self._make_control_btn("⏮", self.spotify.prev_track)
        self.btn_play = self._make_control_btn("▶", self.spotify.play_pause, size=34, highlight=True)
        self.btn_next = self._make_control_btn("⏭", self.spotify.next_track)

        # Progress Bar (Thin line at bottom of pill)
        self.progress = ctk.CTkProgressBar(
            self.container, 
            height=3, 
            progress_color=Styles.PRIMARY, 
            fg_color="#222",
            border_width=0
        )
        self.progress.place(relx=0, rely=0.95, relwidth=1, anchor="sw")
        self.progress.set(0)

        self.start_progress_update()

    def _make_control_btn(self, text, cmd, size=28, highlight=False):
        color = "transparent"
        hover = "#333"
        txt_color = "white"
        
        if highlight:
            color = Styles.PRIMARY
            hover = "#007AFF"
            
        btn = ctk.CTkButton(
            self.controls, 
            text=text, 
            width=size, height=size, 
            corner_radius=size/2,
            fg_color=color,
            hover_color=hover,
            text_color=txt_color,
            command=cmd,
            font=("Arial", 14)
        )
        btn.pack(side="left", padx=4)
        return btn

    def update_ui(self, track):
        try:
            title = track["title"]
            artist = track["artist"]
            
            # Marquee effect simulation (truncate)
            if len(title) > 25: title = title[:25] + "..."
            if len(artist) > 30: artist = artist[:30] + "..."
            
            self.title_lbl.configure(text=title)
            self.artist_lbl.configure(text=artist)
            
            icon = "||" if track["playing"] else "▶"
            if self.btn_play.cget("text") != icon:
                self.btn_play.configure(text=icon)
            
            dur = track["duration"]
            pos = track["position"]
            if dur > 0:
                self.progress.set(pos/dur)
        except:
            pass

    def start_progress_update(self):
        self.after(1000, self.start_progress_update)

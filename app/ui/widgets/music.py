import customtkinter as ctk
import threading
import time
from app.services.spotify_service import SpotifyService

class MusicPlayerWidget(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=15, fg_color="#2b2b2b")
        
        self.spotify = SpotifyService()
        self.spotify.add_callback(self.update_ui)
        
        # Grid layout
        self.grid_columnconfigure(0, weight=0) # Art
        self.grid_columnconfigure(1, weight=1) # Info
        self.grid_columnconfigure(2, weight=0) # Controls
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=0)

        # 1. Album Art Placeholder (or fetch later)
        self.art = ctk.CTkButton(
            self, text="♪", width=70, height=70, 
            corner_radius=10, fg_color="#444", hover=False,
            font=("Arial", 32)
        )
        self.art.grid(row=0, column=0, rowspan=2, padx=15, pady=15, sticky="w")

        # 2. Song Info
        self.info_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.info_frame.grid(row=0, column=1, columnspan=2, sticky="ew", padx=(0,15), pady=(15,0))
        
        self.title_lbl = ctk.CTkLabel(self.info_frame, text="Loading...", font=("Arial", 16, "bold"), anchor="w")
        self.title_lbl.pack(fill="x")
        
        self.artist_lbl = ctk.CTkLabel(self.info_frame, text="Spotify Service", font=("Arial", 13), text_color="gray", anchor="w")
        self.artist_lbl.pack(fill="x")

        # 3. Controls
        self.controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.controls_frame.grid(row=1, column=1, columnspan=2, sticky="ew", padx=(0,15), pady=(5,10))
        
        self.btn_prev = ctk.CTkButton(self.controls_frame, text="⏮", width=40, height=30, command=self.spotify.prev_track)
        self.btn_prev.pack(side="left", padx=5)
        
        self.btn_play = ctk.CTkButton(self.controls_frame, text="▶", width=50, height=40, fg_color="#1f6aa5", command=self.spotify.play_pause)
        self.btn_play.pack(side="left", padx=5)
        
        self.btn_next = ctk.CTkButton(self.controls_frame, text="⏭", width=40, height=30, command=self.spotify.next_track)
        self.btn_next.pack(side="left", padx=5)
        
        # 4. Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self, height=6, progress_color="#1f6aa5")
        self.progress_bar.grid(row=2, column=0, columnspan=3, sticky="ew", padx=15, pady=(0, 15))
        self.progress_bar.set(0)

        # Update loop for smooth progress bar if possible
        self.start_progress_update()
        
        # Start Service
        self.spotify.start_polling()

    def update_ui(self, track_info):
        # Update labels safely
        try:
            self.title_lbl.configure(text=track_info["title"][:30]) # Truncate if too long
            self.artist_lbl.configure(text=f"{track_info['artist']} • {track_info['album']}")
            
            icon = "||" if track_info["playing"] else "▶"
            if self.btn_play.cget("text") != icon:
                self.btn_play.configure(text=icon)
            
            # Progress update logic handled separately for smoothness, but sync here too
            duration = track_info["duration"]
            position = track_info["position"]
            if duration > 0:
                self.progress_bar.set(position / duration)
        except Exception as e:
            print(f"UI Update Error: {e}")

    def start_progress_update(self):
        # Simulate smooth progress locally
        self.after(1000, self.start_progress_update)
        # Real updates happen via callback from service

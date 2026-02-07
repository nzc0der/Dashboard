import customtkinter as ctk
import threading
import time
import urllib.request
from io import BytesIO
from PIL import Image, ImageOps, ImageFilter
from app.services.spotify_service import SpotifyService
from app.ui.styles import Styles

class MusicPlayerWidget(ctk.CTkFrame):
    """
    Advanced Music Player Card.
    Displays Album Art, Blurred Background (simulated), and Controls.
    """
    def __init__(self, parent):
        super().__init__(parent, fg_color=Styles.BG_CARD, corner_radius=Styles.RADIUS_L, border_width=1, border_color="#333")
        
        self.spotify = SpotifyService()
        self.spotify.add_callback(self.update_ui)
        self.last_art_url = None
        self.default_image = self._create_placeholder_image()
        
        # Layout
        self.grid_columnconfigure(0, weight=0) # Art
        self.grid_columnconfigure(1, weight=1) # Info
        self.grid_columnconfigure(2, weight=0) # Controls
        self.grid_rowconfigure(0, weight=1)

        # 1. Album Art
        self.art_label = ctk.CTkLabel(self, text="", image=self.default_image)
        self.art_label.grid(row=0, column=0, rowspan=2, padx=15, pady=15)

        # 2. Info Stack
        self.info_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.info_frame.grid(row=0, column=1, sticky="w", padx=(0, 10), pady=(20, 0))
        
        self.title_lbl = ctk.CTkLabel(
            self.info_frame, 
            text="Not Playing", 
            font=("SF Pro Display", 18, "bold"), 
            anchor="w",
            text_color="white"
        )
        self.title_lbl.pack(fill="x")
        
        self.artist_lbl = ctk.CTkLabel(
            self.info_frame, 
            text="Spotify", 
            font=("SF Pro Text", 14), 
            text_color="#8E8E93", 
            anchor="w"
        )
        self.artist_lbl.pack(fill="x")

        # 3. Controls (Right Side)
        self.controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.controls_frame.grid(row=0, column=2, padx=20, pady=20)
        
        self.btn_prev = self._make_btn("⏮", self.spotify.prev_track)
        self.btn_play = self._make_btn("▶", self.spotify.play_pause, size=40, highlight=True)
        self.btn_next = self._make_btn("⏭", self.spotify.next_track)

        # 4. Progress (Bottom)
        self.progress = ctk.CTkProgressBar(
            self, 
            height=4, 
            progress_color=Styles.BLUE, 
            fg_color="#333",
            corner_radius=2,
            border_width=0
        )
        self.progress.grid(row=1, column=1, columnspan=2, sticky="ew", padx=(0, 20), pady=(0, 20))
        self.progress.set(0)

        # Start Services
        self.spotify.start_polling()
        self.start_progress_update()

    def _create_placeholder_image(self):
        # Create a grey placeholder
        img = Image.new('RGB', (60, 60), color='#333333')
        return ctk.CTkImage(light_image=img, dark_image=img, size=(60, 60))

    def _make_btn(self, text, cmd, size=32, highlight=False):
        color = "transparent"
        fg = "white"
        if highlight:
            color = Styles.BLUE # Using token
            fg = "white"
            
        btn = ctk.CTkButton(
            self.controls_frame, 
            text=text, 
            width=size, height=size, 
            corner_radius=size/2,
            fg_color=color,
            hover_color="#333",
            text_color=fg,
            font=("Arial", 16),
            command=cmd
        )
        btn.pack(side="left", padx=5)
        return btn

    def update_ui(self, track):
        try:
            # Info
            title = track["title"]
            artist = track["artist"]
            if len(title) > 25: title = title[:25] + "..."
            self.title_lbl.configure(text=title)
            self.artist_lbl.configure(text=artist)
            
            # Play State
            icon = "||" if track["playing"] else "▶"
            if self.btn_play.cget("text") != icon:
                self.btn_play.configure(text=icon)
            
            # Progress
            dur = track["duration"]
            pos = track["position"]
            if dur > 0:
                self.progress.set(pos/dur)

            # Album Art (Async)
            art_url = track.get("artwork_url")
            if art_url and art_url != "missing value" and art_url != self.last_art_url:
                self.last_art_url = art_url
                threading.Thread(target=self._fetch_art, args=(art_url,), daemon=True).start()
                
        except Exception as e:
            print(f"UI Error: {e}")

    def _fetch_art(self, url):
        try:
            import ssl
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            with urllib.request.urlopen(url, context=ctx) as u:
                raw_data = u.read()
            
            image = Image.open(BytesIO(raw_data))
            # Resize
            ctk_img = ctk.CTkImage(light_image=image, dark_image=image, size=(60, 60))
            
            # Update on main thread
            self.art_label.configure(image=ctk_img)
            self.art_label.image = ctk_img # Keep ref
        except Exception as e:
            print(f"Art Fetch Error: {e}")

    def start_progress_update(self):
        self.after(1000, self.start_progress_update)

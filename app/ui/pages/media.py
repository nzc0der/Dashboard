import customtkinter as ctk
import urllib.request
import threading
from io import BytesIO
from PIL import Image, ImageFilter
from app.services.spotify_service import SpotifyService
from app.ui.styles import Styles

class MediaPage(ctk.CTkFrame):
    """
    Immersive Apple Music style Full Screen Player.
    """
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self.spotify = SpotifyService()
        self.spotify.add_callback(self.update_ui)
        self.last_art_url = None
        self.default_img = self._create_placeholder()
        
        # Grid: 2 Columns (Art | Controls/Lyrics)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # --- Left: Album Art (Huge) ---
        self.art_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.art_frame.grid(row=0, column=0, sticky="nsew", padx=50, pady=50)
        
        # Shadow effect (Frame behind image)
        self.shadow = ctk.CTkFrame(self.art_frame, width=400, height=400, corner_radius=20, fg_color="#111")
        self.shadow.place(relx=0.5, rely=0.5, anchor="center")
        
        self.art_label = ctk.CTkLabel(self.art_frame, text="", image=self.default_img)
        self.art_label.place(relx=0.5, rely=0.5, anchor="center")

        # --- Right: Info & Controls ---
        self.info_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.info_frame.grid(row=0, column=1, sticky="nsew", padx=50, pady=100)
        
        self.title_lbl = ctk.CTkLabel(
            self.info_frame, 
            text="Waiting for Music...", 
            font=("SF Pro Display", 48, "bold"),
            text_color="white",
            wraplength=400,
            justify="left"
        )
        self.title_lbl.pack(anchor="w", pady=(0, 10))
        
        self.artist_lbl = ctk.CTkLabel(
            self.info_frame, 
            text="Spotify Integration", 
            font=("SF Pro Display", 32),
            text_color=Styles.TEXT_SEC,
            anchor="w"
        )
        self.artist_lbl.pack(anchor="w", pady=(0, 40))
        
        # Progress Bar
        self.progress = ctk.CTkProgressBar(
            self.info_frame, 
            height=6, 
            progress_color=Styles.BLUE, 
            fg_color="#333",
            corner_radius=3,
        )
        self.progress.pack(fill="x", pady=(0, 10))
        
        self.time_lbl = ctk.CTkFrame(self.info_frame, fg_color="transparent")
        self.time_lbl.pack(fill="x")
        self.lbl_pos = ctk.CTkLabel(self.time_lbl, text="0:00", text_color=Styles.TEXT_SEC)
        self.lbl_pos.pack(side="left")
        self.lbl_dur = ctk.CTkLabel(self.time_lbl, text="-:--", text_color=Styles.TEXT_SEC)
        self.lbl_dur.pack(side="right")
        
        # Controls Row (Huge Buttons)
        self.controls = ctk.CTkFrame(self.info_frame, fg_color="transparent")
        self.controls.pack(fill="x", pady=40)
        
        self.btn_prev = self._make_btn("⏮", self.spotify.prev_track, 60)
        self.btn_play = self._make_btn("▶", self.spotify.play_pause, 80, True)
        self.btn_next = self._make_btn("⏭", self.spotify.next_track, 60)
        
        self.spotify.start_polling()

    def _create_placeholder(self):
        img = Image.new('RGB', (400, 400), color='#222')
        return ctk.CTkImage(light_image=img, dark_image=img, size=(400, 400))

    def _make_btn(self, text, cmd, size, highlight=False):
        color = "transparent"
        fg = "white"
        if highlight:
            color = "white"
            fg = "black"
            
        btn = ctk.CTkButton(
            self.controls, 
            text=text, 
            width=size, height=size, 
            corner_radius=size/2,
            fg_color=color,
            hover_color="#ddd" if highlight else "#333",
            text_color=fg,
            font=("Arial", size//2),
            command=cmd
        )
        btn.pack(side="left", padx=20, expand=True)
        return btn

    def update_ui(self, track):
        try:
            # Metadata
            self.title_lbl.configure(text=track["title"])
            self.artist_lbl.configure(text=f"{track['artist']} — {track['album']}")
            
            # Progress
            dur = track["duration"]
            pos = track["position"]
            if dur > 0:
                self.progress.set(pos/dur)
                # update time labels
                self.lbl_pos.configure(text=self._fmt_time(pos))
                self.lbl_dur.configure(text=self._fmt_time(dur))
            
            # Play State
            icon = "||" if track["playing"] else "▶"
            if self.btn_play.cget("text") != icon:
                self.btn_play.configure(text=icon)

            # Art
            art_url = track.get("artwork_url")
            if art_url and art_url != self.last_art_url:
                self.last_art_url = art_url
                threading.Thread(target=self._fetch_art, args=(art_url,), daemon=True).start()
                
        except Exception as e:
            pass

    def _fmt_time(self, seconds):
        if not seconds: return "0:00"
        m = int(seconds // 60)
        s = int(seconds % 60)
        return f"{m}:{s:02d}"

    def _fetch_art(self, url):
        try:
            # Bypass SSL for images too just in case
            import ssl
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            with urllib.request.urlopen(url, context=ctx) as u:
                raw = u.read()
            
            image = Image.open(BytesIO(raw))
            image = image.resize((400, 400), Image.Resampling.LANCZOS)
            ctk_img = ctk.CTkImage(light_image=image, dark_image=image, size=(400, 400))
            
            self.art_label.configure(image=ctk_img)
            self.art_label.image = ctk_img
        except:
            pass

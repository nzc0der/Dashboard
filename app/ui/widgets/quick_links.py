import customtkinter as ctk
import os
from PIL import Image
from app.ui.styles import Styles
import threading

class QuickLinksWidget(ctk.CTkFrame):
    """
    iOS Home Screen Style Dock with support for custom icons.
    """
    def __init__(self, parent):
        super().__init__(parent, fg_color=Styles.BG_CARD, corner_radius=Styles.RADIUS_L)
        
        self.pack_propagate(False) # Keep fixed height
        
        # Paths for icons
        self.icon_dir = os.path.join("assets", "icons", "links")
        if not os.path.exists(self.icon_dir):
            os.makedirs(self.icon_dir, exist_ok=True)
        
        self.links = [
            ("GitHub", "https://github.com", "#24292e"),
            ("Notion", "https://notion.so", "#000000"),
            ("Gmail", "https://mail.google.com", "#EA4335"),
            ("ChatGPT", "https://chat.openai.com", "#10a37f"),
            ("YouTube", "https://youtube.com", "#FF0000"),
            ("Twitter", "https://twitter.com", "#1DA1F2"),
            ("LinkedIn", "https://linkedin.com", "#0077b5")
        ]
        
        # Horizontal Scroll if many items, otherwise center
        self.container = ctk.CTkScrollableFrame(self, fg_color="transparent", orientation="horizontal", height=80)
        self.container.pack(expand=True, fill="both", padx=20, pady=15)

        self.buttons = {}

        for name, url, color in self.links:
            btn = self._create_link_button(self.container, name, url, color)
            btn.pack(side="left", padx=10, pady=5)
            self.buttons[name] = btn
            
            # Start background fetch for icon
            threading.Thread(target=self._fetch_icon, args=(name, url), daemon=True).start()

    def _create_link_button(self, parent, name, url, color):
        # Check local cache first
        icon_path = os.path.join(self.icon_dir, f"{name.lower()}.png")
        img = None
        text = name[:2]
        
        if os.path.exists(icon_path):
            try:
                pil_img = Image.open(icon_path)
                img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(48, 48))
                text = ""
            except:
                pass
        
        # Create Button
        # We store the image ref in the button to prevent GC
        btn = ctk.CTkButton(
            parent, 
            text=text, 
            image=img,
            width=70, height=70, 
            corner_radius=20, # Squircle
            fg_color=color, 
            hover_color=color, # Could darken slightly
            font=("SF Pro Display", 24, "bold"),
            command=lambda u=url: self.open(u)
        )
        return btn

    def _fetch_icon(self, name, url):
        # Google S2 Service (Best for high res)
        # https://t1.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=http://www.google.com&size=128
        
        icon_path = os.path.join(self.icon_dir, f"{name.lower()}.png")
        
        # If exists and validSize, skip
        if os.path.exists(icon_path) and os.path.getsize(icon_path) > 0:
            return

        try:
            import urllib.request
            import ssl
            
            # 128px is good for Retina
            api_url = f"https://t1.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url={url}&size=128"
            
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            req = urllib.request.Request(
                api_url, 
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
                if response.status == 200:
                    data = response.read()
                    if len(data) > 0:
                        with open(icon_path, "wb") as f:
                            f.write(data)
                        
                        # Update UI on main thread (safe-ish in CTK)
                        self._update_button_icon(name, icon_path)
                        
        except Exception as e:
            # print(f"Failed to fetch icon for {name}: {e}")
            pass

    def _update_button_icon(self, name, icon_path):
        if name in self.buttons:
            try:
                pil_img = Image.open(icon_path)
                img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(48, 48))
                self.buttons[name].configure(image=img, text="")
                self.buttons[name].image = img # Keep ref
            except:
                pass

    def open(self, url):
        import webbrowser
        webbrowser.open(url)

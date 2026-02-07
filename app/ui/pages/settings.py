import customtkinter as ctk
from app.ui.styles import Styles

class SettingsPage(ctk.CTkFrame):
    """
    Application Configuration Page.
    """
    def __init__(self, parent, db):
        super().__init__(parent, fg_color="transparent")
        self.db = db
        
        # Grid Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Header
        self.grid_rowconfigure(1, weight=1) # Content

        # Header
        ctk.CTkLabel(
            self, 
            text="Settings", 
            font=Styles.H1, 
            text_color="white"
        ).grid(row=0, column=0, sticky="w", pady=(0, 30))

        # Content Container
        self.content = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.content.grid(row=1, column=0, sticky="nsew")
        
        # --- Profile Section ---
        self._add_section_header("Profile")
        
        self.name_var = ctk.StringVar(value=self.db.get_username())
        self._add_input("Display Name", self.name_var)
        
        # --- Weather Section ---
        self._add_section_header("Weather Configuration")
        
        loc = self.db.get_weather_location()
        self.lat_var = ctk.StringVar(value=str(loc["lat"]))
        self.lon_var = ctk.StringVar(value=str(loc["lon"]))
        
        self._add_input("Latitude", self.lat_var)
        self._add_input("Longitude", self.lon_var)
        
        # --- Save Button ---
        self.btn_save = ctk.CTkButton(
            self.content, 
            text="Save Changes", 
            height=50, 
            corner_radius=25,
            fg_color=Styles.PRIMARY, 
            font=("Arial", 16, "bold"),
            command=self.save_settings
        )
        self.btn_save.pack(pady=40, fill="x", padx=100)
        
        # --- About ---
        ctk.CTkLabel(
            self.content, 
            text="ZenithOS v2.0 - Built by Commander", 
            font=Styles.CAPTION, 
            text_color=Styles.TEXT_SEC
        ).pack(pady=20)

    def _add_section_header(self, text):
        container = ctk.CTkFrame(self.content, fg_color="transparent")
        container.pack(fill="x", pady=(20, 10))
        
        ctk.CTkLabel(
            container, 
            text=text, 
            font=Styles.H2, 
            text_color="white"
        ).pack(side="left")
        
        ctk.CTkFrame(container, height=1, fg_color="#333").pack(side="left", fill="x", expand=True, padx=(20, 0))

    def _add_input(self, label, variable):
        frame = ctk.CTkFrame(self.content, fg_color=Styles.BG_CARD, corner_radius=Styles.RADIUS_M)
        frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            frame, 
            text=label, 
            font=Styles.BODY_BOLD, 
            text_color="white",
            width=150,
            anchor="w"
        ).pack(side="left", padx=20, pady=15)
        
        entry = ctk.CTkEntry(
            frame, 
            textvariable=variable, 
            font=Styles.BODY, 
            fg_color="transparent", 
            border_width=0, 
            text_color=Styles.TEXT_MAIN,
            height=40
        )
        entry.pack(side="left", fill="x", expand=True, padx=20)

    def save_settings(self):
        try:
            # Save Name
            new_name = self.name_var.get().strip()
            if new_name:
                self.db.set_username(new_name)
            
            # Save Weather
            lat = float(self.lat_var.get())
            lon = float(self.lon_var.get())
            self.db.set_weather_location(lat, lon)
            
            # Helper Feedback
            self.btn_save.configure(text="Saved!", fg_color=Styles.SECONDARY)
            self.after(2000, lambda: self.btn_save.configure(text="Save Changes", fg_color=Styles.PRIMARY))
            
            # Note: A restart might be required for some changes to take full effect (like weather service init)
            # Ideally we'd broadcast an event but for now this persists properly.
            
        except ValueError:
            self.btn_save.configure(text="Invalid Input", fg_color=Styles.DANGER)
            self.after(2000, lambda: self.btn_save.configure(text="Save Changes", fg_color=Styles.PRIMARY))

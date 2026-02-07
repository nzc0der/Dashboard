import calendar
import datetime
import customtkinter as ctk
from app.ui.styles import Styles

class CalendarWidget(ctk.CTkFrame):
    """
    Minimalist Monthly Calendar View.
    """
    def __init__(self, parent):
        super().__init__(parent, fg_color=Styles.BG_CARD, corner_radius=Styles.RADIUS_L)
        
        self.year = datetime.date.today().year
        self.month = datetime.date.today().month
        
        # Header (Month Year + Nav)
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=15, pady=(15, 10))
        
        self.btn_prev = ctk.CTkButton(
            self.header, text="<", width=30, height=30, 
            fg_color="transparent", text_color=Styles.TEXT_SEC, 
            hover_color=Styles.BG_CARD_HOVER,
            command=self.prev_month
        )
        self.btn_prev.pack(side="left")
        
        self.lbl_month = ctk.CTkLabel(
            self.header, text=f"{self._get_month_name()} {self.year}", 
            font=Styles.H3, text_color="white"
        )
        self.lbl_month.pack(side="left", expand=True)
        
        self.btn_next = ctk.CTkButton(
            self.header, text=">", width=30, height=30, 
            fg_color="transparent", text_color=Styles.TEXT_SEC, 
            hover_color=Styles.BG_CARD_HOVER,
            command=self.next_month
        )
        self.btn_next.pack(side="right")
        
        # Days Header (Su Mo Tu...)
        self.days_header = ctk.CTkFrame(self, fg_color="transparent")
        self.days_header.pack(fill="x", padx=10)
        
        days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        for d in days:
            ctk.CTkLabel(self.days_header, text=d, font=("Arial", 12, "bold"), text_color=Styles.TEXT_SEC, width=35).pack(side="left", expand=True)
            
        # Calendar Grid
        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.render_calendar()

    def _get_month_name(self):
        return calendar.month_name[self.month]

    def prev_month(self):
        self.month -= 1
        if self.month < 1:
            self.month = 12
            self.year -= 1
        self.render_calendar()

    def next_month(self):
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1
        self.render_calendar()

    def render_calendar(self):
        # Update Header
        self.lbl_month.configure(text=f"{self._get_month_name()} {self.year}")
        
        # Clear old
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
            
        # Get days
        cal = calendar.monthcalendar(self.year, self.month)
        today = datetime.date.today()
        
        for r, week in enumerate(cal):
            row_frame = ctk.CTkFrame(self.grid_frame, fg_color="transparent")
            row_frame.pack(fill="x", expand=True)
            
            for day in week:
                if day == 0:
                    lbl = ctk.CTkLabel(row_frame, text="", width=35)
                else:
                    is_today = (day == today.day and self.month == today.month and self.year == today.year)
                    fg = Styles.PRIMARY if is_today else "transparent"
                    text_col = "white" if is_today else Styles.TEXT_MAIN
                    
                    lbl = ctk.CTkLabel(
                        row_frame, 
                        text=str(day), 
                        width=32, height=32,
                        fg_color=fg,
                        text_color=text_col,
                        corner_radius=10
                    )
                lbl.pack(side="left", expand=True, padx=1, pady=1)

import customtkinter as ctk
from app.ui.styles import Styles

class FocusPage(ctk.CTkFrame):
    """
    Distraction-Free Focus Zone.
    """
    def __init__(self, parent, db):
        super().__init__(parent, fg_color="transparent")
        
        # Center Content
        # self.pack(fill="both", expand=True) <--- REMOVED

        
        # Header
        self.header = ctk.CTkLabel(
            self, 
            text="Deep Focus Mode", 
            font=Styles.H1, 
            text_color="white"
        )
        self.header.pack(pady=40)
        
        # Timer (Pomodoro Style)
        self.timer_frame = ctk.CTkFrame(self, fg_color=Styles.BG_CARD, corner_radius=100, width=300, height=300)
        self.timer_frame.pack(pady=20)
        
        self.timer_lbl = ctk.CTkLabel(
            self.timer_frame, 
            text="25:00", 
            font=("SF Pro Display", 80, "bold"),
            text_color=Styles.PRIMARY
        )
        self.timer_lbl.place(relx=0.5, rely=0.5, anchor="center")
        
        # Controls
        self.btn_start = ctk.CTkButton(
            self, 
            text="Start Focus", 
            width=200, height=50, 
            corner_radius=25, 
            fg_color=Styles.PRIMARY, 
            font=("Arial", 18, "bold"),
            command=self.toggle_timer
        )
        self.btn_start.pack(pady=30)
        
        # Bottom Quote
        self.quote = ctk.CTkLabel(
            self, 
            text='"Success is the sum of small efforts, repeated day in and day out."', 
            font=("SF Pro Text", 16, "italic"),
            text_color=Styles.TEXT_SEC
        )
        self.quote.pack(pady=20)

        # Timer Logic
        self.running = False
        self.default_time = 25 * 60
        self.remaining_time = self.default_time
        self.timer_id = None

    def toggle_timer(self):
        if self.running:
            self.stop_timer()
        else:
            self.start_timer()

    def start_timer(self):
        self.running = True
        self.btn_start.configure(text="Pause Focus", fg_color=Styles.DANGER)
        self.count_down()

    def stop_timer(self):
        self.running = False
        self.btn_start.configure(text="Resume Focus", fg_color=Styles.PRIMARY)
        if self.timer_id:
            try:
                self.after_cancel(self.timer_id)
            except ValueError:
                pass
            self.timer_id = None

    def count_down(self):
        if self.running and self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_display()
            self.timer_id = self.after(1000, self.count_down)
        elif self.remaining_time <= 0:
            self.timer_finished()

    def update_display(self):
        m = self.remaining_time // 60
        s = self.remaining_time % 60
        self.timer_lbl.configure(text=f"{m:02d}:{s:02d}")

    def timer_finished(self):
        self.running = False
        self.remaining_time = self.default_time
        self.update_display()
        self.btn_start.configure(text="Start Focus", fg_color=Styles.PRIMARY)
        # Could add a sound here or a notification
        print("Focus Session Complete!")

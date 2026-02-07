import customtkinter as ctk
import webbrowser
import json
import os
import threading
import time
import random
from datetime import datetime

# ==============================================================================
#   CONFIGURATION & THEME SETUP
# ==============================================================================

# Set the theme to "Dark" and the color accent to "Blue"
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# The filename for saving your data
DATA_FILE = "titanium_data.json"

# ==============================================================================
#   BACKEND: DATA MANAGER
# ==============================================================================

class DataManager:
    """
    Handles all file operations. Saves tasks and notes to a local JSON file.
    This ensures your data persists even after you close the app.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = {
            "tasks": [],
            "notes": "",
            "username": "Commander"
        }
        self.load()

    def load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as f:
                    loaded = json.load(f)
                    # Merge loaded data with defaults to avoid key errors
                    for key in self.data:
                        if key in loaded:
                            self.data[key] = loaded[key]
            except Exception as e:
                print(f"Error loading data: {e}")

    def save(self):
        try:
            with open(self.filepath, "w") as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    # --- Task Helpers ---
    def add_task(self, text):
        new_task = {
            "id": int(time.time() * 1000), # Unique ID based on time
            "text": text,
            "done": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.data["tasks"].append(new_task)
        self.save()
        return new_task

    def delete_task(self, task_id):
        self.data["tasks"] = [t for t in self.data["tasks"] if t["id"] != task_id]
        self.save()

    def toggle_task(self, task_id):
        for t in self.data["tasks"]:
            if t["id"] == task_id:
                t["done"] = not t["done"]
        self.save()

    def get_tasks(self):
        return self.data["tasks"]

    # --- Note Helpers ---
    def set_notes(self, text):
        self.data["notes"] = text
        self.save()

    def get_notes(self):
        return self.data["notes"]

# Initialize the global data manager
db = DataManager(DATA_FILE)


# ==============================================================================
#   UI COMPONENT: CLOCK WIDGET
# ==============================================================================

class ClockWidget(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=15, fg_color="#1a1a1a") # Darker background
        
        # Time Label (Big)
        self.time_lbl = ctk.CTkLabel(
            self, 
            text="00:00", 
            font=("Roboto Medium", 48),
            text_color="white"
        )
        self.time_lbl.pack(pady=(15, 0))

        # Date Label (Small)
        self.date_lbl = ctk.CTkLabel(
            self, 
            text="Loading Date...", 
            font=("Roboto", 14),
            text_color="#a0a0a0"
        )
        self.date_lbl.pack(pady=(0, 15))

        # Start the update loop
        self.update_clock()

    def update_clock(self):
        now = datetime.now()
        # Format: 12:45 PM
        self.time_lbl.configure(text=now.strftime("%I:%M %p"))
        # Format: Monday, January 01
        self.date_lbl.configure(text=now.strftime("%A, %B %d"))
        # Schedule next update in 1 second (1000ms)
        self.after(1000, self.update_clock)


# ==============================================================================
#   UI COMPONENT: SYSTEM MONITOR (VISUALIZER)
# ==============================================================================

class SystemMonitorWidget(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=15)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # CPU Bar
        self.cpu_label = ctk.CTkLabel(self, text="CPU Load", font=("Arial", 12, "bold"))
        self.cpu_label.grid(row=0, column=0, pady=(10,0))
        
        self.cpu_bar = ctk.CTkProgressBar(self, orientation="vertical", height=60, width=15)
        self.cpu_bar.grid(row=1, column=0, pady=10)
        self.cpu_bar.set(0.5)

        # RAM Bar
        self.ram_label = ctk.CTkLabel(self, text="RAM Usage", font=("Arial", 12, "bold"))
        self.ram_label.grid(row=0, column=1, pady=(10,0))
        
        self.ram_bar = ctk.CTkProgressBar(self, orientation="vertical", height=60, width=15, progress_color="#e53935")
        self.ram_bar.grid(row=1, column=1, pady=10)
        self.ram_bar.set(0.4)

        # Start simulation
        self.animate_stats()

    def animate_stats(self):
        # Creates a tech-y fluctuation effect
        new_cpu = random.uniform(0.1, 0.6)
        new_ram = random.uniform(0.3, 0.8)
        
        self.cpu_bar.set(new_cpu)
        self.ram_bar.set(new_ram)
        
        self.after(2000, self.animate_stats)


# ==============================================================================
#   UI COMPONENT: MUSIC PLAYER
# ==============================================================================

class MusicPlayerWidget(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=15, fg_color="#2b2b2b")
        
        # Layout
        self.grid_columnconfigure(1, weight=1) # Middle expands

        # 1. Album Art Placeholder
        self.art = ctk.CTkButton(
            self, text="♫", width=50, height=50, 
            corner_radius=10, fg_color="#444", hover=False,
            font=("Arial", 24)
        )
        self.art.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

        # 2. Song Info
        self.title = ctk.CTkLabel(self, text="Starlight", font=("Arial", 14, "bold"), anchor="w")
        self.title.grid(row=0, column=1, sticky="w", padx=(5,10), pady=(12,0))
        
        self.artist = ctk.CTkLabel(self, text="Muse", font=("Arial", 12), text_color="gray", anchor="w")
        self.artist.grid(row=1, column=1, sticky="w", padx=(5,10), pady=(0,12))

        # 3. Controls
        self.btn_play = ctk.CTkButton(self, text="▶", width=30, height=30, corner_radius=15, command=self.toggle_play)
        self.btn_play.grid(row=0, column=2, rowspan=2, padx=15)
        
        # 4. Progress Bar (Bottom)
        self.progress = ctk.CTkProgressBar(self, height=4, progress_color="#1f6aa5")
        self.progress.grid(row=2, column=0, columnspan=3, sticky="ew", padx=10, pady=(0, 10))
        self.progress.set(0)

        self.playing = True
        self.progress_val = 0.0
        self.start_thread()

    def toggle_play(self):
        self.playing = not self.playing
        self.btn_play.configure(text="||" if self.playing else "▶")

    def start_thread(self):
        thread = threading.Thread(target=self._animate, daemon=True)
        thread.start()

    def _animate(self):
        while True:
            if self.playing:
                self.progress_val += 0.005
                if self.progress_val > 1.0:
                    self.progress_val = 0.0
                try:
                    self.progress.set(self.progress_val)
                except:
                    break # Stop if window closed
            time.sleep(0.1)


# ==============================================================================
#   UI COMPONENT: SEARCH & NEWS BAR
# ==============================================================================

class TopBarWidget(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, height=50, corner_radius=20)
        
        # Search Entry
        self.search_entry = ctk.CTkEntry(
            self, 
            placeholder_text="Search Google...",
            width=300,
            border_width=0,
            fg_color="#2b2b2b"
        )
        self.search_entry.pack(side="left", padx=15, pady=10)
        self.search_entry.bind("<Return>", self.run_search)

        # Search Button
        self.search_btn = ctk.CTkButton(
            self, text="Search", width=60, command=self.run_search
        )
        self.search_btn.pack(side="left", padx=(0, 15))

        # News Ticker (Right side)
        self.news_lbl = ctk.CTkLabel(self, text="LIVE: System Online...", text_color="gray")
        self.news_lbl.pack(side="right", padx=20)
        
        self.news_items = [
            "UPDATE: Weather is partly cloudy.",
            "REMINDER: Drink water.",
            "STATUS: All systems nominal.",
            "MARKET: Tech stocks up 2.4%."
        ]
        self.current_news_idx = 0
        self.rotate_news()

    def run_search(self, event=None):
        query = self.search_entry.get()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            self.search_entry.delete(0, "end")

    def rotate_news(self):
        self.news_lbl.configure(text=self.news_items[self.current_news_idx])
        self.current_news_idx = (self.current_news_idx + 1) % len(self.news_items)
        self.after(4000, self.rotate_news)


# ==============================================================================
#   UI COMPONENT: TASK MANAGER
# ==============================================================================

class TaskManagerWidget(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=15)
        
        # Header
        header = ctk.CTkLabel(self, text="MISSION OBJECTIVES", font=("Arial", 16, "bold"))
        header.pack(pady=10, padx=15, anchor="w")

        # Input Area
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.entry = ctk.CTkEntry(input_frame, placeholder_text="New objective...")
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.entry.bind("<Return>", self.add_task)
        
        add_btn = ctk.CTkButton(input_frame, text="+", width=30, command=self.add_task)
        add_btn.pack(side="right")

        # Scrollable List
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.refresh_ui()

    def add_task(self, event=None):
        text = self.entry.get()
        if text.strip():
            db.add_task(text)
            self.entry.delete(0, "end")
            self.refresh_ui()

    def delete_task(self, task_id):
        db.delete_task(task_id)
        self.refresh_ui()

    def refresh_ui(self):
        # Clear old widgets
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # Build new list
        tasks = db.get_tasks()
        
        if not tasks:
            ctk.CTkLabel(self.scroll_frame, text="No active tasks.", text_color="gray").pack(pady=20)
            return

        for t in tasks:
            self.build_task_row(t)

    def build_task_row(self, task):
        row = ctk.CTkFrame(self.scroll_frame, fg_color="#2b2b2b", corner_radius=8)
        row.pack(fill="x", pady=2)
        
        # Task Text
        lbl = ctk.CTkLabel(row, text=task["text"], anchor="w", font=("Arial", 13))
        lbl.pack(side="left", padx=10, pady=8)

        # Delete Button
        del_btn = ctk.CTkButton(
            row, text="✕", width=25, height=25, 
            fg_color="transparent", hover_color="#800000", text_color="#ff5555",
            command=lambda tid=task["id"]: self.delete_task(tid)
        )
        del_btn.pack(side="right", padx=5)


# ==============================================================================
#   UI COMPONENT: NOTES & SCRATCHPAD
# ==============================================================================

class NotesWidget(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=15)
        
        header = ctk.CTkLabel(self, text="DATA LOGS", font=("Arial", 16, "bold"))
        header.pack(pady=10, padx=15, anchor="w")

        self.textbox = ctk.CTkTextbox(self, font=("Consolas", 14), wrap="word")
        self.textbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Load saved notes
        self.textbox.insert("0.0", db.get_notes())

        # Save Button
        save_btn = ctk.CTkButton(self, text="Save Logs", command=self.save_notes)
        save_btn.pack(pady=(0, 10))

    def save_notes(self):
        text = self.textbox.get("0.0", "end")
        db.set_notes(text)
        print("Notes Saved.")


# ==============================================================================
#   UI COMPONENT: QUICK LINKS
# ==============================================================================

class QuickLinksWidget(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, height=60, corner_radius=15, fg_color="transparent")
        
        links = [
            ("YouTube", "https://youtube.com"),
            ("Gmail", "https://gmail.com"),
            ("GitHub", "https://github.com"),
            ("ChatGPT", "https://chatgpt.com"),
            ("Reddit", "https://reddit.com")
        ]

        for name, url in links:
            btn = ctk.CTkButton(
                self, 
                text=name, 
                fg_color="#2b2b2b", 
                border_width=1,
                border_color="#333",
                hover_color="#1f6aa5",
                command=lambda u=url: webbrowser.open(u)
            )
            btn.pack(side="left", expand=True, fill="x", padx=5)


# ==============================================================================
#   MAIN APPLICATION ASSEMBLY
# ==============================================================================

class ZenithOS(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Config
        self.title("Zenith OS // Command Center")
        self.geometry("1100x750")
        
        # Grid Configuration (2 Columns, 3 Rows)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1) # Main content area expands

        # --- ROW 0: TOP BAR ---
        self.top_bar = TopBarWidget(self)
        self.top_bar.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(20, 10))

        # --- ROW 1: WIDGETS ---
        # Left: Clock
        self.clock_widget = ClockWidget(self)
        self.clock_widget.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        # Right: Sub-grid for Music + Stats
        self.right_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.right_panel.grid(row=1, column=1, sticky="nsew", padx=20, pady=10)
        
        # Split right panel into Music (Left) and Stats (Right)
        self.music_widget = MusicPlayerWidget(self.right_panel)
        self.music_widget.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.stats_widget = SystemMonitorWidget(self.right_panel)
        self.stats_widget.pack(side="right", fill="both", padx=(10, 0))

        # --- ROW 2: MAIN CONTENT ---
        # Left: Tasks
        self.task_widget = TaskManagerWidget(self)
        self.task_widget.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

        # Right: Notes
        self.notes_widget = NotesWidget(self)
        self.notes_widget.grid(row=2, column=1, sticky="nsew", padx=20, pady=10)

        # --- ROW 3: FOOTER ---
        self.links_widget = QuickLinksWidget(self)
        self.links_widget.grid(row=3, column=0, columnspan=2, sticky="ew", padx=20, pady=(10, 20))


# ==============================================================================
#   ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    app = ZenithOS()
    # Handle graceful exit could be added here
    app.mainloop()
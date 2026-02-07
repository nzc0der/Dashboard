import json
import os
import time
from datetime import datetime
from threading import Lock
from app.core import settings


class DataManager:
    """
    Manages persistent data storage for the dashboard.
    Handles tasks, notes, user preferences, and other application state.
    Uses a threading lock to prevent race conditions during file access.
    """
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.lock = Lock()
        self.data = {
            "tasks": [],
            "notes": "",
            "username": "Commander",
            "theme": "dark",
            "weather_location": {"lat": settings.WEATHER_LAT, "lon": settings.WEATHER_LON}, # Defaults to Ormond, Melbourne
            "last_active": None,
            "session_count": 0
        }
        self.load()
        self._update_session()

    def load(self):
        """Loads data from the JSON file into memory."""
        with self.lock:
            if os.path.exists(self.filepath):
                try:
                    with open(self.filepath, "r", encoding='utf-8') as f:
                        loaded = json.load(f)
                        # Deep merge for simplicity (only top level keys for now)
                        for key in self.data:
                            if key in loaded:
                                self.data[key] = loaded[key]
                        # Ensure tasks are lists
                        if not isinstance(self.data.get("tasks"), list):
                            self.data["tasks"] = []
                except (json.JSONDecodeError, IOError) as e:
                    print(f"[DataManager] Error loading data: {e}")
                    # Could implement a backup restore here if needed
            else:
                self.save() # Create file if it doesn't exist

    def save(self):
        """Writes current robust data state to JSON file."""
        with self.lock:
            try:
                # Update last saved timestamp
                self.data["last_saved"] = datetime.now().isoformat()
                
                with open(self.filepath, "w", encoding='utf-8') as f:
                    json.dump(self.data, f, indent=4, ensure_ascii=False)
            except IOError as e:
                print(f"[DataManager] Error saving data: {e}")

    def _update_session(self):
        """Internal method to update session statistics."""
        self.data["last_active"] = datetime.now().isoformat()
        self.data["session_count"] = self.data.get("session_count", 0) + 1
        self.save()

    # --- Task Operations ---
    
    def add_task(self, text, priority="normal"):
        """Adds a new task with metadata including priority and timestamps."""
        task_id = int(time.time() * 1000)
        new_task = {
            "id": task_id,
            "text": text,
            "done": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "completed_at": None,
            "priority": priority
        }
        self.data["tasks"].append(new_task)
        self.save()
        return new_task

    def delete_task(self, task_id):
        """Removes a task by ID."""
        original_count = len(self.data["tasks"])
        self.data["tasks"] = [t for t in self.data["tasks"] if t["id"] != task_id]
        if len(self.data["tasks"]) < original_count:
            self.save()
            return True
        return False

    def toggle_task(self, task_id):
        """Toggles the completion status of a task."""
        for t in self.data["tasks"]:
            if t["id"] == task_id:
                t["done"] = not t["done"]
                if t["done"]:
                    t["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                else:
                    t["completed_at"] = None
                self.save()
                return t
        return None

    def get_tasks(self, filter_status=None):
        """
        Returns tasks, optionally filtered by status ('active', 'completed').
        """
        if filter_status == 'active':
            return [t for t in self.data["tasks"] if not t["done"]]
        elif filter_status == 'completed':
            return [t for t in self.data["tasks"] if t["done"]]
        return self.data["tasks"]

    def clear_completed_tasks(self):
        """Removes all completed tasks."""
        self.data["tasks"] = [t for t in self.data["tasks"] if not t["done"]]
        self.save()

    # --- Note Operations ---

    def set_notes(self, text):
        """Updates the persistent notes scratchpad."""
        if self.data["notes"] != text:
            self.data["notes"] = text
            self.save()

    def get_notes(self):
        """Retrieves the current notes."""
        return self.data.get("notes", "")

    # --- User/Config Operations ---

    def get_username(self):
        return self.data.get("username", "User")
    
    def set_username(self, name):
        self.data["username"] = name
        self.save()

    def get_weather_location(self):
        return self.data.get("weather_location", {"lat": 0, "lon": 0})

    def set_weather_location(self, lat, lon):
        self.data["weather_location"] = {"lat": lat, "lon": lon}
        self.save()

import subprocess
import threading
import time

class SpotifyService:
    """
    Controls Spotify on macOS using AppleScript (osascript).
    Requires Spotify desktop application to be installed.
    """
    
    def __init__(self):
        self.running = False
        self.current_track = {
            "title": "Not playing",
            "artist": "Unknown Artist",
            "album": "Unknown Album",
            "position": 0,
            "duration": 0,
            "playing": False
        }
        self.callbacks = []

    def start_polling(self):
        """Starts background thread to check Spotify state."""
        if not self.running:
            self.running = True
            thread = threading.Thread(target=self._poll_loop, daemon=True)
            thread.start()

    def add_callback(self, func):
        self.callbacks.append(func)

    def _poll_loop(self):
        while self.running:
            try:
                self._update_status()
                time.sleep(1) # Poll every second
            except Exception as e:
                # print(f"Spotify Poll Error: {e}")
                time.sleep(5)

    def _run_script(self, script):
        """Executes an AppleScript command."""
        try:
            command = ['osascript', '-e', script]
            result = subprocess.run(command, capture_output=True, text=True)
            return result.stdout.strip()
        except Exception as e:
            # print(f"AppleScript Error: {e}")
            return None

    def _update_status(self):
        # Check if Spotify is running
        is_running = self._run_script('application "Spotify" is running')
        if is_running != "true":
            new_track = {
                "title": "Spotify Closed",
                "artist": "--",
                "album": "--",
                "position": 0,
                "duration": 100,
                "playing": False
            }
        else:
            state = self._run_script('tell application "Spotify" to player state as string')
            playing = (state == "playing")
            
            title = self._run_script('tell application "Spotify" to name of current track as string')
            artist = self._run_script('tell application "Spotify" to artist of current track as string')
            album = self._run_script('tell application "Spotify" to album of current track as string')
            
            # Position and Duration are in seconds (or ms depending on API, usually seconds via AppleScript)
            # AppleScript for position: user can get 'player position'
            # AppleScript for duration: 'duration of current track' (ms)
            
            pos = self._run_script('tell application "Spotify" to player position as string')
            dur = self._run_script('tell application "Spotify" to duration of current track as string')
            
            try:
                pos = float(pos.replace(',', '.')) if pos else 0
                dur = int(dur) / 1000 if dur else 0 # duration is in ms
            except:
                pos = 0
                dur = 1

            new_track = {
                "title": title if title else "Unknown Title",
                "artist": artist if artist else "Unknown Artist",
                "album": album if album else "Unknown Album",
                "position": pos,
                "duration": dur,
                "playing": playing
            }
        
        # Only notify if changed significantly (or maybe every second to update progress bar)
        self.current_track = new_track
        self._notify()

    def _notify(self):
        for func in self.callbacks:
            try:
                func(self.current_track)
            except:
                pass

    # --- Actions ---

    def play_pause(self):
        self._run_script('tell application "Spotify" to playpause')
        self._update_status()

    def next_track(self):
        self._run_script('tell application "Spotify" to next track')
        self._update_status()

    def prev_track(self):
        self._run_script('tell application "Spotify" to previous track')
        self._update_status()

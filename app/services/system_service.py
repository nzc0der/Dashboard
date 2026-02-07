import time
import threading
try:
    import psutil
except ImportError:
    psutil = None

class SystemService:
    """
    Monitors system resources (CPU, RAM, Disk, Network).
    Uses psutil if available, otherwise returns simulated data.
    """
    
    def __init__(self):
        self.running = False
        self.stats = {
            "cpu_percent": 0,
            "ram_percent": 0,
            "disk_percent": 0,
            "net_sent": 0,
            "net_recv": 0
        }
        self.callbacks = []

    def start_polling(self):
        if not self.running:
            self.running = True
            thread = threading.Thread(target=self._poll_loop, daemon=True)
            thread.start()

    def add_callback(self, func):
        self.callbacks.append(func)

    def _poll_loop(self):
        while self.running:
            self._update_stats()
            self._notify()
            time.sleep(1)

    def _update_stats(self):
        if psutil:
            cpu = psutil.cpu_percent(interval=None)
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            net = psutil.net_io_counters()

            self.stats = {
                "cpu_percent": cpu,
                "ram_percent": ram,
                "disk_percent": disk,
                "net_sent": net.bytes_sent,
                "net_recv": net.bytes_recv
            }
        else:
            # Simulation mode
            import random
            self.stats = {
                "cpu_percent": random.randint(10, 60),
                "ram_percent": random.randint(30, 80),
                "disk_percent": 45,
                "net_sent": 0,
                "net_recv": 0
            }

    def _notify(self):
        for func in self.callbacks:
            try:
                func(self.stats)
            except:
                pass

import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

_reload_callback = None
_debounce_timer = None

class ExcelChangeHandler(FileSystemEventHandler):
    def __init__(self, filepath: str, callback):
        self.filepath = filepath
        self.callback = callback

    def on_modified(self, event):
        if event.src_path.endswith(self.filepath.split("/")[-1]):
            self._debounce()

    def on_created(self, event):
        if event.src_path.endswith(self.filepath.split("/")[-1]):
            self._debounce()

    def _debounce(self):
        global _debounce_timer
        if _debounce_timer:
            _debounce_timer.cancel()
        # Wait 2 seconds after last change before reloading (file may still be writing)
        _debounce_timer = threading.Timer(2.0, self._trigger)
        _debounce_timer.start()

    def _trigger(self):
        print("[Watcher] Excel file changed — reloading data...")
        try:
            self.callback()
        except Exception as e:
            print(f"[Watcher] Error during reload: {e}")


def start_watcher(filepath: str, callback):
    handler = ExcelChangeHandler(filepath, callback)
    observer = Observer()
    observer.schedule(handler, path="data/", recursive=False)
    observer.daemon = True
    observer.start()
    print(f"[Watcher] Watching: {filepath}")
    return observer
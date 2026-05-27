import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIGURATION ---
# We will watch your data_outputs folder to log whenever new leads are found
WATCH_DIRECTORY = os.path.abspath("data_outputs") 
LOG_FILE = "activity_log.txt"

class LeadEngineHandler(FileSystemEventHandler):
    """Logs whenever a scraper saves a new file or updates one."""
    
    def on_modified(self, event):
        if event.is_directory:
            return
        
        filename = os.path.basename(event.src_path)
        message = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] UPDATE: Scraper updated data in {filename}\n"
        print(message.strip())
        
        with open(LOG_FILE, "a") as f:
            f.write(message)

    def on_created(self, event):
        if event.is_directory:
            return
        
        filename = os.path.basename(event.src_path)
        message = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] NEW LEAD: A new lead file was created: {filename}\n"
        print(message.strip())
        
        with open(LOG_FILE, "a") as f:
            f.write(message)

def start_logger():
    if not os.path.exists(WATCH_DIRECTORY):
        os.makedirs(WATCH_DIRECTORY)
        print(f"[*] Created directory to watch: {WATCH_DIRECTORY}")

    event_handler = LeadEngineHandler()
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_DIRECTORY, recursive=False)
    
    print(f"[*] RSNW Activity Logger started.")
    print(f"[*] Monitoring folder: {WATCH_DIRECTORY}")
    print(f"[*] Logging to: {LOG_FILE}")
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping logger...")
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_logger()

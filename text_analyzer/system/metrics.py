from datetime import datetime
from threading import Lock

class Metrics:
    def __init__(self):
        self.files_processed = 0
        self.latest_file_processed_timestamp = None
        self._lock = Lock()

    def increment_files_processed(self):
        print("[M] increment_files_processed")
        with self._lock:
            self.files_processed += 1
            self.latest_file_processed_timestamp = datetime.now().isoformat()

    def get_metrics(self):
        with self._lock:
            return {
                "files_processed": self.files_processed,
                "latest_file_processed_timestamp": self.latest_file_processed_timestamp
            }

metrics = Metrics()
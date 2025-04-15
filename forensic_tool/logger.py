from datetime import datetime, timezone, timedelta
import os

class Logger:
    def __init__(self, log_dir):
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.log_file = os.path.join(log_dir, f"triage_log_{timestamp}.txt")

    def log(self, message):
        # Získaj aktuálny čas v UTC a lokalizuj ho
        now_utc = datetime.now(timezone.utc)
        # Napríklad pre stredoeurópsky čas: UTC+2
        local_offset_hours = 2
        local_time = now_utc + timedelta(hours=local_offset_hours)
        timestamp = local_time.strftime(f"%Y-%m-%d %H:%M:%S UTC+{local_offset_hours}")

        # Zápis do logu
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"{timestamp} | {message}\n")

    def get_log_path(self):
        return self.log_file

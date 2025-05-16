import csv
from collections import Counter
from datetime import datetime

class UidErrorsAnalyzer:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def analyze(self) -> dict:
        try:
            with open(self.csv_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                entries = list(reader)
        except Exception as e:
            print(f"Failed to read {self.csv_path}: {e}")
            return {}

        total = len(entries)
        per_day = Counter()
        keyword_counter = Counter()
        first_boot_time = "Not found"

        keywords = [
            "first boot", "factory reset", "boot",
            "system has been changed", "release-keys"
        ]

        for entry in entries:
            timestamp = entry["Timestamp"]
            message = entry["Message"].lower()

            try:
                dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S UTC")
                per_day[dt.strftime("%Y-%m-%d")] += 1
            except:
                pass

            # first boot details
            if "first boot" in message or "factory reset" in message:
                if first_boot_time == "Not found":
                    first_boot_time = timestamp

            for keyword in keywords:
                if keyword in message:
                    keyword_counter[keyword] += 1

        return {
            "Total entries": total,
            "First boot time": first_boot_time,
            "Entries per day": per_day.most_common(),
            "Common keywords": keyword_counter.most_common()
        }

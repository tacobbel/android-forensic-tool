import csv
from collections import Counter

class WpaSupplicantAnalyzer:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def analyze(self) -> dict:
        try:
            with open(self.csv_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                profiles = list(reader)
        except Exception as e:
            print(f"Failed to read {self.csv_path}: {e}")
            return {}

        total_profiles = len(profiles)
        ssids = [p["ssid"] for p in profiles if p["ssid"] and p["ssid"] != "N/A"]
        psk_count = sum(1 for p in profiles if p.get("psk") and p["psk"] != "N/A")
        bssid_count = sum(1 for p in profiles if p.get("bssid") and p["bssid"] != "N/A")

        key_mgmt_counts = Counter(p["key_mgmt"] for p in profiles if p["key_mgmt"] and p["key_mgmt"] != "N/A")

        return {
            "Total Wi-Fi profiles": total_profiles,
            "Profiles with password (PSK)": psk_count,
            "Profiles with BSSID": bssid_count,
            "Unique SSIDs": len(set(ssids)),
            "Top key management methods": key_mgmt_counts.most_common(5)
        }

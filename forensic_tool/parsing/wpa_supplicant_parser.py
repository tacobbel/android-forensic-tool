import os
import csv
from pathlib import Path
from forensic_tool.logger import Logger

class WpaSupplicantParser:
    def __init__(self, file_to_parse: str, output_dir: str, logger: Logger):
        self.conf_path = Path(file_to_parse) / "wpa_supplicant" / "wpa_supplicant.conf"
        self.output_dir = Path(output_dir) / "wpa_supplicant"
        self.logger = logger

    def parse(self):
        self.logger.log(f"Starting Wi-Fi supplicant parsing at: {self.conf_path}")

        if not self.conf_path.exists():
            msg = f"wpa_supplicant.conf not found at {self.conf_path}"
            self.logger.log(msg)
            return

        networks = []
        current_network = {}

        try:
            with open(self.conf_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("network={"):
                        current_network = {}
                    elif line.startswith("}"):
                        if current_network:
                            networks.append(current_network)
                    elif "=" in line:
                        key, value = line.split("=", 1)
                        value = value.strip('"')
                        current_network[key.strip()] = value.strip()
        except Exception as e:
            self.logger.log(f"Failed to parse wpa_supplicant.conf: {e}")
            return

        os.makedirs(self.output_dir, exist_ok=True)
        csv_path = self.output_dir / "wifi_profiles.csv"

        try:
            with open(csv_path, "w", newline='', encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["ssid", "psk", "bssid", "priority", "key_mgmt"])
                writer.writeheader()
                for net in networks:
                    writer.writerow({
                        "ssid": net.get("ssid", "N/A"),
                        "psk": net.get("psk", "N/A"),
                        "bssid": net.get("bssid", "N/A"),
                        "priority": net.get("priority", "N/A"),
                        "key_mgmt": net.get("key_mgmt", "N/A")
                    })
            self.logger.log(f"Parsed {len(networks)} Wi-Fi profiles and saved to {csv_path}")
        except Exception as e:
            self.logger.log(f"Failed to write Wi-Fi CSV: {e}")

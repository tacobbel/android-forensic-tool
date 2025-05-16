import os
import csv
import xml.etree.ElementTree as ET
from pathlib import Path
from forensic_app.logger import Logger
from datetime import datetime


class PackagesXmlParser:
    def __init__(self, file_to_parse: str, output_dir: str, logger: Logger):
        self.xml_path = Path(file_to_parse) / "packages" / "packages.xml"
        self.output_dir = Path(output_dir) / "packages"
        self.logger = logger

    def parse(self):
        self.logger.log(f"Starting packages.xml parsing at: {self.xml_path}")

        if not self.xml_path.exists():
            msg = f"packages.xml not found at {self.xml_path}"
            self.logger.log(msg)
            return

        try:
            tree = ET.parse(self.xml_path)
            root = tree.getroot()
        except Exception as e:
            msg = f"Error parsing XML: {e}"
            self.logger.log(msg)
            return

        os.makedirs(self.output_dir, exist_ok=True)
        csv_path = self.output_dir / "packages_info.csv"

        with open(csv_path, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Package name", "Version", "User ID",
                "Install path", "Installed at", "Updated at", "System App?"
            ])

            count = 0
            for pkg in root.findall("package"):
                name = pkg.attrib.get("name", "N/A")
                version = pkg.attrib.get("version", "N/A")
                user_id = pkg.attrib.get("userId", "N/A")
                code_path = pkg.attrib.get("codePath", "N/A")
                ft_raw = pkg.attrib.get("ft", "N/A")
                it_raw = pkg.attrib.get("it", "N/A")
                installed_at = convert_hex_timestamp(ft_raw)
                updated_at = convert_hex_timestamp(it_raw)

                flags = pkg.attrib.get("flags", "0")
                is_system = (
                        "system" in code_path.lower()
                        or (flags.isdigit() and int(flags) & 1 != 0)
                )

                writer.writerow([
                    name, version, user_id, code_path,
                    installed_at, updated_at, "Yes" if is_system else "No"
                ])
                count += 1

        msg = f"packages.xml parsed: {count} packages extracted and saved to: {csv_path}"
        print(msg)
        self.logger.log(msg)

def convert_hex_timestamp(hex_string):
    try:
        timestamp = int(hex_string, 16)
        if timestamp > 1e12:  # miliseconds
            timestamp = timestamp / 1000
        return datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S UTC")
    except:
        return "N/A"
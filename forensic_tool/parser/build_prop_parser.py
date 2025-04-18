import csv
import os
from pathlib import Path


class BuildPropParser:
    def __init__(self, mount_dir: str, output_dir: str):
        self.mount_dir = mount_dir
        self.build_prop_path = Path(self.mount_dir) / "system" / "build.prop"
        self.output_dir = output_dir
        self.keys_to_extract = [
            "ro.build.version.release",
            "ro.build.version.sdk",
            "ro.product.model",
            "ro.product.brand",
            "ro.product.manufacturer",
            "ro.build.id",
            "ro.build.version.incremental"
        ]

    def parse(self):
        parsed_data = {}

        if not os.path.isfile(self.build_prop_path):
            print(f"File not found: {self.build_prop_path}")
            return

        with open(self.build_prop_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or "=" not in line or line.startswith("#"):
                    continue
                key, value = line.split("=", 1)
                if key in self.keys_to_extract:
                    parsed_data[key] = value

        os.makedirs(os.path.join(self.output_dir, "build"), exist_ok=True)
        output_file = os.path.join(self.output_dir, "build", "build_info.csv")
        with open(output_file, "w", encoding="utf-8", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Key", "Value"])
            for key in self.keys_to_extract:
                writer.writerow([key, parsed_data.get(key, "N/A")])

        print(f"build.prop info exported to {output_file}")


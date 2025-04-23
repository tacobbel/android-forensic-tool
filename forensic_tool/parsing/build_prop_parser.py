import csv
import os
from pathlib import Path

from forensic_tool.logger import Logger


class BuildPropParser:
    def __init__(self, file_to_parse: str, output_dir: str, logger: Logger):
        self.input_path = file_to_parse
        self.output_dir = output_dir
        self.logger = logger
        self.build_prop_path = Path(file_to_parse) / "build" / "build.prop"
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
        self.logger.log(f"Starting build.prop parsing at: {self.build_prop_path}")

        parsed_data = {}

        if not os.path.isfile(self.build_prop_path):
            msg = f"build.prop not found at: {self.build_prop_path}"
            print(msg)
            self.logger.log(msg)
            return

        try:
            with open(self.build_prop_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or "=" not in line or line.startswith("#"):
                        continue
                    key, value = line.split("=", 1)
                    if key in self.keys_to_extract:
                        parsed_data[key] = value

            count = len([key for key in self.keys_to_extract if key in parsed_data])


        except Exception as e:
            msg = f"Error while reading build.prop: {e}"
            print(msg)
            self.logger.log(msg)
            return

        try:
            output_subdir = os.path.join(self.output_dir, "build")
            os.makedirs(output_subdir, exist_ok=True)
            output_file = os.path.join(output_subdir, "build_info.csv")

            with open(output_file, "w", encoding="utf-8", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Key", "Value"])
                for key in self.keys_to_extract:
                    writer.writerow([key, parsed_data.get(key, "N/A")])

            msg = f"build.prop parsed: {count} values extracted and saved to: {self.build_prop_path}"
            print(msg)
            self.logger.log(msg)
        except Exception as e:
            msg = f"Failed to export build.prop info: {e}"
            print(msg)
            self.logger.log(msg)

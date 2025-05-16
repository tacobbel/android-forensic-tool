import csv
import os
from pathlib import Path
from forensic_app.logger import Logger
from datetime import datetime, timezone, timedelta

class UidErrorsParser:
    def __init__(self, file_to_parse: str, output_dir: str, logger: Logger):
        self.input_path = Path(file_to_parse) / "uiderrors" / "uiderrors.txt"
        self.output_dir = Path(output_dir) / "uiderrors"
        self.logger = logger

    def parse(self):
        self.logger.log(f"Starting uiderrors.txt parsing at: {self.input_path}")

        if not self.input_path.exists():
            msg = f"uiderrors.txt not found at {self.input_path}"
            self.logger.log(msg)
            return

        os.makedirs(self.output_dir, exist_ok=True)
        output_file = self.output_dir / "uiderrors_summary.csv"

        try:
            with open(self.input_path, "r", encoding="utf-8", errors="ignore") as infile, \
                 open(output_file, "w", encoding="utf-8", newline="") as outfile:
                writer = csv.writer(outfile)
                writer.writerow(["Timestamp", "Message"])

                for line in infile:
                    if ": " not in line:
                        continue
                    timestamp_raw, message = line.strip().split(": ", 1)
                    timestamp_utc = self.convert_to_utc(timestamp_raw.strip())
                    writer.writerow([timestamp_utc, message.strip()])

            msg = f"uiderrors.txt parsed and saved to: {output_file}"
            print(msg)
            self.logger.log(msg)

        except Exception as e:
            msg = f"Error while parsing uiderrors.txt: {e}"
            print(msg)
            self.logger.log(msg)

    def convert_to_utc(self, ts_string: str) -> str:
        try:
            local_dt = datetime.strptime(ts_string, "%d.%m.%y %H:%M")
            local_offset_hours = 2
            utc_dt = local_dt - timedelta(hours=local_offset_hours)
            return utc_dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        except:
            return "N/A"

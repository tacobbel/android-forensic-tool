import csv
import os
from pathlib import Path
from forensic_tool.logger import Logger

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
                    timestamp, message = line.strip().split(": ", 1)
                    writer.writerow([timestamp.strip(), message.strip()])

            msg = f"uiderrors.txt parsed and saved to: {output_file}"
            print(msg)
            self.logger.log(msg)

        except Exception as e:
            msg = f"Error while parsing uiderrors.txt: {e}"
            print(msg)
            self.logger.log(msg)

import sqlite3
import csv
import os
from pathlib import Path
from forensic_tool.logger import Logger

class AccountsDbParser:
    def __init__(self, file_to_parse: str, output_dir: str, logger: Logger):
        self.db_path = Path(file_to_parse) / "accounts" / "accounts.db"
        self.output_dir = Path(output_dir) / "accounts"
        self.logger = logger

    def parse(self):
        self.logger.log(f"Starting accounts.db parsing at: {self.db_path}")

        if not self.db_path.exists():
            msg = f"accounts.db not found at {self.db_path}"
            self.logger.log(msg)
            return

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name, type, password FROM accounts")
            rows = cursor.fetchall()
        except Exception as e:
            self.logger.log(f"Error reading database: {e}")
            return
        finally:
            conn.close()

        os.makedirs(self.output_dir, exist_ok=True)
        csv_path = self.output_dir / "accounts_info.csv"

        try:
            with open(csv_path, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Account Name", "Type", "Password (if any)"])
                for row in rows:
                    writer.writerow(row)
            self.logger.log(f"accounts.db parsed and saved to: {csv_path}")
        except Exception as e:
            self.logger.log(f"Error saving CSV: {e}")

import csv
from collections import Counter

class AccountsAnalyzer:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def analyze(self) -> dict:
        try:
            with open(self.csv_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                accounts = list(reader)
        except Exception as e:
            print(f"Failed to read {self.csv_path}: {e}")
            return {}

        total = len(accounts)
        types = [acc["Type"] for acc in accounts]
        passwords = [acc for acc in accounts if acc["Password (if any)"].strip()]
        type_counter = Counter(types)

        return {
            "Total accounts": total,
            "Accounts with passwords": len(passwords),
            "Top account types": type_counter.most_common(5)
        }

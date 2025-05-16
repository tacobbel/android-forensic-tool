class PackagesAnalyzer:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def analyze(self) -> dict:
        from collections import Counter
        import csv
        from datetime import datetime

        try:
            with open(self.csv_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                packages = list(reader)
        except Exception as e:
            print(f"Failed to read {self.csv_path}: {e}")
            return {}

        total = len(packages)
        system_apps = sum(1 for p in packages if p["System App?"] == "Yes")
        user_apps = total - system_apps

        codepaths = Counter(p["Install path"].split("/")[1] for p in packages if "/" in p["Install path"])

        # find earliest and latest installation time
        def safe_parse(ts): #fallback
            try:
                return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S UTC")
            except:
                return None

        install_times = list(filter(None, (safe_parse(p["Installed at"]) for p in packages)))
        earliest = min(install_times).strftime("%Y-%m-%d") if install_times else "N/A"
        latest = max(install_times).strftime("%Y-%m-%d") if install_times else "N/A"

        return {
            "Total apps": total,
            "System apps": system_apps,
            "User apps": user_apps,
            "Top install dirs": codepaths.most_common(5),
            "Earliest install": earliest,
            "Latest install": latest
        }

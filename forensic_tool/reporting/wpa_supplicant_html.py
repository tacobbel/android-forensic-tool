import os
from forensic_tool.analyzing.wpa_supplicant_analyzer import WpaSupplicantAnalyzer

def generate_wpa_supplicant_section(output_dir: str) -> str:
    analyzer = WpaSupplicantAnalyzer(
        csv_path=os.path.join(output_dir, "wpa_supplicant", "wifi_profiles.csv")
    )
    stats = analyzer.analyze()

    section = ['<details><summary>Wi-Fi profiles analysis (wpa_supplicant.conf)</summary><ul>']
    for key, value in stats.items():
        if isinstance(value, list):
            section.append(f"<li><strong>{key}:</strong><ul>")
            for v in value:
                section.append(f"<li>{v[0]} ({v[1]})</li>")
            section.append("</ul></li>")
        else:
            section.append(f"<li><strong>{key}:</strong> {value}</li>")
    section.append("</ul></details>")
    return "\n".join(section)

def generate_wpa_supplicant_section_sk(output_dir: str) -> str:
    analyzer = WpaSupplicantAnalyzer(
        csv_path=os.path.join(output_dir, "wpa_supplicant", "wifi_profiles.csv")
    )
    stats = analyzer.analyze()

    section = ['<details><summary>Analýza Wi-Fi profilov (wpa_supplicant.conf)</summary><ul>']
    for key, value in stats.items():
        translated_key = translate_key_sk(key)
        if isinstance(value, list):
            section.append(f"<li><strong>{translated_key}:</strong><ul>")
            for v in value:
                section.append(f"<li>{v[0]} ({v[1]})</li>")
            section.append("</ul></li>")
        else:
            section.append(f"<li><strong>{translated_key}:</strong> {value}</li>")
    section.append("</ul></details>")
    return "\n".join(section)

def translate_key_sk(key: str) -> str:
    dictionary = {
        "Total Wi-Fi profiles": "Celkový počet Wi-Fi profilov",
        "Profiles with password (PSK)": "Profily s heslom (PSK)",
        "Profiles with BSSID": "Profily s BSSID",
        "Unique SSIDs": "Jedinečné SSID",
        "Top key management methods": "Najčastejšie metódy správy kľúčov",
    }
    return dictionary.get(key, key)

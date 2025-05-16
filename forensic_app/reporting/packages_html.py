import os
from forensic_app.analyzing.packages_analyzer import PackagesAnalyzer

def generate_packages_section(output_dir: str) -> str:

    analyzer = PackagesAnalyzer(
        csv_path=os.path.join(output_dir, "packages", "packages_info.csv")
    )
    stats = analyzer.analyze()

    section = ['<details><summary>Installed packages analysis (packages.xml)</summary><ul>']
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

def generate_packages_section_sk(output_dir: str) -> str:
    analyzer = PackagesAnalyzer(
        csv_path=os.path.join(output_dir, "packages", "packages_info.csv")
    )
    stats = analyzer.analyze()

    section = ['<details><summary>Analýza nainštalovaných balíkov (packages.xml)</summary><ul>']
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
        "Total apps": "Celkový počet aplikácií",
        "System apps": "Systémové aplikácie",
        "User apps": "Používateľské aplikácie",
        "Top install dirs": "Top inštalačné adresáre",
        "Earliest install": "Najskoršia inštalácia",
        "Latest install": "Najnovšia inštalácia"
    }
    return dictionary.get(key, key)

import os
from forensic_tool.analyzing.uid_errors_analyzer import UidErrorsAnalyzer

def generate_uid_errors_section(output_dir: str) -> str:
    analyzer = UidErrorsAnalyzer(
        csv_path=os.path.join(output_dir, "uiderrors", "uiderrors_summary.csv")
    )
    stats = analyzer.analyze()

    section = ['<details><summary>UID Errors Analysis (uiderrors.txt)</summary><ul>']

    for key, value in stats.items():
        if isinstance(value, list):
            section.append(f"<li><strong>{key}:</strong><ul>")
            for v in value:
                section.append(f"<li>{v[0]} ({v[1]})</li>")
            section.append("</ul></li>")
        else:
            section.append(f"<li><strong>{key}:</strong> {value}</li>")

    section.append('</ul></details>')
    return "\n".join(section)

def generate_uid_errors_section_sk(output_dir: str) -> str:
    analyzer = UidErrorsAnalyzer(
        csv_path=os.path.join(output_dir, "uiderrors", "uiderrors_summary.csv")
    )
    stats = analyzer.analyze()

    section = ['<details><summary>Analýza UID chýb (uiderrors.txt)</summary><ul>']

    for key, value in stats.items():
        translated_key = translate_key_sk(key)
        if isinstance(value, list):
            section.append(f"<li><strong>{translated_key}:</strong><ul>")
            for v in value:
                section.append(f"<li>{v[0]} ({v[1]})</li>")
            section.append("</ul></li>")
        else:
            section.append(f"<li><strong>{translated_key}:</strong> {value}</li>")

    section.append('</ul></details>')
    return "\n".join(section)

def translate_key_sk(key: str) -> str:
    dictionary = {
        "Total entries": "Celkový počet záznamov",
        "First boot time": "Čas prvého spustenia",
        "Entries per day": "Záznamy podľa dňa",
        "Common keywords": "Najčastejšie kľúčové slová"
    }
    return dictionary.get(key, key)

import os
from forensic_tool.analyzing.accounts_analyzer import AccountsAnalyzer

def generate_accounts_section_eng(output_dir: str) -> str:
    analyzer = AccountsAnalyzer(
        csv_path=os.path.join(output_dir, "accounts", "accounts_info.csv")
    )
    stats = analyzer.analyze()

    section = ['<details><summary>Accounts analysis (accounts.db)</summary><ul>']
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

def translate_accounts_key_sk(key: str) -> str:
    return {
        "Total accounts": "Celkový počet účtov",
        "Accounts with passwords": "Účty s heslom",
        "Top account types": "Najčastejšie typy účtov",
    }.get(key, key)

def generate_accounts_section_sk(output_dir: str) -> str:
    analyzer = AccountsAnalyzer(
        csv_path=os.path.join(output_dir, "accounts", "accounts_info.csv")
    )
    stats = analyzer.analyze()

    section = ['<details><summary>Analýza účtov (accounts.db)</summary><ul>']
    for key, value in stats.items():
        sk_key = translate_accounts_key_sk(key)
        if isinstance(value, list):
            section.append(f"<li><strong>{sk_key}:</strong><ul>")
            for v in value:
                section.append(f"<li>{v[0]} ({v[1]})</li>")
            section.append("</ul></li>")
        else:
            section.append(f"<li><strong>{sk_key}:</strong> {value}</li>")
    section.append("</ul></details>")
    return "\n".join(section)

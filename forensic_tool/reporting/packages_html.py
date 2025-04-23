import os

from forensic_tool.analyzing.packages_analyzer import PackagesAnalyzer

def generate_packages_section(output_dir: str) -> str:

    analyzer = PackagesAnalyzer(
        csv_path=os.path.join(output_dir, "packages", "packages_info.csv")
    )
    stats = analyzer.analyze()

    section = ['<details><summary>Installed packages analysis</summary><ul>']
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

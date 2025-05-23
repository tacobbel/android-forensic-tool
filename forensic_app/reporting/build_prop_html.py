from pathlib import Path
import csv

def generate_build_prop_section_eng(output_dir: str) -> str:
    csv_path = Path(output_dir) / "build" / "build_info.csv"
    section_html = [
        '<details>',
        '<summary>Device details (build.prop)</summary>'
    ]

    if not csv_path.exists():
        section_html.append("<p style='color:red;'>File build_info.csv was not found.</p>")
        section_html.append("</details>")
        return "\n".join(section_html)

    build_data = {}
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)
        for key, value in reader:
            build_data[key] = value

    section_html.append("<ul>")
    section_html.append(f"<li><strong>Android version:</strong> {build_data.get('ro.build.version.release', 'N/A')}</li>")
    section_html.append(f"<li><strong>SDK version:</strong> {build_data.get('ro.build.version.sdk', 'N/A')}</li>")
    section_html.append(f"<li><strong>Device model:</strong> {build_data.get('ro.product.model', 'N/A')}</li>")
    section_html.append(f"<li><strong>Manufacturer:</strong> {build_data.get('ro.product.manufacturer', 'N/A')}</li>")
    section_html.append(f"<li><strong>Brand:</strong> {build_data.get('ro.product.brand', 'N/A')}</li>")
    section_html.append(f"<li><strong>Build ID:</strong> {build_data.get('ro.build.id', 'N/A')}</li>")
    section_html.append(f"<li><strong>Build version:</strong> {build_data.get('ro.build.version.incremental', 'N/A')}</li>")
    section_html.append("</ul>")
    section_html.append("</details>")

    return "\n".join(section_html)

def generate_build_prop_section_sk(output_dir: str) -> str:
    csv_path = Path(output_dir) / "build" / "build_info.csv"
    section_html = [
        '<details>',
        '<summary>Detaily zariadenia (build.prop)</summary>'
    ]

    if not csv_path.exists():
        section_html.append("<p style='color:red;'>Súbor build_info.csv nebol nájdený.</p>")
        section_html.append("</details>")
        return "\n".join(section_html)

    build_data = {}
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)
        for key, value in reader:
            build_data[key] = value

    section_html.append("<ul>")
    section_html.append(f"<li><strong>Verzia Androidu:</strong> {build_data.get('ro.build.version.release', 'N/A')}</li>")
    section_html.append(f"<li><strong>SDK verzia:</strong> {build_data.get('ro.build.version.sdk', 'N/A')}</li>")
    section_html.append(f"<li><strong>Model zariadenia:</strong> {build_data.get('ro.product.model', 'N/A')}</li>")
    section_html.append(f"<li><strong>Výrobca:</strong> {build_data.get('ro.product.manufacturer', 'N/A')}</li>")
    section_html.append(f"<li><strong>Značka:</strong> {build_data.get('ro.product.brand', 'N/A')}</li>")
    section_html.append(f"<li><strong>Build ID:</strong> {build_data.get('ro.build.id', 'N/A')}</li>")
    section_html.append(f"<li><strong>Verzia buildu:</strong> {build_data.get('ro.build.version.incremental', 'N/A')}</li>")
    section_html.append("</ul>")
    section_html.append("</details>")

    return "\n".join(section_html)
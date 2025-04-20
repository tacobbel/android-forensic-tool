import csv
from pathlib import Path


def generate_html_report(output_dir: str, html_name: str = "parser_report.html"):
    html_path = Path(output_dir) / html_name
    html_parts = ['<html><head><meta charset="utf-8"><title>Parser Report</title></head><body>',
                  "<h1>Forensic CSV Report</h1>"]
    for csv_path in Path(output_dir).rglob("*.csv"):
        relative_path = csv_path.relative_to(output_dir)
        html_parts.append(f"<h2>{relative_path}</h2>")

        try:
            with open(csv_path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)

                if not rows:
                    html_parts.append("<p><em>No data.</em></p>")
                    continue

                html_parts.append('<table border="1" cellpadding="5" cellspacing="0">')

                for i, row in enumerate(rows):
                    tag = "th" if i == 0 else "td"
                    html_parts.append("<tr>" + "".join(f"<{tag}>{cell}</{tag}>" for cell in row) + "</tr>")

                html_parts.append("</table><br>")
        except Exception as e:
            html_parts.append(f"<p style='color:red;'>Failed to read {csv_path}: {e}</p>")

    html_parts.append("</body></html>")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html_parts))

    print(f"HTML report generated at {html_path}")
    return html_path

from pathlib import Path
from forensic_tool.reporting.build_prop_html import generate_build_prop_section
from forensic_tool.reporting.packages_html import generate_packages_section


def generate_combined_html_report(output_dir: str, html_name: str = "case_report.html"):
    html_path = Path(output_dir) / html_name

    html_parts = [
        '<html>',
        '<head>',
        '<meta charset="utf-8">',
        '<title>Case Report</title>',
        '<style>',
        '''
        body {
            font-family: Ubuntu, sans-serif;
            line-height: 1.6;
            margin: 20px;
        }
        summary {
            cursor: pointer;
            font-size: 1.1em;
            background-color: #f0f0f0;
            padding: 8px 12px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-weight: bold;
            transition: background-color 0.2s ease-in-out;
        }
        summary:hover {
            background-color: #e0e0e0;
        }
        details {
            margin-bottom: 20px;
            border-left: 4px solid #6c757d;
            padding-left: 12px;
        }
        ul {
            list-style-type: disc;
            margin: 10px 0 10px 20px;
        }
        ''',
        '</style>',
        '</head>',
        '<body>',
        "<h1>Case Report</h1>"
    ]

    html_parts.append(generate_build_prop_section(output_dir))
    html_parts.append(generate_packages_section(output_dir))

    # --- USER-DEFINED SECTION START ---
    # you can add new sections to the html report
    # e.g. html_parts.append(generate_your_section(...))
    # --- USER-DEFINED SECTION END ---

    html_parts.append("</body></html>")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html_parts))

    print(f"Overall HTML report generated at {html_path}")
    return html_path

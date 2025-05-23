from pathlib import Path

from forensic_app.reporting.accounts_html import generate_accounts_section_eng, generate_accounts_section_sk
from forensic_app.reporting.build_prop_html import generate_build_prop_section_eng, generate_build_prop_section_sk
from forensic_app.reporting.packages_html import generate_packages_section, generate_packages_section_sk
from forensic_app.reporting.uid_errors_html import generate_uid_errors_section, generate_uid_errors_section_sk
from forensic_app.reporting.wpa_supplicant_html import generate_wpa_supplicant_section, \
    generate_wpa_supplicant_section_sk


def generate_combined_html_report_eng(output_dir: str, html_name: str = "case_report_eng.html"):
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

    html_parts.append(generate_build_prop_section_eng(output_dir))
    html_parts.append(generate_packages_section(output_dir))
    html_parts.append(generate_wpa_supplicant_section(output_dir))
    html_parts.append(generate_accounts_section_eng(output_dir))
    html_parts.append(generate_uid_errors_section(output_dir))

    # --- USER-DEFINED SECTION START ---
    # add new sections to the html report here
    # e.g. html_parts.append(generate_your_new_section(...))
    # --- USER-DEFINED SECTION END ---

    html_parts.append("</body></html>")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html_parts))

    print(f"Overall english HTML report generated at {html_path}")
    return html_path

def generate_combined_html_report_sk(output_dir: str, html_name: str = "case_report_sk.html"):
    html_path = Path(output_dir) / html_name

    html_parts = [
        '<html>',
        '<head>',
        '<meta charset="utf-8">',
        '<title>Forenzná správa</title>',
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
        "<h1>Forenzná správa</h1>"
    ]

    html_parts.append(generate_build_prop_section_sk(output_dir))
    html_parts.append(generate_packages_section_sk(output_dir))
    html_parts.append(generate_wpa_supplicant_section_sk(output_dir))
    html_parts.append(generate_accounts_section_sk(output_dir))
    html_parts.append(generate_uid_errors_section_sk(output_dir))

    # --- USER-DEFINED SECTION START ---
    # add new sections to the html report here
    # e.g. html_parts.append(generate_your_new_section(...))
    # --- USER-DEFINED SECTION END ---

    html_parts.append("</body></html>")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html_parts))

    print(f"Overall slovak HTML report generated at {html_path}")
    return html_path
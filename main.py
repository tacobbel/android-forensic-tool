from forensic_tool.logger import Logger
from forensic_tool.parsing.build_prop_parser import BuildPropParser
from forensic_tool.reporting.overall_html_report import generate_combined_html_report
from forensic_tool.triage import Triage

if __name__ == "__main__":
    mount_dir = "/home/ubuntu/android"
    output_dir = "/home/ubuntu/forensicOutput"

    # triage phase
    system_triage = Triage(mount_dir, output_dir)
    data_triage = Triage(mount_dir, output_dir)
    print("Triage starting")

    system_triage.extract_file("system/build.prop")

    # --- USER-DEFINED SECTION START ---
    # you can add more files for triage
    # e.g. system_triage.extract_file("system/relative_file_path")
    #      data_triage.extract_file("data/relative_file_path")
    # --- USER-DEFINED SECTION END ---

    # logger used by all the parsers
    parser_logger = Logger(log_dir=output_dir, custom_prefix="parser_log")

    # parsing phase
    build_prop_parser = BuildPropParser(output_dir, output_dir, parser_logger)
    build_prop_parser.parse()

    # --- USER-DEFINED SECTION START ---
    # you can add more files to parse using your own parsers
    # e.g. new_parser = YourParser(...)
    #      new_parser.parse()
    # --- USER-DEFINED SECTION END ---

    # reporting phase
    generate_combined_html_report(output_dir)

from forensic_tool.logger import Logger
from forensic_tool.parsing.build_prop_parser import BuildPropParser
from forensic_tool.reporting.html_report import generate_html_report
from forensic_tool.triage import Triage

if __name__ == "__main__":
    mount_dir = "/home/ubuntu/android"
    output_dir = "/home/ubuntu/triageOutput"

    # triage phase
    system_triage = Triage(mount_dir, output_dir)
    print("Triage starting")
    system_triage.extract_file("system/build.prop")

    # logger used by all the parsers
    parser_logger = Logger(log_dir=output_dir, custom_prefix="parser_log")

    # parsing phase
    build_prop_parser = BuildPropParser(mount_dir, output_dir, parser_logger)
    build_props = build_prop_parser.parse()

    # reporting phase
    generate_html_report(output_dir)

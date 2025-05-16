import argparse

from forensic_app.logger import Logger
from forensic_app.parsing.accounts_parser import AccountsDbParser
from forensic_app.parsing.build_prop_parser import BuildPropParser
from forensic_app.parsing.packages_parser import PackagesXmlParser
from forensic_app.parsing.uid_errors_parser import UidErrorsParser
from forensic_app.parsing.wpa_supplicant_parser import WpaSupplicantParser
from forensic_app.reporting.overall_html_report import generate_combined_html_report_eng, generate_combined_html_report_sk
from forensic_app.triage import Triage

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated Android forensic analysis tool")
    parser.add_argument('--mount_dir', required=True, help='Parent directory of mounted Android partitions')
    parser.add_argument('--output_dir', required=True, help='Directory to store output files')

    args = parser.parse_args()
    mount_dir = args.mount_dir
    output_dir = args.output_dir

    # triage phase
    triage = Triage(mount_dir, output_dir)

    print("Triage starting")

    triage.extract_file("system/build.prop")
    triage.extract_file("data/system/packages.xml")
    triage.extract_file("data/system/users/0/accounts.db")
    triage.extract_file("data/misc/wifi/wpa_supplicant.conf")
    triage.extract_file("data/system/uiderrors.txt")


    # --- USER-DEFINED SECTION START ---
    # add more files for triage here
    # e.g. system_triage.extract_file("system/relative_file_path")
    #      data_triage.extract_file("data/relative_file_path")
    # --- USER-DEFINED SECTION END ---

    # logger used by all the parsers
    parser_logger = Logger(log_dir=output_dir, custom_prefix="parser_log")

    # parsing phase
    build_prop_parser = BuildPropParser(output_dir, output_dir, parser_logger)
    build_prop_parser.parse()

    packages_parser = PackagesXmlParser(output_dir, output_dir, parser_logger)
    packages_parser.parse()

    accounts_parser = AccountsDbParser(output_dir, output_dir, parser_logger)
    accounts_parser.parse()

    wpa_supplicant_parser = WpaSupplicantParser(output_dir, output_dir, parser_logger)
    wpa_supplicant_parser.parse()

    uid_errors_parser = UidErrorsParser(output_dir, output_dir, parser_logger)
    uid_errors_parser.parse()

    # --- USER-DEFINED SECTION START ---
    # use new parsers here
    # e.g. new_parser = YourParser(...)
    #      new_parser.parse()
    # --- USER-DEFINED SECTION END ---

    # reporting phase
    generate_combined_html_report_eng(output_dir)
    generate_combined_html_report_sk(output_dir)

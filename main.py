from forensic_tool.parser.build_prop_parser import BuildPropParser
from forensic_tool.triage import Triage

if __name__ == "__main__":
    mount_dir = "/home/ubuntu/android"
    output_dir = "/home/ubuntu/triageOutput"

    system_triage = Triage(mount_dir, output_dir)
    print("Triage starting")
    system_triage.extract_file("system/build.prop")

    build_prop_parser = BuildPropParser(mount_dir, output_dir)
    build_props = build_prop_parser.parse()
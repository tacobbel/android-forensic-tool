from forensic_tool.triage import Triage

if __name__ == "__main__":
    mount_dir = "/home/ubuntu/android"
    output_dir = "/home/ubuntu/triageOutput"

    triage = Triage(mount_dir, output_dir)
    print("Triage starting")
    triage.extract_file("system/build.prop")
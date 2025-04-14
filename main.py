if __name__ == "__main__":
    mount_dir = "mnt/selected_partition"
    output_dir = "triage_output"

    triage = Triage(mount_dir, output_dir)
    triage.extract_build_prop()
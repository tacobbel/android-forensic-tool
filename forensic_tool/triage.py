import os
import shutil

from forensic_tool.logger import Logger


class Triage:
    def __init__(self, mount_dir, output_dir):
        self.mount_dir = mount_dir
        self.output_dir = output_dir
        self.logger = Logger(log_dir=output_dir)

    def extract_file(self, relative_path):
        source_path = os.path.join(self.mount_dir, relative_path)
        self.logger.log(f"Searching for: {source_path}")

        if not os.path.isfile(source_path):
            msg = f"File not found: {source_path}"
            print(msg)
            self.logger.log(msg)
            return

        # file name (e.g. build.prop)
        filename = os.path.basename(relative_path)

        # target directory = file name without extention (e.g. build)
        target_dir_name = filename.split('.')[0]
        target_dir = os.path.join(self.output_dir, target_dir_name)
        os.makedirs(target_dir, exist_ok=True)
        self.logger.log(f"Target directory created: {target_dir}")

        target_file = os.path.join(target_dir, filename)

        try:
            shutil.copy2(source_path, target_file)
            msg = f"File {filename} successfully copied to: {target_file}"
            print(msg)
            self.logger.log(msg)
        except Exception as e:
            msg = f"Error while copying {filename}: {e}"
            print(msg)
            self.logger.log(msg)

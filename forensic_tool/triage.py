import csv
import datetime
import hashlib
import os
import shutil
import threading
from os import PathLike

from forensic_tool.logger import Logger


class Triage:
    def __init__(self, mount_dir, output_dir):
        self.mount_dir = mount_dir
        self.output_dir = output_dir
        self.logger = Logger(log_dir=output_dir)

    def extract_file(self, relative_path: str | PathLike):

        source_path : str = os.path.join(self.mount_dir, relative_path)
        self.logger.log(f"Searching for: {source_path}")

        if not os.path.isfile(source_path):
            msg = f"File not found: {source_path}"
            print(msg)
            self.logger.log(msg)
            return

        # file name (e.g. build.prop)
        filename: str = os.path.basename(relative_path)


        # get and log original time stamps of file
        stat = os.stat(source_path)
        accessed = datetime.datetime.fromtimestamp(stat.st_atime)
        modified = datetime.datetime.fromtimestamp(stat.st_mtime)
        changed = datetime.datetime.fromtimestamp(stat.st_ctime)

        self.logger.log(f"Timestamps for {filename} before copy:")
        self.logger.log(f"  Accessed: {accessed}")
        self.logger.log(f"  Modified: {modified}")
        self.logger.log(f"  Changed : {changed}")

        # target directory = file name without extension (e.g. build)
        target_dir_name = filename.split('.')[0]
        target_dir = os.path.join(self.output_dir, target_dir_name)
        os.makedirs(target_dir, exist_ok=True)
        self.logger.log(f"Target directory created: {target_dir}")

        # compute hash value in the background
        threading.Thread(target=self.compute_and_log_hash, args=(source_path,), daemon=False).start()

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

    def compute_and_log_hash(self, file_path: str):
        sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256.update(chunk)
            hash_value = sha256.hexdigest()
            log_path = os.path.join(self.output_dir, "hashes.csv")
            file_exists = os.path.isfile(log_path)

            with open(log_path, "a", newline='', encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                if not file_exists:
                    writer.writerow(["Filename", "Path", "SHA256", "Timestamp"])
                writer.writerow([
                    os.path.basename(file_path),
                    file_path,
                    hash_value,
                    self.get_standard_timestamp()
                ])
            self.logger.log(f"SHA256 hash saved for {file_path}")
        except Exception as e:
            self.logger.log(f"Error while computing hash for {file_path}: {e}")

    def get_standard_timestamp(self) -> str:
        now_utc = datetime.datetime.now(datetime.timezone.utc)
        local_offset_hours = 2
        local_time = now_utc + datetime.timedelta(hours=local_offset_hours)
        return local_time.strftime(f"%Y-%m-%d %H:%M:%S UTC+{local_offset_hours}")

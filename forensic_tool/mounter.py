import os
import subprocess

class Mounter:
    def __init__(self, image_path, mount_dir):
        self.image_path = image_path
        self.mount_dir = mount_dir
        self.loop_device = None
        self.sector_size = 512

    def list_partitions(self):
        """Získa zoznam partícií a ich sektorov z image súboru."""
        result = subprocess.run(
            ['fdisk', '-l', self.image_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )

        partitions = []
        lines = result.stdout.splitlines()
        parsing = False
        for line in lines:
            if line.strip().startswith("Device"):
                parsing = True
                continue
            if parsing:
                parts = line.split()
                if len(parts) >= 5:
                    start_sector = int(parts[1])
                    partitions.append({
                        "device": parts[0],
                        "start_sector": start_sector
                    })

        return partitions

    def calculate_offset(self, start_sector):
        return start_sector * self.sector_size

    def mount_partition(self, start_sector):
        offset = self.calculate_offset(start_sector)
        os.makedirs(self.mount_dir, exist_ok=True)

        subprocess.run(
            ['mount', '-o', f'ro,loop,offset={offset}', self.image_path, self.mount_dir],
            check=True
        )
        print(f"Mounted partition at offset {offset} to {self.mount_dir}")

    def umount(self):
        subprocess.run(['umount', self.mount_dir], check=False)
        print(f"Unmounted {self.mount_dir}")

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
                if len(parts) >= 5 and parts[1].isdigit():
                    start_sector = int(parts[1])
                    partitions.append({
                        "device": parts[0],
                        "start_sector": start_sector
                    })

        return partitions

    def calculate_offset(self, start_sector):
        return start_sector * self.sector_size

    def setup_loop_device(self, offset):
        """Nastaví loop zariadenie so špecifikovaným offsetom."""
        result = subprocess.run(
            ['losetup', '--find', '--show', '-o', str(offset), self.image_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )
        self.loop_device = result.stdout.strip()
        return self.loop_device

    def mount_partition(self, start_sector):
        offset = self.calculate_offset(start_sector)
        os.makedirs(self.mount_dir, exist_ok=True)

        loop_dev = self.setup_loop_device(offset)

        subprocess.run(
            ['mount', '-o', 'ro', loop_dev, self.mount_dir],
            check=True
        )
        print(f"✅ Partition mounted: {loop_dev} → {self.mount_dir}")

    def umount(self):
        subprocess.run(['umount', self.mount_dir], check=False)
        print(f"🧹 Unmounted {self.mount_dir}")
        if self.loop_device:
            subprocess.run(['losetup', '-d', self.loop_device], check=False)
            print(f"🧹 Detached loop device {self.loop_device}")

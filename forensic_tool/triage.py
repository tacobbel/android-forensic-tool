import os
import shutil

class Triage:
    def __init__(self, mount_dir, output_dir):
        self.mount_dir = mount_dir
        self.output_dir = output_dir

    def extract_build_prop(self):
        # Typická cesta k build.prop v Android image
        build_prop_path = os.path.join(self.mount_dir, 'system', 'build.prop')
        print(build_prop_path)

        print("📁 Obsah adresára:")
        print(os.listdir(os.path.join(self.mount_dir, 'system')))

        if not os.path.isfile(build_prop_path):
            print("❌ Súbor build.prop sa nenašiel.")
            return

        target_dir = os.path.join(self.output_dir, 'build.prop')
        os.makedirs(target_dir, exist_ok=True)

        target_file = os.path.join(target_dir, 'build.prop')
        shutil.copy2(build_prop_path, target_file)

        print(f"✅ Súbor build.prop bol extrahovaný do: {target_file}")

from forensic_tool.mounter import Mounter

if __name__ == "__main__":
    image_path = "test_data/android.dd"
    mount_dir = "mnt/selected_partition"

    mounter = Mounter(image_path, mount_dir)

    try:
        partitions = mounter.list_partitions()
        print("Dostupné partície:")
        for idx, p in enumerate(partitions):
            print(f"{idx}: {p['device']} - Start sector: {p['start_sector']}")

        selected = int(input("Zadaj číslo partície na mount: "))
        selected_partition = partitions[selected]

        mounter.mount_partition(selected_partition["start_sector"])
        print(f"Namountované do {mount_dir}")

    except Exception as e:
        print(f"Chyba: {e}")
    finally:
        input("Stlač ENTER pre odmountovanie...")
        mounter.umount()



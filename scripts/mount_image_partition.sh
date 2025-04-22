#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <path_to_image.dd> <target_directory>"
    exit 1
fi

IMAGE="$1"
TARGET_DIR="$2"

if [ ! -f "$IMAGE" ]; then
    echo "File does not exist: $IMAGE"
    exit 1
fi

mkdir -p "$TARGET_DIR"

echo "Loading image partitions $IMAGE ..."
PARTS=$(fdisk -l "$IMAGE" | grep "^$IMAGE")


if [ -z "$PARTS" ]; then
    echo "No partitions were found."
    exit 1
fi

echo ""
echo "Partitions found:"
printf "%-3s | %-14s | %-12s | %-8s | %-10s | %s\n" "#" "Start (sector)" "End (sector)" "Sectors" "Size" "Partition"
printf "%s\n" "----|----------------|--------------|----------|------------|-----------------------------"
TMP_PARTS=$(mktemp)
SECTOR_SIZE=512

INDEX=1
echo "$PARTS" | while IFS= read -r line; do
    printf "[%2d] %s\n" "$INDEX" "$line"
    echo "$line" >> "$TMP_PARTS"
    INDEX=$((INDEX + 1))
done



echo ""
read -p "Enter the number of the partition to mount: " SELECTED_INDEX

SELECTED_LINE=$(sed -n "${SELECTED_INDEX}p" "$TMP_PARTS")

if [ -z "$SELECTED_LINE" ]; then
    echo "Invalid selection."
    rm "$TMP_PARTS"
    exit 1
fi

SELECTED_NAME=$(echo "$SELECTED_LINE" | sed -E 's/^(.+\.dd[0-9]+)\s+.*/\1/')
SELECTED_OFFSET=$(echo "$SELECTED_LINE" | sed -E 's/^.+\.dd[0-9]+\s+([0-9]+).*/\1/')

if ! [[ "$SELECTED_OFFSET" =~ ^[0-9]+$ ]]; then
    echo "Invalid offset extracted: '$SELECTED_OFFSET'"
    exit 1
fi

BYTE_OFFSET=$((SELECTED_OFFSET * SECTOR_SIZE))
PART_SUFFIX=$(basename "$SELECTED_NAME" | grep -oE 'dd[0-9]+')

ALLOWED_NAMES=("system" "data")

echo ""
echo "Allowed names for mount directory: ${ALLOWED_NAMES[*]}"
read -p "Enter the name of the directory to mount the partition into: " CUSTOM_NAME

VALID=false
for name in "${ALLOWED_NAMES[@]}"; do
    if [[ "$CUSTOM_NAME" == "$name" ]]; then
        VALID=true
        break
    fi
done

if [ "$VALID" = false ]; then
    echo "Invalid name. Only the following are allowed: ${ALLOWED_NAMES[*]}"
    rm "$TMP_PARTS"
    exit 1
fi

MOUNT_POINT="$TARGET_DIR/$CUSTOM_NAME"
mkdir -p "$MOUNT_POINT"

echo "Mounting partition $SELECTED_NAME to $MOUNT_POINT ..."

LOOP_DEVICE=$(sudo losetup --find --show --offset $BYTE_OFFSET "$IMAGE")
sudo mount "$LOOP_DEVICE" "$MOUNT_POINT"

if [ $? -eq 0 ]; then
    echo "Successfully mounted to $MOUNT_POINT"
else
    echo "Failed to mount the selected partition. Make sure the partition contains a supported filesystem."
fi

rm "$TMP_PARTS"


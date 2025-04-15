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
echo "$PARTS" | while read -r line; do
    START=$(echo "$line" | awk '{print $2}')
    END=$(echo "$line" | awk '{print $3}')
    NAME=$(echo "$line" | awk '{print $1}')
    
    SECTORS=$((END - START + 1))
    SIZE_BYTES=$((SECTORS * SECTOR_SIZE))
    
    if [ "$SIZE_BYTES" -lt $((1024*1024)) ]; then
    SIZE_KB=$(awk "BEGIN {printf \"%.1f\", $SIZE_BYTES / 1024}")
    SIZE_HR="${SIZE_KB} KB"
    elif [ "$SIZE_BYTES" -lt $((1024*1024*1024)) ]; then
    SIZE_MB=$(awk "BEGIN {printf \"%.1f\", $SIZE_BYTES / (1024*1024)}")
    SIZE_HR="${SIZE_MB} MB"
    else
    SIZE_GB=$(awk "BEGIN {printf \"%.2f\", $SIZE_BYTES / (1024*1024*1024)}")
    SIZE_HR="${SIZE_GB} GB"
    fi

    printf "[%2d] | %14d | %12d | %8d | %10s | %s\n" \
    "$INDEX" "$START" "$END" "$SECTORS" "$SIZE_HR" "$NAME"


    echo "$START:$NAME" >> "$TMP_PARTS"
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

SELECTED_OFFSET=$(echo "$SELECTED_LINE" | cut -d: -f1)
SELECTED_NAME=$(echo "$SELECTED_LINE" | cut -d: -f2)

BYTE_OFFSET=$((SELECTED_OFFSET * SECTOR_SIZE))
PART_SUFFIX=$(basename "$SELECTED_NAME" | grep -oE 'dd[0-9]+')

read -p "Enter the name of the directory to mount the partition into (leave empty for default name): " CUSTOM_NAME

if [ -z "$CUSTOM_NAME" ]; then
    # fallback: use name of the partition (e.g. android.dd1)
    CUSTOM_NAME=$(basename "$SELECTED_NAME")
fi

MOUNT_POINT="$TARGET_DIR/$CUSTOM_NAME"
mkdir -p "$MOUNT_POINT"

echo "Mounting partition $SELECTED_NAME to $MOUNT_POINT ..."

sudo mount -o loop,offset=$BYTE_OFFSET "$IMAGE" "$MOUNT_POINT"

if [ $? -eq 0 ]; then
    echo "✅ Successfully mounted to $MOUNT_POINT"
else
    echo "❌ Failed to mount the selected partition. Make sure the partition contains a supported filesystem."
fi

rm "$TMP_PARTS"


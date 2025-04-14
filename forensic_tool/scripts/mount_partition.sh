#!/bin/bash

IMAGE=$1
MOUNTPOINT=$2
START_SECTOR=$3
SECTOR_SIZE=512

OFFSET=$((START_SECTOR * SECTOR_SIZE))

# Vytvor mount point ak neexistuje
mkdir -p "$MOUNTPOINT"

# Mountni partíciu s offsetom
sudo mount -o loop,ro,offset=$OFFSET "$IMAGE" "$MOUNTPOINT"

# Vypíš výsledok
echo "✅ Mounted $IMAGE (offset=$OFFSET) → $MOUNTPOINT"

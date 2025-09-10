#!/bin/bash

# CONFIGURATION
SPLUNK_DB="/opt/splunk/var/lib/splunk"
ARCHIVE_DIR="/mnt/archive/splunk_buckets"
DAYS_OLD=180  # Change this to your threshold
MANIFEST="$ARCHIVE_DIR/manifest.csv"

# Create archive directory and manifest
mkdir -p "$ARCHIVE_DIR"
echo "Index,Bucket,StartEpoch,EndEpoch,SizeMB,OriginalPath" > "$MANIFEST"

# Loop through all indexes
for index in $(ls "$SPLUNK_DB"); do
  COLDDIR="$SPLUNK_DB/$index/colddb"
  [ -d "$COLDDIR" ] || continue

  echo "Scanning index: $index"

  # Find bucket directories older than specified days
  find "$COLDDIR" -maxdepth 1 -type d -name 'db_*' -mtime +$DAYS_OLD | while read bucket_path; do
    bucket_name=$(basename "$bucket_path")
    size_mb=$(du -sm "$bucket_path" | cut -f1)

    # Extract time range from bucket name (rough estimate)
    start_epoch=$(echo "$bucket_name" | cut -d'_' -f2)
    end_epoch=$(echo "$bucket_name" | cut -d'_' -f3)

    # Archive bucket
    archive_path="$ARCHIVE_DIR/$index/$bucket_name"
    mkdir -p "$(dirname "$archive_path")"
    mv "$bucket_path" "$archive_path"

    # Log to manifest
    echo "$index,$bucket_name,$start_epoch,$end_epoch,$size_mb,$bucket_path" >> "$MANIFEST"

    echo "Archived $bucket_name from $index"
  done
done

echo "✅ Archive complete. Manifest saved to $MANIFEST"

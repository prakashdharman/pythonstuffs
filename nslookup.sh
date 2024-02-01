#!/bin/bash

# Check if a file is provided as an argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

filename=$1

# Check if the file exists
if [ ! -f "$filename" ]; then
    echo "File $filename not found!"
    exit 1
fi

# Read the file line by line
while IFS= read -r line; do
    # Extract IP and hostname from each line
    ip=$(echo "$line" | awk '{print $1}')
    hostname=$(echo "$line" | awk '{print $2}')
    
    # Print IP and hostname
    echo "IP: $ip, Hostname: $hostname"
done < "$filename"

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
while IFS= read -r hostname; do
    # Get IP address corresponding to the hostname
    ip=$(host "$hostname" | awk '/has address/ {print $4}')
    
    # Print IP and hostname
    echo "$ip $hostname"
done < "$filename"

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
while read -r line; do
    # Extract IP and hostname from each line
    ip=$(echo "$line" | awk '{print $1}')
    hostname=$(echo "$line" | awk '{$1=""; print $0}')
    
    # Print IP and hostname in desired format
    echo -n "$ip ($hostname)"
done < "$filename"

# Print a newline character at the end
echo

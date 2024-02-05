# Check if filename is provided as an argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 filename"
    exit 1
fi

filename=$1

# Check if the file exists
if [ ! -f "$filename" ]; then
    echo "File '$filename' not found."
    exit 1
fi

# Read each line from the file
while IFS=' ' read -r ip hostname; do
    # Format the output
    echo "$ip ($hostname)"
done < "$filename"

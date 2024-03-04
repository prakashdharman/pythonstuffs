import subprocess
from datetime import datetime

# Define the command
command = ['splunk', 'show', 'shcluster-status']

# Execute the command and capture the output
try:
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    output = result.stdout
except subprocess.CalledProcessError as e:
    print("Error executing command:", e)
    output = ""

# Get the current time
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Format the output with the timestamp
output_with_time = f"{current_time}\n{output}\n"

# Write the output to a file
with open('shcluster_status_output.txt', 'a') as file:
    file.write(output_with_time)

print("Output saved to shcluster_status_output.txt")

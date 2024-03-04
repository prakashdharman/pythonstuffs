import subprocess
import time

# Function to execute the command and write output to file
def execute_and_write():
    # Define the command
    command = ['splunk', 'show', 'shcluster-status']

    # Execute the command and capture the output
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, universal_newlines=True)
        output = result.stdout
    except subprocess.CalledProcessError as e:
        print("Error executing command:", e)
        output = ""

    # Write the output to the file
    with open('shcluster_status_output.txt', 'a') as file:
        file.write(output)

    print("Output saved to shcluster_status_output.txt")

# Main loop to execute every 30 seconds
while True:
    execute_and_write()
    time.sleep(30)

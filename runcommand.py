import subprocess
import logging
import schedule
import time

# Configure logging
logging.basicConfig(filename='service_restart.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def restart_service(server, service_name):
    try:
        # SSH command to restart the service
        ssh_command = f"ssh {server} 'sudo service {service_name} restart'"
        
        # Execute the SSH command using subprocess
        process = subprocess.Popen(ssh_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        # Log the result
        if process.returncode == 0:
            logging.info(f"Service restarted successfully on {server}")
            logging.info(stdout.decode())
        else:
            logging.error(f"Error occurred while restarting service on {server}")
            logging.error(stderr.decode())
    except Exception as e:
        logging.error(f"An error occurred while restarting service on {server}: {e}")

def restart_services(servers, service_name):
    for server in servers:
        restart_service(server, service_name)

def main():
    # Server configurations
    servers = [
        'username1@server1.example.com',
        'username2@server2.example.com',
        # Add more servers as needed
    ]
    service_name = 'your_service_name_here'

    # Schedule service restarts
    schedule.every(12).hours.do(restart_services, servers=servers, service_name=service_name)

    # Main loop to execute scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()

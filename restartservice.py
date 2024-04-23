import subprocess
import logging
import time

# Configure logging
logging.basicConfig(filename='service_restart.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Function to restart service
def restart_service(service_name):
    try:
        subprocess.run(['sudo', 'systemctl', 'restart', service_name], check=True)
        logging.info(f"Service {service_name} restarted successfully")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to restart service {service_name}: {e}")

if __name__ == "__main__":
    # Specify the service name
    service_name = "your_service_name"

    while True:
        restart_service(service_name)
        time.sleep(12 * 60 * 60)  # Sleep for 12 hours before restarting again

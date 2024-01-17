import logging
from logging.handlers import TimedRotatingFileHandler

# Set up logging to write logs to both the console and a file with rotation
log_file_path = '/path/to/logs/logfile.log'

# Configure the root logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a console handler and set its level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a file handler with rotation
file_handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1, backupCount=4)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Add the handlers to the root logger
logging.getLogger().addHandler(console_handler)
logging.getLogger().addHandler(file_handler)

# ... (rest of the script)


import ipaddress

class FileDownloader:
    # ... (existing code)

    def create_csv(self, csv_output_path, header):
        try:
            if os.path.exists(self.local_filepath):
                with open(self.local_filepath, 'r') as input_file, open(csv_output_path, 'w') as output_csv:
                    logger.info(f"Writing CSV file to {csv_output_path}")
                    start_time = time.time()
                    output_csv.write(f"{header}\n")  # CSV header

                    for line in input_file:
                        # Skip commented lines
                        if not line.startswith("#"):
                            line = line.strip()
                            if '/' in line:  # Check if the line is a CIDR notation
                                try:
                                    ip_network = ipaddress.IPv4Network(line, strict=False)
                                    for ip_address in ip_network:
                                        output_csv.write(f"{ip_address}\n")
                                except ValueError as e:
                                    logger.error(f"Error parsing CIDR {line}: {str(e)}")
                            else:
                                output_csv.write(f"{line}\n")

                    create_csv_time = time.time() - start_time
                    logger.info(f"Wrote CSV file to {csv_output_path} in {create_csv_time:.2f} seconds")

        except Exception as e:
            logger.error(f"Error creating CSV file: {str(e)}")



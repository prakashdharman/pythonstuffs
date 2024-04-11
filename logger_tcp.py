import logging
import socket
import time

def log_to_tcp(host, port, message):
    try:
        # Create a TCP socket
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to the TCP listener
        tcp_socket.connect((host, port))
        
        # Send the log message over the socket
        tcp_socket.sendall(message.encode())
        
        # Close the TCP socket
        tcp_socket.close()
    except Exception as e:
        print("Error while logging:", e)

# Configure logging
logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)

# Create a TCP handler
host = 'localhost'
port = 9999
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def log_tcp(message):
    log_to_tcp(host, port, message)

tcp_handler = logging.StreamHandler()
tcp_handler.emit = log_tcp
tcp_handler.setFormatter(formatter)
logger.addHandler(tcp_handler)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Log some messages
for i in range(5):
    logger.info("This is log message %d" % i)
    time.sleep(1)  # Sleep for 1 second between log messages

# Close the TCP handler (there's no need to close console handler)
logger.removeHandler(tcp_handler)

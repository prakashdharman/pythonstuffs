import logging
import logging.handlers
import socket
import ssl
import time

# Configure logging
logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)

# Create a TCP socket
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Wrap the socket with SSL/TLS
ssl_socket = ssl.wrap_socket(tcp_socket, ssl_version=ssl.PROTOCOL_TLS)

# Connect to the TCP listener
ssl_socket.connect(('localhost', 9999))

# Create a socket handler with the SSL socket
tcp_handler = logging.StreamHandler(ssl_socket)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
tcp_handler.setFormatter(formatter)

# Add the TCP handler to the logger
logger.addHandler(tcp_handler)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Add the console handler to the logger
logger.addHandler(console_handler)

# Log some messages
for i in range(5):
    logger.info("This is log message %d" % i)
    time.sleep(1)  # Sleep for 1 second between log messages

# Close the SSL socket
ssl_socket.close()

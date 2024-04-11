import logging
import socket
import time

def log_to_tcp(host, port, record):
    try:
        # Create a TCP socket
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to the TCP listener
        tcp_socket.connect((host, port))
        
        # Send the log message over the socket
        tcp_socket.sendall(record.encode())
        
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

def log_tcp(record):
    log_to_tcp(host, port, formatter.format(record))

tcp_handler = logging.StreamHandler()
tcp_handler.emit = log_tcp
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




import socket

def send_test_message(host, port, message):
    try:
        # Create a TCP socket
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to the TCP listener
        tcp_socket.connect((host, port))
        
        # Send the test message over the socket
        tcp_socket.sendall(message.encode())
        
        # Close the TCP socket
        tcp_socket.close()
        print("Test message sent successfully.")
    except Exception as e:
        print("Error while sending test message:", e)

# Example usage: Replace 'localhost', 9999, and "Test message" with your desired host, port, and message.
send_test_message('localhost', 9999, "Test message")



"import socket; sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM); sock.connect(('localhost', 9999)); sock.sendall(b'Test message'); sock.close()"



import logging
import socket
import time

def send_log_to_tcp(host, port, message):
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
        print("Error while sending log message:", e)

# Configure logging
logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)

# Create a TCP handler
host = '10.1.134'
port = 10838
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def log_to_tcp(record):
    send_log_to_tcp(host, port, formatter.format(record))

tcp_handler = logging.StreamHandler()
tcp_handler.emit = log_to_tcp
tcp_handler.setFormatter(formatter)
logger.addHandler(tcp_handler)

# Log some messages
for i in range(5):
    logger.info("This is log message %d" % i)
    time.sleep(1)  # Sleep for 1 second between log messages

# Close the TCP handler
logger.removeHandler(tcp_handler)


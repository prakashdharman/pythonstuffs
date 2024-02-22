import socket

def check_connectivity(host, port):
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set timeout to 2 seconds
        sock.settimeout(2)
        
        # Attempt to connect to the host/port
        sock.connect((host, port))
        print(f"Connected to {host} on port {port}")
        return True
    except Exception as e:
        print(f"Connection to {host} on port {port} failed: {e}")
        return False
    finally:
        # Close the socket
        sock.close()

def main():
    hosts = ["example.com", "google.com", "facebook.com"]
    ports = [80, 443, 22]  # Example list of ports to check
    
    for host in hosts:
        for port in ports:
            check_connectivity(host, port)

if __name__ == "__main__":
    main()





## Check the connection between hosts

import socket
import time

# Define your server IP addresses
servers = ['server1_ip', 'server2_ip', 'server3_ip', 'server4_ip', 'server5_ip']

def check_connectivity(server_ip, port):
    try:
        # Attempt to create a socket connection to the server
        socket.create_connection((server_ip, port), timeout=5)
        return True  # Connection successful
    except Exception as e:
        return False  # Connection failed

def log_failure(server_ip):
    with open('connectivity_logs.txt', 'a') as f:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] Failed to connect to server {server_ip} on port 8089\n")

def main():
    while True:
        for server_ip in servers:
            if not check_connectivity(server_ip, 8089):
                log_failure(server_ip)
        time.sleep(60)  # Check every 60 seconds

if __name__ == "__main__":
    main()


## more detailed and running from central server

import subprocess
import socket
import time

# SSH username and path to the SSH private key
ssh_username = "your_username"
ssh_key_path = "/path/to/your/private/key"

# Define your server IP addresses and port
servers = [('server1_ip', 8089), ('server2_ip', 8089), ('server3_ip', 8089), ('server4_ip', 8089), ('server5_ip', 8089)]

def check_connectivity(server_ip, port):
    try:
        # Attempt to create a socket connection to the server
        with socket.create_connection((server_ip, port), timeout=5) as sock:
            return True  # Connection successful
    except Exception as e:
        return False  # Connection failed

def log_failure(source_server, destination_server):
    with open('connectivity_logs.txt', 'a') as f:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{timestamp}] Failed to connect from {source_server} to {destination_server} on port 8089\n")

def main():
    current_server = socket.gethostname()  # Get the current server's hostname
    
    for destination_server, port in servers:
        if destination_server != current_server:
            ssh_command = f'ssh -i {ssh_key_path} {ssh_username}@{destination_server} "python -c \\"import socket; \
                            sock = socket.create_connection((\'{destination_server}\', {port}), timeout=5); \
                            sock.close()\\""'

                            

            try:
                subprocess.check_call(ssh_command, shell=True)
            except subprocess.CalledProcessError:
                log_failure(current_server, destination_server)

if __name__ == "__main__":
    main()

                log_failure(current_server, destination_server)

if __name__ == "__main__":
    main()

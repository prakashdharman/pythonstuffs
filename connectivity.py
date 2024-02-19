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

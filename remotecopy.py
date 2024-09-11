import subprocess
import logging
import os
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FileTransferManager:
    """Class to handle file transfer operations to multiple servers."""

    def __init__(self, servers, local_files, remote_temp_dir, final_destination, ssh_key_path, main_user, become_user):
        self.servers = servers
        self.local_files = local_files
        self.remote_temp_dir = remote_temp_dir
        self.final_destination = final_destination
        self.ssh_key_path = ssh_key_path
        self.main_user = main_user
        self.become_user = become_user

    def run_command(self, command):
        """Run a shell command and log output/errors."""
        logging.info(f"Running command: {command}")
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode != 0:
            logging.error(f"Command failed: {result.stderr.decode('utf-8')}")
            raise Exception(f"Command failed: {result.stderr.decode('utf-8')}")
        
        logging.info(f"Command output: {result.stdout.decode('utf-8')}")
        return result.stdout.decode('utf-8')

    def copy_files_to_server(self, server):
        """Copy files to the remote server using scp."""
        try:
            for local_file in self.local_files:
                command = f"scp -i {self.ssh_key_path} {local_file} {self.main_user}@{server}:{self.remote_temp_dir}"
                self.run_command(command)
        except Exception as e:
            logging.error(f"Failed to copy files to server {server}: {e}")
            raise

    def switch_user_and_move_files(self, server):
        """Switch to the 'become' user and move files to the final destination using ssh."""
        try:
            # Command to switch to the become_user and move files
            commands = [
                f"sudo -u {self.become_user} mv {self.remote_temp_dir}/* {self.final_destination}",
                f"sudo -u {self.become_user} chown {self.become_user}:{self.become_user} {self.final_destination}/*"
            ]
            
            for command in commands:
                ssh_command = f"ssh -i {self.ssh_key_path} {self.main_user}@{server} '{command}'"
                self.run_command(ssh_command)
        except Exception as e:
            logging.error(f"Failed to move files as '{self.become_user}' on server {server}: {e}")
            raise

    def process_servers(self):
        """Process the list of servers and copy files as 'main_user', then move as 'become_user'."""
        for server in self.servers:
            logging.info(f"Processing server: {server}")
            try:
                # Copy files to the remote temp directory using scp
                self.copy_files_to_server(server)

                # Switch to 'become_user' and move the files to the final destination
                self.switch_user_and_move_files(server)

            except Exception as e:
                logging.error(f"An error occurred on server {server}: {e}")
            finally:
                logging.info(f"Completed processing for server: {server}")

# Example usage in another script

if __name__ == "__main__":
    # Check if required parameters are passed as arguments
    if len(sys.argv) < 5:
        print("Usage: python file_transfer_manager.py /path/to/private/key main_user become_user")
        sys.exit(1)

    # Get SSH key path, main user, and become user from the command-line arguments
    ssh_key_path = sys.argv[1]
    main_user = sys.argv[2]
    become_user = sys.argv[3]

    # List of servers to process
    servers = [
        "server1.example.com",
        "server2.example.com"
    ]

    # List of local files to copy
    local_files = [
        "/path/to/local/file1",
        "/path/to/local/file2"
    ]

    # Remote temporary directory where files will be copied
    remote_temp_dir = "/tmp/upload"

    # Final destination where 'become_user' will move the files
    final_destination = "/var/log/telegraf"

    # Create an instance of FileTransferManager
    manager = FileTransferManager(
        servers=servers,
        local_files=local_files,
        remote_temp_dir=remote_temp_dir,
        final_destination=final_destination,
        ssh_key_path=ssh_key_path,
        main_user=main_user,
        become_user=become_user
    )

    # Process all servers
    manager.process_servers()

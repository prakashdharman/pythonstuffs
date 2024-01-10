#!/usr/bin/env python3

import requests
import os
import logging
import time
import subprocess
import sys

class FileDownloader:
    def __init__(self, url, local_filepath, backup_dir, proxies=None):
        self.url = url
        self.local_filepath = local_filepath
        self.backup_dir = backup_dir
        self.proxies = proxies

    def fetch_and_save(self):
        os.makedirs(self.backup_dir, exist_ok=True)

        # Move existing files to the backup directory with date and time
        for i in range(9, 0, -1):
            old_filepath = f"{self.local_filepath}.{i}"
            if os.path.exists(old_filepath):
                timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
                new_filepath = os.path.join(self.backup_dir, f"{os.path.basename(self.local_filepath)}_{timestamp}_{i}.dat")
                os.rename(old_filepath, new_filepath)

        # Move the current file to backup if it exists
        if os.path.exists(self.local_filepath):
            timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
            backup_filepath = os.path.join(self.backup_dir, f"{os.path.basename(self.local_filepath)}_{timestamp}_1.dat")
            os.rename(self.local_filepath, backup_filepath)

        try:
            # Fetch and save the new file
            logger.info(f"Fetching data from {self.url}")
            start_time = time.time()
            response = requests.get(self.url)
            #response = requests.get(self.url, proxies=self.proxies)
            response.raise_for_status()  # Raise HTTPError for bad responses
            download_time = time.time() - start_time
            logger.info(f"Fetched data from {self.url} in {download_time:.2f} seconds")

            with open(self.local_filepath, 'wb') as file:
                logger.info(f"Writing response to {self.local_filepath}")
                start_time = time.time()
                file.write(response.content)
                save_time = time.time() - start_time
                logger.info(f"Wrote response to {self.local_filepath} in {save_time:.2f} seconds")

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching or saving data: {str(e)}")

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
                            ip_address = line.strip()
                            output_csv.write(f"{ip_address}\n")
                    create_csv_time = time.time() - start_time
                    logger.info(f"Wrote CSV file to {csv_output_path} in {create_csv_time:.2f} seconds")

        except Exception as e:
            logger.error(f"Error creating CSV file: {str(e)}")

    def copy_to_remote(self, remote_host, remote_user, remote_key_path, remote_dest):
        try:
            # Secure copy the local CSV file to the remote machine
            subprocess.run([
                'scp',
                '-i', remote_key_path,
                self.local_filepath,
                f"{remote_user}@{remote_host}:{remote_dest}"
            ], check=True)

            # Run commands on the remote machine to switch user and move the file
            subprocess.run([
                'ssh',
                '-i', remote_key_path,
                f"{remote_user}@{remote_host}",
                f"sudo -u service_splunk mv {remote_dest}{os.path.basename(self.local_filepath)} /opt/splunk/etc/apps/prakash/lookups/"
            ], check=True)

            logger.info(f"File successfully copied to {remote_host}:{remote_dest}")

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to copy file to {remote_host}:{remote_dest}. Error: {e}")

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")

def main():
    # Set up proxy information
    proxies = {
        'http': 'http://your_proxy_address:your_proxy_port',
        'https': 'https://your_proxy_address:your_proxy_port',
    }

    # Set up other variables
    anon_url = "https://iplists.firehol.org/files/firehol_anonymous.netset"
    tor_url = "https://iplists.firehol.org/files/dm_tor.ipset"
    download_path = "./firehol/"
    backup_dir = "./firehol_backup/"
    csv_output_anon_path = os.path.join(download_path, "firehol.csv")
    csv_output_tor_path = os.path.join(download_path, "dm_tor.csv")

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    global logger
    logger = logging.getLogger(__name__)

    # Download and save anonymous file
    downloader_anon = FileDownloader(anon_url, os.path.join(download_path, "firehol_anonymous.netset"), backup_dir, proxies=proxies)
    downloader_anon.fetch_and_save()

    # Download and save tor file
    downloader_tor = FileDownloader(tor_url, os.path.join(download_path, "dm_tor.ipset"), backup_dir, proxies=proxies)
    downloader_tor.fetch_and_save()

    # Create CSV files
    downloader_anon.create_csv(csv_output_anon_path, "ip_address")
    downloader_tor.create_csv(csv_output_tor_path, "ip_sets")

    # List of remote hosts
    remote_hosts = ['remote_host1', 'remote_host2']  # Add your remote hosts here

    # SSH parameters for autoservice user
    remote_user = 'autoservice'
    remote_key_path = '/path/to/autoservice_private_key'

    # Remote destination directory
    remote_dest = '/tmp/'

    for host in remote_hosts:
        # Copy files to remote hosts
        logger.info(f"Copying files to {host}...")
        #downloader_anon.copy_to_remote(host, remote_user, remote_key_path, remote_dest)
        #downloader_tor.copy_to_remote(host, remote_user, remote_key_path, remote_dest)

if __name__ == "__main__":
    try:
        main()
        sys.exit(0)  # Exit with status code 0 for success
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)  # Exit with a non-zero status code for error

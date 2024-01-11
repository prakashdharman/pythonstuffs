import socket  # Import the socket module for getting the host name

# ... (rest of the code remains unchanged)

def main():
    # Get the host name
    host_name = socket.gethostname()

    # Set up proxy information based on the host name
    if 'test' in host_name:
        proxies = {
            'http': 'http://test_proxy_address:test_proxy_port',
            'https': 'https://test_proxy_address:test_proxy_port',
        }
    elif 'dev' in host_name:
        proxies = {
            'http': 'http://dev_proxy_address:dev_proxy_port',
            'https': 'https://dev_proxy_address:dev_proxy_port',
        }
    else:
        proxies = None  # No proxies for other hosts

    # ... (rest of the code remains unchanged)

    # Download and save anonymous file
    downloader_anon = FileDownloader(anon_url, os.path.join(download_path, "firehol_anonymous.netset"), backup_dir, proxies=proxies)
    downloader_anon.fetch_and_save()

    # Create CSV for anonymous file
    downloader_anon.create_csv(csv_output_anon_path, "ip_address")

    # Download and save tor file
    downloader_tor = FileDownloader(tor_url, os.path.join(download_path, "dm_tor.ipset"), backup_dir, proxies=proxies)
    downloader_tor.fetch_and_save()

    # Create CSV for tor file
    downloader_tor.create_csv(csv_output_tor_path, "ip_sets")

    # ... (rest of the code remains unchanged)

if __name__ == "__main__":
    main()


-----

import os

# ... (previous code remains unchanged)

def get_host_name():
    try:
        return os.uname().nodename  # For Unix-like systems
    except AttributeError:
        return os.environ.get('COMPUTERNAME', os.environ.get('HOSTNAME', 'unknown'))

def main():
    # Get the host name
    host_name = get_host_name()

    # Set up proxy information based on the host name
    if host_name.endswith('t'):  # Check if the host name ends with 't' for test
        proxies = {
            'http': 'http://test_proxy_address:test_proxy_port',
            'https': 'https://test_proxy_address:test_proxy_port',
        }
        remote_hosts = ['test_remote_host1', 'test_remote_host2']  # Add your test remote hosts here
    elif host_name.endswith('d'):  # Check if the host name ends with 'd' for dev
        proxies = {
            'http': 'http://dev_proxy_address:dev_proxy_port',
            'https': 'https://dev_proxy_address:dev_proxy_port',
        }
        remote_hosts = ['dev_remote_host1', 'dev_remote_host2']  # Add your dev remote hosts here
    else:
        proxies = None  # No proxies for other hosts
        remote_hosts = []  # No remote hosts for other hosts

    # ... (rest of the code remains unchanged)

    # List of remote hosts
    for host in remote_hosts:
        # Copy files to remote hosts
        logger.info(f"Copying files to {host}...")
        downloader_anon.copy_to_remote(host, remote_user, remote_key_path, remote_dest)
        downloader_tor.copy_to_remote(host, remote_user, remote_key_path, remote_dest)

# ... (rest of the code remains unchanged)

if __name__ == "__main__":
    main()

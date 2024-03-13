#!/usr/bin/env python3.11
import requests
import xml.etree.ElementTree as ET
import csv
import getpass
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class InstalledAppsReport:
    def __init__(self, splunk_hosts_file, splunk_port):
        self.splunk_hosts = self.read_hosts_from_file(splunk_hosts_file)
        self.splunk_port = splunk_port
        self.splunk_username = input("Enter your Splunk username: ")
        self.splunk_password = getpass.getpass("Enter your Splunk password: ")
        self.reports = self.generate_reports()

    def read_hosts_from_file(self, splunk_hosts_file):
        with open(splunk_hosts_file, 'r') as file:
            return [line.strip() for line in file.readlines()]

    def retrieve_installed_apps(self, splunk_host):
        url = f'https://{splunk_host}:{self.splunk_port}/services/apps/local'
        response = requests.get(url, auth=(self.splunk_username, self.splunk_password), verify=False)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the XML response
        root = ET.fromstring(response.text)

        # Define namespace mappings
        namespaces = {
            'atom': 'http://www.w3.org/2005/Atom',
            'ns0': 'http://www.w3.org/2005/Atom',  # Mapping for ns0 namespace
            'ns1': 'http://dev.splunk.com/ns/rest'  # Mapping for ns1 namespace
        }

        # Find all <entry> elements in the XML tree using XPath with namespaces
        apps = root.findall('.//ns0:entry', namespaces)

        # Initialize a list to store installed apps
        installed_apps = []

        # Iterate over each <entry> element to extract app name and version
        for app in apps:
            # Find the <title> element within each <entry>
            app_name_element = app.find('./ns0:title', namespaces)

            # Extract app name if the <title> element is found
            if app_name_element is not None:
                app_name = app_name_element.text.strip()
                app_version = None  # Initialize version to None

                # Find the <content> element within each <entry>
                content_element = app.find('./ns0:content', namespaces)

                # Extract app version only if the content element is found
                if content_element is not None:
                    # Find the <ns1:dict> element within the <content> element
                    dict_element = content_element.find('./ns1:dict', namespaces)

                    # Find the <ns1:key name="version"> element within the <ns1:dict> element
                    version_element = dict_element.find('./ns1:key[@name="version"]', namespaces)

                    # Extract app version if the version element is found
                    if version_element is not None:
                        app_version = version_element.text.strip()

                installed_apps.append({'app_name': app_name, 'app_version': app_version})

        return installed_apps

    def generate_reports(self):
        reports = []
        for host in self.splunk_hosts:
            installed_apps = self.retrieve_installed_apps(host)
            reports.append({'host': host, 'installed_apps': installed_apps})
        return reports

    def generate_csv_report(self, filename='installed_apps_report.csv'):
        # Define CSV fieldnames
        fieldnames = ['Host', 'App Name', 'Version']

        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Write header
            writer.writeheader()

            # Write rows
            for report in self.reports:
                host = report['host']
                installed_apps = report['installed_apps']
                for app in installed_apps:
                    writer.writerow({'Host': host, 'App Name': app['app_name'], 'Version': app['app_version'] if app['app_version'] is not None else 'None'})

def main():
    SPLUNK_HOSTS_FILE = 'splunk_hosts.txt'
    SPLUNK_PORT = '8089'  # Usually 8089 for the management port

    # Initialize the report generator
    report_generator = InstalledAppsReport(SPLUNK_HOSTS_FILE, SPLUNK_PORT)
    
    # Generate the CSV report
    report_generator.generate_csv_report()

if __name__ == "__main__":
    main()

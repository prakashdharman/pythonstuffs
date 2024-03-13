#!/usr/bin/env python3.11
import requests
from bs4 import BeautifulSoup
import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
import xml.etree.ElementTree as ET

# Splunk credentials and API endpoint
SPLUNK_USERNAME = 'admin'
SPLUNK_PASSWORD = ''
SPLUNK_HOST = 'prakashs-macbook-pro.local'
SPLUNK_PORT = '8091'  # Usually 8089 for the management port

# Static Splunk Enterprise version to check compatibility against
SPLUNK_ENTERPRISE_VERSION = '9.2.1'

def get_installed_apps():
    url = f'https://{SPLUNK_HOST}:{SPLUNK_PORT}/services/apps/local'
    response = requests.get(url, auth=(SPLUNK_USERNAME, SPLUNK_PASSWORD), verify=False)
    #print(response.content)
    response.raise_for_status()  # Raise an exception for HTTP errors
    root = ET.fromstring(response.text)
    #print(response.text)
    print(root.findall('./{http://www.w3.org/2005/Atom}entry'))
    print("************")
    apps = root.findall('.//{http://www.w3.org/2005/Atom}entry')
    
    print (apps)
    print("************")

    installed_apps = {}
    for entry in apps:
        app_name_element = entry.find('.//{http://www.w3.org/2005/Atom}name')
        print(ET.tostring(entry, encoding='unicode', method='xml'))
        print(app_name_element.text.strip())
        #app_name = app.find('.//name').text
        #app_version = app.find('.//version').text
        #installed_apps[app_name] = app_version
    print(installed_apps)
    return installed_apps

def check_compatibility(installed_apps):
    compatibility_report = {}
    for app_name, app_version in installed_apps.items():
        splunkbase_app_version = get_splunkbase_app_version(app_name)
        if splunkbase_app_version:
            if app_version == splunkbase_app_version:
                compatibility_report[app_name] = "Compatible"
            else:
                compatibility_report[app_name] = "Not Compatible"
        else:
            compatibility_report[app_name] = "Version Information Not Available"
    return compatibility_report

def get_splunkbase_app_version(app_name):
    url = f'https://splunkbase.splunk.com/app/{app_name}/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        version_info = soup.find('div', class_='versionInfo')
        if version_info:
            return version_info.text.strip()
    return None

def main():
    installed_apps = get_installed_apps()
    if installed_apps:
        compatibility_report = check_compatibility(installed_apps)
        print("Installed Apps Compatibility Report:")
        print("-----------------------------------")
        for app_name, compatibility in compatibility_report.items():
            print(f"{app_name} (Version: {installed_apps[app_name]}) - {compatibility} with Splunk Enterprise {SPLUNK_ENTERPRISE_VERSION}")

if __name__ == "__main__":
    main()

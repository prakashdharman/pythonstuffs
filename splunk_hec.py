import logging
from logging import Handler
import requests

class SplunkHECHandler(Handler):
    def __init__(self, url, token):
        super().__init__()
        self.url = url
        self.token = token

    def emit(self, record):
        log_entry = self.format(record)
        event_data = {"event": log_entry}
        headers = {
            "Authorization": f"Splunk {self.token}",
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(self.url, headers=headers, json=event_data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            # Log a warning message if there's an error sending the log to Splunk
            logging.warning(f"Error sending log to Splunk HEC: {e}")



how to use ?

# main.py

# Import the SplunkHECHandler class from splunk_hec.py
from splunk_hec import SplunkHECHandler

def main():
    # Configure the Splunk HEC URL and token
    splunk_hec_url = "http://localhost:8089/services/collector/event"
    splunk_hec_token = "YOUR_TOKEN_HERE"

    # Create a SplunkHECHandler instance
    splunk_handler = SplunkHECHandler(splunk_hec_url, splunk_hec_token)

    # Configure the logger
    logger = logging.getLogger("splunk_logger")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(splunk_handler)

    # Test the logger
    logger.debug("Log message sent to Splunk HEC")

if __name__ == "__main__":
    main()


For more options


import logging
import requests

class SplunkHECHandler(logging.Handler):
    def __init__(self, url, token, sourcetype=None, index=None):
        super().__init__()
        self.url = url
        self.token = token
        self.sourcetype = sourcetype
        self.index = index

    def emit(self, record):
        log_entry = self.format(record)
        event_data = {"event": log_entry}
        if self.sourcetype:
            event_data["sourcetype"] = self.sourcetype
        if self.index:
            event_data["index"] = self.index
        headers = {
            "Authorization": f"Splunk {self.token}",
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(self.url, headers=headers, json=event_data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            # Log a warning message if there's an error sending the log to Splunk
            logging.warning(f"Error sending log to Splunk HEC: {e}")

# Example usage:
if __name__ == "__main__":
    # Configure the Splunk HEC URL, token, sourcetype, and index
    splunk_hec_url = "http://localhost:8089/services/collector/event"
    splunk_hec_token = "YOUR_TOKEN_HERE"
    splunk_hec_sourcetype = "your_sourcetype"
    splunk_hec_index = "your_index"

    # Create a SplunkHECHandler instance with sourcetype and index
    splunk_handler = SplunkHECHandler(splunk_hec_url, splunk_hec_token, splunk_hec_sourcetype, splunk_hec_index)

    # Configure the logger
    logger = logging.getLogger("splunk_logger")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(splunk_handler)

    # Test the logger
    logger.debug("Log message sent to Splunk HEC")

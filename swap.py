import xml.etree.ElementTree as ET

xml_data = """
<feed xmlns:ns0="http://www.w3.org/2005/Atom">
  ... (list of app entries) ...
</feed>
"""

root = ET.fromstring(xml_data)

# Assuming entries are under the "entry" element within the root
for entry in root.findall(".//{http://www.w3.org/2005/Atom}entry"):
  app_title = entry.findtext(".//{http://www.w3.org/2005/Atom}title")
  app_version = entry.findtext(".//{http://dev.splunk.com/ns/rest}dict/ns1:key[@name='version']/text()")
  
  # Print information for each app
  print(f"App Title: {app_title}")
  print(f"App Version: {app_version}")
  print("-" * 20)  # Optional separator between apps


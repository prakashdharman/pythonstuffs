import xml.etree.ElementTree as ET

def modify_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Modify genre attribute for all book elements
    for book in root.findall('book'):
        current_genre = book.get('genre', '')  # Get the current genre attribute value
        if current_genre:
            new_genre = f"{current_genre} (Updated)"
            book.set('genre', new_genre)  # Modify the genre attribute

    # Write the changes back to the XML file
    tree.write(xml_file)

if __name__ == "__main__":
    xml_file_path = 'example.xml'
    modify_xml(xml_file_path)

''' example.xml
<bookstore>
    <book genre="Science Fiction">
        <title>Introduction to Python</title>
        <author>John Doe</author>
        <price>29.99</price>
    </book>
    <book genre="Data Science">
        <title>Data Science with Python</title>
        <author>Jane Smith</author>
        <price>39.99</price>
    </book>
</bookstore>
'''

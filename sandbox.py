import xml.etree.ElementTree as ET

xml_string = """
<catalog>
  <item id="A1" type="software">
    <name>Translation Editor</name>
    <version>3.2</version>
  </item>
  <item id="A2" type="hardware">
    <name>CAT Tool Dongle</name>
    <version></version>
  </item>
  <item id="A3" type="software">
    <name>QA Checker</name>
    <version>1.0</version>
  </item>
</catalog>
"""

# 1. Parse the string

root = ET.fromstring(xml_string)
print(root)

# 2. Find all <item> elements
# 3. For each item print: id attribute, type attribute, name text, version text

for item in root.findall('item'):
    print(item.attrib['id'])
    print(item.attrib['type'])
    nameElement, versionElement = item.find('name'), item.find('version')
    version = versionElement.text if versionElement is not None and versionElement.text else None
    print(nameElement.text, version)
    

# 4. Handle empty version gracefully

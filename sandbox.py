import xml.etree.ElementTree as ET

test = ET.fromstring('<seg><bpt>tag</bpt>Insert image <ept>tag</ept> of a file driver</seg>')
print(list(test.itertext()))
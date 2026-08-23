import xml.etree.ElementTree as ET

xml_string = """
<library>
  <book id="1">
    <title>Deep Learning</title>
    <year>2016</year>
  </book>
  <book id="2">
    <title>Python for Data Analysis</title>
    <year>2022</year>
  </book>
  <book id="3">
    <title>Attention Is All You Need</title>
    <year></year>
  </book>
</library>
"""

# Parse the string (not a file this time — use ET.fromstring())

root = ET.fromstring(xml_string)

# Find all <book> elements

allBooks = root.findall('book')

# For each book: print its id attribute, title text, and year text

for book in allBooks:
    book_id = book.attrib
    title_text = book.find("title")
    year = book.find("year")
    print(book_id["id"], title_text.text, year.text)

# Handle the empty year gracefully — don't crash

import xml.etree.ElementTree as ET
import pandas as pd

xml_string = """
<translations>
  <unit id="U1" status="final">
    <source>Click to continue</source>
    <target lang="fr">Cliquez pour continuer</target>
  </unit>
  <unit id="U2" status="draft">
    <source>Cancel</source>
    <target lang="fr"></target>
  </unit>
  <unit id="U3" status="final">
    <source>Save and exit</source>
    <target lang="fr">Enregistrer et quitter</target>
  </unit>
</translations>
"""

root = ET.fromstring(xml_string)

# Using same root — build list of dicts, then DataFrame

entries = []

for unit in root.findall('unit'):
    entries.append({
        
    })

# Keys: id, status, source, target, lang, source_word_count

df = pd.DataFrame()

# Handle missing target as None
# Then:
# - filter to final status only
# - filter to units where target is not null
# - add a 'translated' column: 1 if target exists, 0 if not


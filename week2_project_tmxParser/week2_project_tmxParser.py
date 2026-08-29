# starting on 08/26/26 as part of the week2 flow

# before runnin ensure you cd to
# C:\Users\mateu\pytorch-nlp-journey\week2_project_tmxParser

import xml.etree.ElementTree as ET
import pandas as pd

XML_LANG = '{http://www.w3.org/XML/1998/namespace}lang'

def tmx_parser(file_path):
    segments_from_tmx = []
    xml_tree = ET.parse(file_path)
    root = xml_tree.getroot()
    for tu in root.findall('body/tu'):
        source = None
        target = None
        target_lang = None
        for tuv in tu.findall('tuv'):
            lang = tuv.attrib[XML_LANG]
            seg = tuv.find('seg')
            text = seg.text if seg is not None and seg.text else None

            if lang == 'en-US':
                source = seg.text
            else:
                target_lang = lang
                target = seg.text if seg is not None and seg.text else None

        # append the dict here - outside the inner loop
        segments_from_tmx.append({
            'source': source,
            'target': target,
            'target_lang': target_lang,
            'source_len': len(source.split()),
            'target_len': len(target.split()) if target else None
            })
    return segments_from_tmx

file_path = r'C:\Users\mateu\pytorch-nlp-journey\week2_project_tmxParser\sample_tm.tmx'

results = tmx_parser(file_path)

df = pd.DataFrame(results)
#print(df.head())
#print(df.isnull().sum())

# counting coverage
total_segments = df.groupby('target_lang')['source'].count()
translated_segments = df.groupby('target_lang')['target'].count()
coverage = translated_segments / total_segments * 100
print(coverage)

summary = pd.DataFrame({
    'total': total_segments,
    'translated': translated_segments,
    'coverage_pct': coverage
    })

print(summary)
'''
print(f'Total segments parsed: {len(results)}')
for r in results[:3]:
    print(r)
'''
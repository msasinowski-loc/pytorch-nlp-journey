# starting on 08/26/26 as part of the week2 flow
# v2 started on 09/05 - moves from mock TMX to actual examples
# v2.1 is identifying language codes instead of hardcoding
# v2.2 is improving the TUs parser to account for nested tags 

# before runnin ensure you cd to
# C:\Users\mateu\pytorch-nlp-journey\week2_project_tmxParser

import xml.etree.ElementTree as ET
import pandas as pd

XML_LANG = '{http://www.w3.org/XML/1998/namespace}lang'

# detect language code used in the tmx
# on reflection, deemed as redundant, code left in case of future use
'''
def language_code_detector(file_path):
    xml_tree = ET.parse(file_path)
    root = xml_tree.getroot()

    lang_code = set()
    header = root.find('header')
    source_language = header.attrib['srclang']

    for tuv in root.findall('body/tu/tuv'):
        lang_code.add(tuv.attrib[XML_LANG])
    return source_language, lang_code

'''

def tmx_parser(file_path):
    segments_from_tmx = []
    xml_tree = ET.parse(file_path)
    root = xml_tree.getroot()

    header = root.find('header')
    source_language = header.attrib['srclang']

    for tu in root.findall('body/tu'):
        source = None
        target = None
        target_lang = None
        for tuv in tu.findall('tuv'):
            lang = tuv.attrib[XML_LANG]
            seg = tuv.find('seg')
            text = seg.text if seg is not None and seg.text else None

            if lang == source_language:
                source = seg.text
            else:
                target_lang = lang
                target = seg.text if seg is not None and seg.text else None

        # append the dict here - outside the inner loop
        segments_from_tmx.append({
            'source': source,
            'target': target,
            'target_lang': target_lang,
            'source_len': len(source.split()) if source else None,
            'target_len': len(target.split()) if target else None
            })
    return segments_from_tmx

# counting coverage
def counting_coverage(df_from_results):
    total_segments = df_from_results.groupby('target_lang')['source'].count()
    translated_segments = df_from_results.groupby('target_lang')['target'].count()
    coverage = translated_segments / total_segments * 100

    summary = pd.DataFrame({
    'total': total_segments,
    'translated': translated_segments,
    'coverage_pct': coverage
    })

    print(summary)
    print(coverage)


file_path = r'C:\@my stuff\@study\Programming\pytorch-nlp-journey\tmxes_samples\full_size\LIUNA-Other-eng-spa-US-Master.tmx'
results = tmx_parser(file_path)

'''
print(f'Total segments parsed: {len(results)}')
for r in results[:3]:
    print(r)
'''


df = pd.DataFrame(results)

#print(df.head())
#print(df.isnull().sum())

#print(counting_coverage(df))

# df[df['source'].isnull()].to_csv('empty_tus.csv', index=False) # not used rn
# print(df[df['source'].isnull()])  # ditto

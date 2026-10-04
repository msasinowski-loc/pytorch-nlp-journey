# starting on 08/26/26 as part of the week2 flow

# v2 started on 09/05 - moves from mock TMX to actual examples
# v2.1 is identifying language codes instead of hardcoding
# v2.2 is improving the TUs parser to account for nested tags 

# 09/12
# decided to separate the cleaner into a stand-alone tool, closing this script
# as a pure parser

# before runnin ensure you cd to
# C:\Users\mateu\pytorch-nlp-journey\week2_project_tmxParser

import xml.etree.ElementTree as ET
import pandas as pd
import regex as re

XML_LANG = '{http://www.w3.org/XML/1998/namespace}lang'

file_path = r'C:\@my stuff\@study\Programming\pytorch-nlp-journey\tmxes_samples\full_size\LIUNA-Other-eng-spa-US-Master.tmx'
#file_path = r'C:\Users\mateu\pytorch-nlp-journey\week2_project_tmxParser_tmCleaner\tmxes_samples\full_size\LIUNA-Other-eng-spa-US-Master.tmx'

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

        source_clean = None # guardrails against no source tuv in TU, as it's appended below
        target_clean = None  # ditto
        
        for tuv in tu.findall('tuv'):
            lang = tuv.attrib[XML_LANG]
            seg = tuv.find('seg')

            if seg is not None:
                if lang == source_language:
                    source_full = ' '.join(seg.itertext())
                    source_clean = re.sub(r'&lt;.*?&gt;', '', source_full) # this strips escaped <>, technically
                    # not essential anymore as moved to a tmx cleaner, but doesn't hurt
                else:
                    target_lang = lang
                    target_full = ' '.join(seg.itertext())
                    target_clean = re.sub(r'&lt;.*?&gt;', '', target_full)

        # append the dict here - outside the inner loop
        segments_from_tmx.append({
            'source': source_clean,
            'target': target_clean,
            'target_lang': target_lang,
            'source_len': len(source_clean.split()) if source_clean else None,
            'target_len': len(target_clean.split()) if target_clean else None
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

df.to_csv('parsed_tmx_raw.csv', index=False) # not used rn
# print(df[df['source'].isnull()])  # ditto

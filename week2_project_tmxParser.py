# starting on 08/26/26 as part of the week2 flow

import xml.etree.ElementTree as ET

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
                # tbd
            else:
                # tbd

            # append the dict here - outside the inner loop
            segments_from_tmx({
                # tbd
            })
            # print(lang, seg.text)
    return segments_from_tmx


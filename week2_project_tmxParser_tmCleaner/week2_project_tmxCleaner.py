# starting on 09/12/26 as an addition to the week2 flow, which grew now /
# into a stand-alone database cleaner 

# a bit of break until 09/19, managed to create the whole logic, started working on the actual cleaning functions 

'''
the interface is
tmx_parser.py  →  raw_output.csv
tm_cleaner.py  →  reads raw_output.csv  →  clean.csv + flagged.csv
'''

import pandas as pd
import re 

# path on the rig
file_path = r'C:\@my stuff\@study\Programming\pytorch-nlp-journey\tmxes_processed\parsed_tmx_raw.csv'

# path on the laptop
# file_path = r'C:\Users\mateu\pytorch-nlp-journey\tmx_processed\parsed_tmx_raw.csv'

# establish possible tagging noise 

patterns_keys = {
    r'<[a-zA-Z]': 'unescaped_tags',  # <cap>, <strike>, but only the < + first letter, enough for detection
    r'\{[^}]*\}': 'curly_placeholders', # {lorem ipsum}
    r'‹#›': 'placeholder_hash',
    r'&lt;': 'escaped_tags', # html/xml escape sequence for <, think &lt;cap val="none"&gt; which \
    # browser or xml parser would render as <cap val="none">
    r'.*?&gt;': 'escaped_tags_closing', # html/xml escape sequence for >
}


def strip_unescaped_tags(df):
    pattern = r'<[^>]+>' # matches < then any characters that are not > and closes with > for a full structure
    df['source'] = df['source'].str.replace(pattern, '', regex=True)
    df['target'] = df['target'].str.replace(pattern, '', regex=True)
    return df


def strip_escaped_tags():
    pass

def escaped_tags_closing():
    pass

def strip_capitalization_tag():
    pass

# establish functions out of the patterns
CLEANING_FUNCTIONS = {
    'escaped_tags': strip_escaped_tags,
    'unsureWhatsthis': escaped_tags_closing,
    'capitalization_tag': strip_capitalization_tag
}

# detect the actual issues in the tmx

def detect_inline_tags(file):
    detected_problems = []

    df = pd.read_csv(file)

    for pattern, key in patterns_keys.items():
        if df['source'].str.contains(pattern, na=False).any():
            detected_problems.append(key)

    print (f'These are the problems detected in the CSV file:')
    print('\n'.join(detected_problems))
    return detected_problems

def tmx_cleaner(file, detected_problems):
    cleaned_df = pd.read_csv(file)
    for problem in detected_problems:
        if problem in CLEANING_FUNCTIONS:
            cleaned_df = CLEANING_FUNCTIONS[problem](cleaned_df)
           

    return cleaned_df


detect_inline_tags(file_path)
# starting on 09/12/26 as an addition to the week2 flow, which grew now /
# into a stand-alone database cleaner 

# a bit of break until 09/19, managed to create the whole logic, started working on the actual cleaning functions 

# picking up on 10/10 to add tag clean-up
# and it's done - the other four cleaning functions remain as placeholder, ready to add to the master logic when needed

# NEXT: remove trailing and extra spaces in tmx_cleaner function


'''
the interface is
tmx_parser.py  →  raw_output.csv
tm_cleaner.py  →  reads raw_output.csv  →  clean.csv + flagged.csv
'''

import pandas as pd
import re 

# path on the rig
# file_path = r'C:\@my stuff\@study\Programming\pytorch-nlp-journey\tmxes_processed\parsed_tmx_raw.csv'

# path on the laptop
file_path = r'C:\Users\mateu\pytorch-nlp-journey\tmx_processed\parsed_tmx_raw.csv'

# establish possible tagging noise 

patterns_keys = {
    r'<[a-zA-Z]': 'tags_unescaped',  # <cap>, <strike>, but only the < + first letter, enough for detection
    r'\{[^}]*\}': 'curly_placeholders', # {lorem ipsum}
    r'‹#›': 'placeholder_hash',
    r'&lt;': 'tags_escaped', # html/xml escape sequence for <, think &lt;cap val="none"&gt; which \
    # browser or xml parser would render as <cap val="none">
    r'.*?&gt;': 'tags_escaped_closing', # html/xml escape sequence for >
}

# actual cleaning functions here, activated when needed only

def strip_unescaped_tags(df):
    pattern = r'<[^>]+>' # matches < then any characters that are not > and closes with > for a full structure
    df['source'] = df['source'].str.replace(pattern, '', regex=True)
    df['target'] = df['target'].str.replace(pattern, '', regex=True)
    return df


def strip_escaped_tags(df):
    return df

def strip_escaped_tags_closing(df):
    return df

def strip_curly_placeholders(df):
    return df

def strip_placeholder_hash(df):
    return df

# establish functions out of the patterns
CLEANING_FUNCTIONS = {
    'tags_escaped': strip_escaped_tags,
    'tags_unescaped': strip_unescaped_tags,
    'tags_escaped_closing': strip_escaped_tags_closing,
    'curly_placeholders': strip_curly_placeholders,
    'placeholder_hash': strip_placeholder_hash

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


# the core function, triggers cleaning function based on the list detected

def tmx_cleaner(file, detected_problems):
    cleaned_df = pd.read_csv(file)
    for problem in detected_problems:
        if problem in CLEANING_FUNCTIONS:
            cleaned_df = CLEANING_FUNCTIONS[problem](cleaned_df)

    # stripping function created leading and trailing spaces + multiple spaces, removing them here:


    cleaned_df.to_csv('parsed_tmx_raw_CleanedUp.csv', index=False)
    return cleaned_df



detected_problems = detect_inline_tags(file_path)
tmx_cleaner(file_path, detected_problems)
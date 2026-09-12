# starting on 09/12/26 as an addition to the week2 flow, which grew now /
# into a stand-alone database cleaner 

'''
the interface is
tmx_parser.py  →  raw_output.csv
tm_cleaner.py  →  reads raw_output.csv  →  clean.csv + flagged.csv
'''

import pandas as pd
import re 


file_path = r'C:\@my stuff\@study\Programming\pytorch-nlp-journey\tmxes_processed\parsed_tmx_raw.csv'

patterns = [
    r'&lt;',
    r'.*?&gt;'
    r'<cap>'
]

CLEANING_FUNCTIONS = {
    'xyz': xyz_fix
}

def detect_inline_tags(file):
    detected_problems = []

    df = pd.read_csv(file)

    for pattern in patterns:
        if df['source'].str.contains(pattern, na=False).any():
            detected_problems.append(pattern)

    print (f'These are the problems detected in the CSV file:')
    print('\n'.join(detected_problems))
    return detected_problems

def tmx_cleaner(file, detected_problems):
    cleaned_df = pd.read_csv(file)
    for problem in detected_problems:
        if problem in CLEANING_FUNCTIONS:
            cleaned_df = CLEANING_FUNCTIONS[problem](cleaned_df)
           

    return cleaned_df


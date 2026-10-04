'''
The core idea is simple: for a good translation, 
the target should be roughly proportional in length to the source. 
EN→ES typically runs 15-25% longer. 
Segments where the ratio is wildly off are worth flagging.

Three stages:

Compute the ratio — target_len / source_len per row. What's the right Pandas operation for this?
Establish what "normal" looks like — compute mean and standard deviation of the ratio. A segment is an outlier if it's more than N standard deviations from the mean. This is called a z-score.
Flag and report — add an outlier column, separate clean from flagged, export both CSVs + print a summary.

10/04 development stops at v1 - the initial results shows that the z-score alone is too blunt.
The high-ratio cases detected in the pilot were fine, because:
Spanish expands English abbreviations (OSHA, EPA, CFR) into full phrases
Short segments amplify the ratio

A more useful signal would combine z-score with a segment type check — that's exactly the "segment classifier" idea I put in the weekend projects backlog. 
An abbreviation-heavy short segment with high ratio is probably fine; a full sentence with high ratio is more suspicious.
More to come maybe
'''

import numpy as np
import pandas as pd


file_path = r'C:\@my stuff\@study\Programming\pytorch-nlp-journey\tmxes_processed\parsed_tmx_raw.csv'

def compute_ratio(file_path):
    df = pd.read_csv(file_path)
    # pd.set_option('display.max_columns',  None) # this is useful for showing all columns
    # print(df.head())

    
    df = df[df['source_len'] > 3]  # this is filtering the noise out, too short segments are too sensitive for length change and would make the mean/median less accurate
    df['ratio'] = df['target_len'] / df['source_len']
    # print(df['ratio'].describe()) # this showsthe distance between mean and median (50th percentile), used to help with decision on which to choose
    
    average_ratio = df['ratio'].median()
    return(average_ratio)
        

def find_outliers(file_path, average_ratio):
    df = pd.read_csv(file_path)
    df = df[df['source_len'] > 3] 

    df['ratio'] = df['target_len'] / df['source_len']
    median = df['ratio'].median()
    std = df['ratio'].std()
    df['z'] = (df['ratio'] - median) / std
      
    df['outlier'] = abs(df['z']) > 2

    
    df_clean = df[~df['outlier']]
    df_flagged = df[df['outlier']]
    
    print(f'Total segments: {len(df)}')
    print(f'Clean: {len(df_clean)}')
    print(f"Flagged: {len(df_flagged)} ({len(df_flagged)/len(df)*100:.1f}%)")
    print(f"Ratio range for flagged: {df_flagged['ratio'].min():.2f} – {df_flagged['ratio'].max():.2f}")

    
    df_clean.to_csv('lqa_clean.csv', index=False)
    df_flagged.to_csv('lqa_flagged.csv', index=False)


average = compute_ratio(file_path)
find_outliers(file_path, average)






'''
The core idea is simple: for a good translation, 
the target should be roughly proportional in length to the source. 
EN→ES typically runs 15-25% longer. 
Segments where the ratio is wildly off are worth flagging.
'''
'''
Three stages:

Compute the ratio — target_len / source_len per row. What's the right Pandas operation for this?
Establish what "normal" looks like — compute mean and standard deviation of the ratio. A segment is an outlier if it's more than N standard deviations from the mean. This is called a z-score.
Flag and report — add an outlier column, separate clean from flagged, export both CSVs + print a summary.

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
    z = (ratio - average_ratio) / std

    
    df['outlier'] = 


compute_ratio(file_path)

    



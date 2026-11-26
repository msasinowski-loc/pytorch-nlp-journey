"""
Similarity Finder \ near_duplicate_detector
==========================
pytorch-nlp-journey · weekend build · msasinowski-loc

PURPOSE
-------
Find pairs of source segments inside one TM that are near-duplicates of each
other (internal fuzzy matches), score them with cosine similarity on word-count
vectors, and report them in CAT-style match bands.

DATA
----
Input:      parsed_tmx_raw_CleanedUp.csv  (regex-cleaned parser output)
Reference:  parsed_tmx_raw.csv            (untouched; kept for data preservation)
Columns:    source, target, target_lang, source_len, target_len
Corpus:     LIUNA project, EN -> ES-US, 8,552 segments
Prototype:  500-segment random sample (fixed random_state) before scaling up

PIPELINE (milestones)
---------------------
M1  Load & sample      -> clean list of source segments
M2  Vocabulary         -> dict: word -> column index
M3  Count matrix       -> A, shape (N, V): one row per segment, one column per word
M4  Similarity matrix  -> S = A @ A.T, shape (N, N), normalised to cosine similarity
M5  Pair extraction    -> upper triangle only (no self-pairs, no duplicate pairs),
                          filtered by threshold
M6  Report             -> DataFrame (seg_i, seg_j, score), sorted, exported to CSV,
                          with counts per match band

11/14 update, upon M2 progress:
load → remove empty → dedupe raw text (count repetitions) → sample 500
     → tokenise → filter [] (count) → vocabulary → M3

CAT TOOL COMPARISON (memoQ homogeneity / internal fuzzy matching)
-----------------------------------------------------------------
Shared:
  - Compares segments within the same document, not against an external TM
  - Produces a similarity score per pair, grouped into match bands
  - Separates exact repetitions from fuzzy matches  [TODO: confirm in M6]
Differs:
  - memoQ processes segments in document order (results depend on order);
    this tool scores every pair at once, so order does not matter
  - memoQ's scoring is proprietary; this tool uses transparent cosine
    similarity on word counts
  - Bag-of-words ignores word order: "Call your doctor" vs "Your doctor call"
    scores 1.0 here; a CAT tool would penalise the reordering

KEY MATH
--------
cos(a, b) = (a . b) / (||a|| * ||b||)
  - 1.0 = same direction (same word profile), 0.0 = no shared words
  - Word counts are non-negative, so scores here fall in [0, 1]
S = A @ A.T gives every pairwise dot product at once:
  - S[i, j] = dot(segment_i, segment_j)
  - S[i, i] = ||segment_i||^2 (squared length on the diagonal)
Normalisation divides S by the outer product of the row norms,
via broadcasting: (N, 1) against (1, N)

DESIGN DECISIONS
----------------
DESIGN DECISIONS
----------------
- Cleaned dataset over raw: tag codes would otherwise become "words"
- 500-segment prototype: the full N x N matrix for 8,552 segments is ~73M
  cells  [TODO: record the memory cost you calculated]
- source_len is stale: the 42 empty sources still show source_len = 3, so it was
  computed before the regex cleanup  [TODO: recompute on cleaned text, or don't use]

Decided 2026-11-14 (M2):
- Case: all lowercase. Only risk is an all-caps acronym that spells out as a word,
  e.g. SHIP (State Health Insurance Assistance Program) vs "ship". Not relevant
  for the pilot, so decided against the distraction.
- Punctuation: strip it. Low risk, not worth complicating the code until proven
  otherwise. Side effect: stripping punctuation also removes { and }.
- {} placeholders: [TABLED] want to see specific examples to assess the risk.
  Build the core code first, then isolate these cases.
- Placeholder-only segments (e.g. ‹#›): filter out of scoring. After stripping
  they become empty -> zero vector -> norm 0 -> NaN in the cosine (M1 lesson).
  [TODO: count and report them, as CAT lists them with 0 billable
- dedupe on raw text, before sampling, to get a clean source data
- [TODO] for n-grams/compounds as a future enhancement.

Decided 2026-11-21 (M3):
- M2 established the token pool. Re-doing it in M3 would offer clarity of logical connection,
but means re-doing the operation, computation and cost. Decided to re-use M2's pool.
- [TODO] in 


KA ITEMS EXERCISED
------------------
FundMath-LinAlg-004 (cosine similarity), LinAlg-003 (matmul, A @ A.T),
LinAlg-005 (dot product), LinAlg-007 (L2 norm), Ph1-Python-005 (broadcasting),
Ph1-Python-006 (indexing), Ph1-Python-008 (DataFrame)

VERSION LOG
-----------
v0.1  2026-10-24  Project scoped. Milestones M1-M6 defined. CleanedUp dataset
                  chosen; raw kept as reference. CAT comparison documented.
                  Open decisions listed as TODOs.
v0.2  2026-11-08  M1 completed, creating a sampled clean list of source segments
                  42 empty rows removed (42 NaN, 0 whitespace), 8,510 rows left, 500 sampled with random_state=42. 
                  one learning: read_csv turns empty fields into NaN.
v0.3  2026-11-14  M2 started; decisions made; tokenise() written and tested on 4 segments; 
                  the empty-list result found to identify placeholder-only segments.
v0.4  2026-11-15  M2 closed: deduped the raw entries, found 2,243 reps. established dictionary of tokens
                  with 1,863 entries on the fixed 500-segments sample, 0 empty segments in it
v0.5  2026-11-21  M3 started: the A array created with zeros, set for vectorizing sentences. (N,V) shape
                  where N is the number of rows, V is one column per token
                  

                  

next planned (last update: 11/15): 
M3 starts
"""

import numpy as np
import pandas as pd
import regex as re

# FILE PATH ESTABLISHING
# clunky at the moment, to be fixed at a later stage

# rig
file_path = r'C:\@my stuff\@study\Programming\pytorch-nlp-journey\tmxes_processed\parsed_tmx_raw_CleanedUp.csv'

# laptop
# file_path = r'C:\Users\mateu\pytorch-nlp-journey\tmx_processed\parsed_tmx_raw_CleanedUp.csv'

dataset = pd.read_csv(file_path)

# basic sanity checks
# print(dataset.shape)
# print(dataset.head())

# verifying how many empty segments are there
# they need to be removed to reduce the computation costs - there is no value in calculating them. 
# Remove empty sources: their word-count vector is all zeros → L2 norm = 0 →
# the cosine denominator (||a|| * ||b||) becomes 0 in M4. NumPy doesn't crash on
# division by zero: it quietly returns NaN (with a warning), and that NaN spreads
# into every pair involving the segment. Fewer rows to compute is a bonus.

# it's a two-step approach, first for None or NaN
# followed by whitespaces only, which Panda doesn't see as None/NaN but an empty, yet present, string data
# it's defensive code - breaking into components instead of a blended result

is_nan_source = dataset['source'].isnull()
is_source_whitespace =  dataset['source'].str.strip() == '' # note the use of .str. as the accessor for Panda Series to string method bridge

is_empty_source_combined = (is_nan_source) | (is_source_whitespace)
empty_segments = dataset[is_empty_source_combined] 

# print(f'The count for NaN segments is: {is_nan_source.sum()}')
# print(f'The count for whitespaces segments is: {is_source_whitespace.sum()}')

# sanity checks - checking the total
# print(empty_segments.shape)
# print(empty_segments.head())

# removing the empty segments from the dataset
dataset_no_empty_segments = dataset[~is_empty_source_combined]

print(dataset_no_empty_segments.shape)

# deduping - removing duplicates from the dataset with no empty segments:
# WHY? to remove what CAT would count as repetitions, multiple instaces of identical segments would
# introduce noise to the similarity calculations, as same segment will identify multiple pairs of identity

is_duplicate_source = dataset_no_empty_segments.duplicated(subset='source')

count_of_duplicates = is_duplicate_source.sum()
print(f'The total count of found duplicated segments is {count_of_duplicates}')
# veryfing what was identified as duplicates
# print(f"The 5 most common duplicates are: {dataset_no_empty_segments['source'].value_counts().head(5)}")

# removing the duplicates

dataset_unique = dataset_no_empty_segments[~is_duplicate_source]

# random sampling on a fixed seed to allow consistency in results between sessions
sampled_dataset = dataset_unique.sample(n=500, random_state=42)
#print(sampled_dataset.head(5))

list_from_sampled_dataset = sampled_dataset['source'].tolist()


# building the tokenizer

def tokenizer(text):
    text_clean = re.sub(r'[^\w\s]', ' ', text) # removing punctuation
    tokens = text_clean.lower().split() 
    return tokens

''' testing the tokenizer
test_text = "{} Underground Utilities {}"
test_text2 = "Before using a pile driver…"
test_text3 = "but if there are electrical, gas, water lines, or other underground utilities, they MUST be avoided."
test_text4 ="‹#›"

print(tokenizer(test_text4))
'''

# BUILDING VOCAB POOL

vocab_pool = {}
empty_lists_entry = 0


# preparing for M3 - transitioning from full sentences ("check the hat") in list_from_sampled_dataset
# to an intermediary storage of ["check", "the", "hat"] - this will be used to loop through it and assign values to columns


list_of_tokenized_sentences = [] 

for entry in list_from_sampled_dataset:
    tokens_in_the_entry = tokenizer(entry)
    list_of_tokenized_sentences.append(tokens_in_the_entry)
    if tokens_in_the_entry == []:
        empty_lists_entry += 1
    for token in tokens_in_the_entry:
        if token not in vocab_pool:
            counter = len(vocab_pool)
            vocab_pool[token] = counter

print(f'Checking the number of unique words generated: {len(vocab_pool)}')
print(f'And checking the number of empty segments in the cleaned up dataset: {empty_lists_entry}')
print(f'The length of the list_of_tokenized_sentences is: {len(list_of_tokenized_sentences)}')


# and building the flipped dictionary to allow column-to-word check

reverse_vocab_pool_dictionary = {}
for word, column in vocab_pool.items():
    reverse_vocab_pool_dictionary[column] = word

# creating the zero matrix

A = np.zeros((len(list_from_sampled_dataset), len(vocab_pool)))
#print(A.shape)
#print(A.sum())

# filling in the A array with actual vectors

for i, sentence in enumerate(list_of_tokenized_sentences):
    row_number = i
    for token in sentence:
        A[row_number, vocab_pool[token]] += 1


# check on the loop result, it needs to match the token count from the itemized list

tokens_total = 0
for sentence in list_of_tokenized_sentences:
    tokens_total += len(sentence)

#print(tokens_total)
print(f'Check if the A loop yielded same token total as the length of the list: {tokens_total == A.sum()}')

# sanity checks:
print(A.max())

# if sanity checks gives an unexpected result (example: 27), then this is the way to identify the segment:

row_with_the_highest_token_count = A.max(axis=1)
row_id_for_the_highest_token_count = np.argmax(row_with_the_highest_token_count)

#print(list_from_sampled_dataset[row_id_for_the_highest_token_count])
print(reverse_vocab_pool_dictionary[np.argmax(A[row_id_for_the_highest_token_count])])
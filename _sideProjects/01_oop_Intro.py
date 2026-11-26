"""
Placeholder Checker
===================
pytorch-nlp-journey · OOP week build · msasinowski-loc

PURPOSE
-------
For each TM row, check whether the target keeps the source's placeholders
intact. Report the rows where they don't (missing, extra, or reordered).

CAT TOOL COMPARISON (memoQ QA / Xbench tag & placeholder checks)
----------------------------------------------------------------
Shared:
  - Compares placeholders/tags between source and target, row by row
  - Flags mismatches for a human to review
Differs:
  - CAT QA uses severity levels and can allow legitimate reordering;
    this tool is blunt: exact match or not
  - CAT tools know each file format's tags; this tool uses one regex

DATA
----
Input:   parsed_tmx_raw_CleanedUp.csv (source and target columns)
Corpus:  LIUNA project, EN -> ES-US

DESIGN DECISIONS
----------------
- OOP: one Segment object per TM row; source and target live together
  because every check needs both.
- extract_placeholders(text) takes the text as a parameter, so one method
  serves both sides (DRY) instead of two near-identical methods.
- Placeholder pattern: r'\\{\\d*\\}|‹#›' -> {}, {0}, {12}, ‹#›
- "Blunt" comparison: the two lists must match exactly, so order AND
  count both matter. Legitimate reordering in Spanish ({1} envió {0})
  will be flagged; flagged means "for a human", not "wrong".
- placeholders_match() returns True/False per row: a Bernoulli check,
  so its mean over the TM = the TM's placeholder error rate.
- [STRETCH] user-friendly export of mismatching rows, showing what differs.
- [IDEA] real-world triage: exact matches pass automatically; only count
  or order differences go to a human reviewer.

KA ITEMS EXERCISED
------------------
OOP (class, __init__, self, methods), regex (re.findall), Bernoulli (Prob-004)

VERSION LOG
-----------
v0.1  2026-11-26  Segment class: __init__(source, target),
                  extract_placeholders(text), placeholders_match().
                  Tested on one row: ['{}', '{}'] vs ['{}'] -> mismatch found.

next planned: Test step (edge cases), then run on the full TM.
"""

import re

class Segment:
    def __init__(self, source, target):
      self.source = source
      self.target = target

    def extract_placeholders(self, text):
        placeholders = re.findall(r'\{\d*\}|‹#›', text)
        return placeholders

    def placeholders_match(self):
       source_placeholders = self.extract_placeholders(self.source)
       target_placeholders = self.extract_placeholders(self.target)
       return source_placeholders == target_placeholders

seg = Segment("{} Task 2 {} :", "{} Tarea 2 :")
print(seg.source)
print(seg.target)
print(type(seg))
print(seg.extract_placeholders('{} Task 2 {} :'))
print(seg.extract_placeholders('{} Tarea 2 :'))
#!/usr/bin/env python
"""
Deduplicate tokens (that are not punctuation)
and preserves whitespace between them -- e.g. you don't lose your newlines.

(Assumes tokens are separated by whitespace.)
"""
import re,sys,string
from collections import defaultdict
PUNCT = set(string.punctuation)

def is_punct(s):
  return all(x in PUNCT for x in s)

text = sys.stdin.read()
token_ws_alternation = re.split(r'(\s+)', text)
#print token_ws_alternation

tokens = [t for t in token_ws_alternation if re.search(r'\S', t)]
counts = defaultdict(int)
for tok in tokens:
  if not is_punct(tok):
    counts[tok] += 1

needs_dedup = set([w for w in counts if counts[w] > 1])
counter = defaultdict(int)
output = []
for tok in token_ws_alternation:
  if tok in needs_dedup:
    counter[tok] += 1
    tok = "{}-{}".format(tok, counter[tok])
  output.append(tok)

print ''.join(output)

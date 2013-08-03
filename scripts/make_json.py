#!/usr/bin/env python
"""
Convert from annotations format to FUDG JSON, as specified in FUDG_JSON.md.
Outputs one sentence (or rather, annotations container) per line, with the
columns:

SentenceID TAB SpaceSepTokens TAB {ParseGraphAsJson}

E.g.:
  scripts/make_json.py anno/tweets/dev.0000.anno

... It may be desirable to use ID information contained in other parts of the
container, but I guess we'll use filenames for now...
"""
from __future__ import print_function

import sys,re,os
try:
  import ujson as json
except ImportError:
  import json

import view
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../gflparser'))
import parser as gfl_parser

args = sys.argv[1:]
for filename in args:
  tokens_codes_annos = view.process_potentially_multifile(filename)
  doc_id = re.sub(r'\.(anno|txt)$','', filename)

  for i,(tokens,code,anno) in enumerate(tokens_codes_annos):
    if not code: continue
    sentence_id = doc_id
    if len(tokens_codes_annos)>1: sentence_id += ':' + str(i)
    parse = gfl_parser.parse(tokens, code, check_semantics=True)
    parseJ = parse.to_json()
    print(sentence_id, ' '.join(tokens), json.dumps(parseJ), sep='\t')

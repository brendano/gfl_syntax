#!/usr/bin/env python
"""
convert from annotations format to JSON.  Outputs one sentence (or rather, annotations
container) per line, with the columns:

SentenceID TAB SpaceSepTokens TAB {ParseGraphAsJson}

E.g.:
  scripts/make_json.py anno/tweets/dev.0000.anno

... It may be desirable to use ID information contained in other parts of the
container, but I guess we'll use filenames for now...
"""
import sys,re,os
try:
  import ujson as json
except ImportError:
  import json
import view
import gfl_parser

args = sys.argv[1:]
for filename in args:
  tokens_codes_annos = view.process_potentially_multifile(filename)
  doc_id = re.sub(r'\.(anno|txt)$','', filename)

  for i,(tokens,code,anno) in enumerate(tokens_codes_annos):
    if not code: continue
    sentence_id = doc_id
    if len(tokens_codes_annos)>1: sentence_id += ':' + str(i)
    parse = gfl_parser.parse(tokens,code)
    parseJ = parse.to_json()
    ## hacky! if a token is on its own line in the annotation, it gets specially added to nodes
    for ln in code.splitlines():
      if ln in tokens and ln not in parseJ['nodes']:
        parseJ['nodes'].append('W('+ln+')')
        parseJ['node2words']['W('+ln+')'] = [ln]
    print "{id}\t{tokens}\t{parse}".format(id=sentence_id, tokens=' '.join(tokens), parse=json.dumps(parseJ))


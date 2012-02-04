#!/usr/bin/env python
from __future__ import division
import re,sys,os,traceback
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../parser'))
import gfl_parser

show_words = False

def parse_parts(tweet_text):
  s = tweet_text
  s = re.sub('^--- *', '', s)
  lines = s.split('\n')
  lines = [L.strip() for L in lines if L.strip()]

  parts = re.split(r'(\n|^)%', s)
  parts = [x.strip() for x in parts]
  parts = [x for x in parts if x]
  pairs = []
  for part in parts:
    lines = part.split('\n')
    if len(lines)==1:
      L = lines[0]
      if len(L.split())==2:
        pairs.append(L.split())
        continue
    key = lines[0].strip()
    value = '\n'.join(lines[1:]).strip()
    pairs.append((key,value))
  return dict(pairs)

def clean_name_for_dot(s):
  # s = s.replace('$','N_').replace('^','_')
  if not show_words:
    s = re.sub(r'^(MW|W)\((.*?)\)$', r'\2', s)
  s = s.encode('utf8')
  s = s.replace('"', "''")
  s = '"{}"'.format(s)
  return s

def psf2dot(parse):
  global show_words
  G = []
  fontsize = 12
  wfontsize = 11
  conjcol = '"#106010"'
  conjbg  = '"#90c090"'
  darkblue = '"#202090"'
  for head,child,label in parse.node_edges:
    head=clean_name_for_dot(head)
    child=clean_name_for_dot(child)
    col = {None:darkblue, 'Conj':conjcol, 'Anaph':'purple'}.get(label, 'blue')
    dir = {'Anaph':'none'}.get(label, 'back')
    weight = {'Anaph':0.2}.get(label, 2)
    lab = '' if not label else label
    e = '{head} -> {child} [color={col} fontsize={fontsize} fontcolor={col} dir={dir} weight={weight} label="{lab}"]'.format(**locals())
    G.append(e)
  
  ## Node information
  for node in parse.nodes:
    #label = re.sub(r'\(.*','', node)
    label = node
    bg = conjbg if node.startswith('$') else '"#d0d0f0"'
    G.append('{name} [color={bg} style=filled fillcolor={bg} height=0.4 fontcolor=black label={label} fontsize={fontsize}]'.format(
      name=clean_name_for_dot(node), label=clean_name_for_dot(label), fontsize=fontsize, bg=bg))

  if show_words:
    seen_words = set()
    for node,words in parse.node2words.items():
      node = clean_name_for_dot(node)
      # emit edges in surface order ... graphviz seems to respect this a little bit.
      words = sorted(words, key=lambda w: parse.word2id[w])
      for w in words:
        w = clean_name_for_dot(w)
        seen_words.add(w)
        e = '%s -> %s [color=gray weight=1 dir=none]' % (node, w)
        G.append(e)
    for node,wordlabels in parse.extra_node2words.items():
      node = clean_name_for_dot(node)
      for w,label in wordlabels:
        w = clean_name_for_dot(w)
        seen_words.add(w)
        lab = '' if not label else clean_name_for_dot(label)
        e = '{node} -> {w} [color={conjcol} fontcolor={conjcol} fontsize={fontsize} weight=2 dir=none label={lab}]'.format(**locals())
        G.append(e)
    for word in seen_words:
      col = '"#e0e0e0"'
      G.append("{word} [shape=box fillcolor={col} style=filled color={col} height=0.1 width=0.1 fontsize={wfontsize}]".format(**locals()))

  #for word,ind in parse.word2id.items():
  #  if word not in seen_words: continue
  #  G.append('''%s [pos="%s,0!"]''' % (clean_name_for_dot(word),(1.1 * ind)))
  #G.append('splines=true')
  s = '\n'.join(L+';' for L in G)
  return 'digraph {\n %s \n}' % s

def print_html(out, anno_text, png):
  img = '' if not png else "<img src={}>".format(os.path.basename(png))
  print>>out, """
  <hr>
  <pre>{anno_text}</pre>
  <p>{img}
  """.format(**locals())
  #print>>out, """
  #<table><tr><td style="padding-right:20px; vertical-align:top">
  #  <pre>{anno_text}</pre>
  #<td style="vertical-align:top"><img src={png}>
  #</table>
  #""".format(**locals())

def print_header(out):
  print>>out, """
  <style>
  pre {
    font-family: times, serif;
    white-space: pre-wrap;       /* css-3 */
    white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
    white-space: -pre-wrap;      /* Opera 4-6 */
    white-space: -o-pre-wrap;    /* Opera 7 */
    word-wrap: break-word;       /* Internet Explorer 5.5+ */
  }
  </style>
  <body>
  """

def make_html(basename, anno_text, png):
  html_filename = basename + '.html'
  with open(html_filename, 'w') as out:
    print_header(out)
    print_html(out, anno_text, png)
  return html_filename

def process_one_parse(p, base):
  # base is for OUTPUT
  dot = psf2dot(p)
  with open("{base}.dot".format(**locals()),'w') as f: print>>f, dot
  cmd = "dot -Tpng < {base}.dot > {base}.png".format(**locals())
  print cmd
  os.system(cmd)

def desktop_open(filename):
  # TODO how does this work on other platforms
  if 'darwin' in sys.platform:
    os.system("""open "{filename}" """.format(**locals()))
  else:
    print "File is ready to open:  " + filename
    
def process_potentially_multifile(filename):
  # parse container format and return GFL code .. do NOT parse it yet
  anno_text = open(filename).read().strip()
  if '%' not in anno_text:
    tokens = string.letters
    code = anno_text
    return [(tokens, code, anno_text)]
  multi_annos = re.split(r'(\n|^)--- *(\n|$)', anno_text)
  multi_annos = ['---\n' + x.strip() for x in multi_annos if x.strip()]
  if len(multi_annos) == 0:
    print "empty annotations"
    return None
  tuples = []
  for anno_text in multi_annos:
    container = parse_parts(anno_text)
    tokens = container.get('TEXT','').split()
    code = container.get('ANNO','').strip()
    tuples.append((tokens, code, anno_text))
  return tuples

if __name__=='__main__':
  import string
  from optparse import OptionParser
  p = OptionParser(usage="""
  %prog filename.anno  [or multiple files]
  Visualizes a GFL annotations file via GraphViz (as an image file).
  Also can handle a file with multiple annotations in it (outputs HTML)""")
  p.add_option('-w', dest="show_words", action='store_true', help="show words in graph")
  p.add_option('-n', dest="supress_open", action='store_true', help="force to not open image when done")
  p.add_option('-v', dest="verbose", action='store_true', help="verbose mode")
  p.add_option('-m', dest="open_html", action='store_true', help="force to open html, not png, version")
  opts,args = p.parse_args()
  show_words = opts.show_words
  batch_mode = len(args) > 1
  do_open = not batch_mode and not opts.supress_open
  VERBOSE = opts.verbose
  multi_mode = None
  multi_annos = None

  if not args:
    print "(use -h for help)"
    args = ['/dev/stdin']

  for filename in args:
    print "FILE",filename
    if filename=='/dev/stdin':
      bigbase = 'tmp'
    else:
      bigbase = re.sub(r'\.(txt|anno)$','', filename)

    tokens_codes_texts = process_potentially_multifile(filename)

    if len(tokens_codes_texts)==1:
      tokens,code,anno_text = tokens_codes_texts[0]
      try:
        parse = gfl_parser.parse(tokens, code)
      except Exception:
        if not batch_mode: raise
        traceback.print_exc()
        continue
      base = bigbase
      process_one_parse(parse, base)
      htmlfile = make_html(base, anno_text, base+'.png')
      if do_open:
        if opts.open_html:
          desktop_open(htmlfile)
        else:
          desktop_open("{base}.png".format(**locals()))
      sys.exit()

    parses = []
    for tokens,code,text in tokens_codes_texts:
      if not code or not tokens:
        parses.append(None)
      else:
        try:
          p = gfl_parser.parse(tokens, code)
          parses.append(p)
        except Exception:
          print code
          parses.append(None)
          if not batch_mode: raise
          traceback.print_exc()
          continue
    os.system("rm -f {bigbase}.*.png".format(**locals()))

    htmlfile = bigbase + '.html'
    out = open(htmlfile, 'w')
    print_header(out)
    x = []
    for i,parse in enumerate(parses):
      anno_text = tokens_codes_texts[i][2]
      base = "%s.%d" % (bigbase,i)
      print "\t",base
      if parse is not None:
        process_one_parse(parse, base)
      print_html(out, anno_text, base + '.png' if parse is not None else None)
    out.close()
    if do_open:
      desktop_open(htmlfile)


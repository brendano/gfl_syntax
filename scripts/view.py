#!/usr/bin/env python
from __future__ import division
import re,sys,os,traceback
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../parser'))
import gfl_parser

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
  s = s.encode('utf8')
  s = s.replace('"', "''")
  s = '"{}"'.format(s)
  return s

def psf2dot(parse, show_words=True):
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

  png = os.path.basename(png)
  print>>out, """
  <hr>
  <pre>{anno_text}</pre>
  <p><img src={png}>
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

def make_multi_html(bigbase, base_and_texts):
  html_filename = bigbase + '.html'
  with open(html_filename, 'w') as out:
    print_header(out)
    for base,anno_text in base_and_texts:
      print_html(out, anno_text, base + '.png')
  return html_filename

def process_one_parse(p, base, show_words):
  # base is for OUTPUT
  dot = psf2dot(p, show_words=show_words)
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
  opts,args = p.parse_args()
  batch_mode = len(args) > 1
  do_open = not batch_mode and not opts.supress_open
  VERBOSE = opts.verbose
  multi_mode = None
  multi_annos = None

  if not args:
    print "(use -h for options help)"
    args = ['/dev/stdin']

  for filename in args:
    print "FILE",filename
    if filename=='/dev/stdin':
      bigbase = 'tmp'
    else:
      bigbase = re.sub(r'\.(txt|anno)$','', filename)
    anno_text = open(filename).read()
    multi_annos,tokens,code = None,None,None
    if '%' not in anno_text:
      tokens = string.letters
      code = anno_text
      multi_mode = 'SINGLE'
    else:
      multi_annos = re.split(r'(\n|^)--- *(\n|$)', anno_text)
      multi_annos = ['---\n' + x.strip() for x in multi_annos if x.strip()]
      if len(multi_annos) == 0:
        print "empty annotations"
        continue
      elif len(multi_annos) == 1:
        container = parse_parts(anno_text)
        tokens = container['TEXT'].split()
        code = container['ANNO']
        multi_mode = 'SINGLE'
      else:
        multi_mode = 'MULTI'

    if multi_mode=='SINGLE':
      try:
        parses_annos = [(gfl_parser.parse(tokens, code), multi_annos[0])]
      except Exception:
        if not batch_mode: raise
        traceback.print_exc()
        continue
      base = bigbase
      process_one_parse(parses_annos[0][0], base, opts.show_words)
      make_html(base, anno_text, base+'.png')
      if do_open:
        desktop_open("{base}.png".format(**locals()))
    else:
      parses_annos = []
      for anno in multi_annos:
        x = parse_parts(anno)
        if not (x.get('TEXT','').strip() or x.get('ANNO','').strip()):
          parses_annos.append((None,anno))
          continue
        try:
          p = gfl_parser.parse(x['TEXT'].split(), x['ANNO'])
          parses_annos.append((p, anno))
        except Exception:
          print x['ANNO']
          if not batch_mode: raise
          traceback.print_exc()
          continue
      os.system("rm -f {bigbase}.*.png".format(**locals()))
      x = []
      for i,(parse,anno) in enumerate(parses_annos):
        base = "%s.%d" % (bigbase,i)
        print "\t",base
        if parse is not None:
          process_one_parse(parse, base, opts.show_words)
        x.append((base,anno))
      htmlfile = make_multi_html(bigbase, x)
      if do_open:
        desktop_open(htmlfile)


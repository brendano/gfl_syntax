#!/usr/bin/env python
# vim:sts=4:sw=4
from __future__ import division, absolute_import
import re,sys,os,traceback,itertools,json,codecs
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'gflparser'))
import gfl_parser

show_words = False

ROOT = '**'

def is_balanced(s):
    def check(l,r):
        if l not in s and r not in s: return True
        if l not in s and r in s: return False
        d = 0
        for c in s:
            if c==l: d += 1
            if c==r: d -= 1
            if d<0: return False
        return d==0
    return check('(',')') and check('[',']') and check('{','}')

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

def dot_clean(s, node_label=False):
    # s = s.replace('$','N_').replace('^','_')
    if node_label:
        #not show_words:
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
    gray = '"#606060"'
    
    def idx(items, elt, default=None):
        if elt not in items: return default
        return items.index(elt)
    
    for head,child,label in sorted(parse.node_edges, key=lambda (h,c,l): (idx(parse.tokens, next(iter(parse.n2w.get(h,{None})))), idx(parse.tokens, next(iter(parse.n2w.get(c,{None})))))):
        if child=='W('+ROOT+')' and label not in ('fe*','Anaph'): raise Exception("The root node "+ROOT+" cannot be a dependent except as fehead or Anaph.")
        # TODO: if ROOT is an fehead, the above doesn't verify that the FE is the root of the annotation graph
        child=dot_clean(child)
        head=dot_clean(head)
        col = {None:darkblue, 'Conj':conjcol, 'Anaph':'purple', 'unspec':gray}.get(label, 'blue')
        dir = {'Anaph':'none'}.get(label, 'back')
        constraint = 'constraint="false"' if label=='Anaph' else ''
        lab = '' if not label else label
        e = '{head} -> {child} [color={col} fontsize={fontsize} fontcolor={col} dir={dir} {constraint} label="{lab}"]'.format(**locals())
        G.append(e)
    
    ## Node information
    for node in parse.nodes:
        #label = re.sub(r'\(.*','', node)
        label = node
        bg = conjbg if node.startswith('$') or node.startswith('FE') else '"#d0d0f0"'
        G.append('{name} [color={bg} style=filled fillcolor={bg} height=0.4 fontcolor=black label={label} fontsize={fontsize}]'.format(
            name=dot_clean(node), label=dot_clean(label, node_label=True), fontsize=fontsize, bg=bg))

    seen_words = set()

    # standard node-word edges only when "show_words" flag is on
    if show_words:
        for node,words in parse.n2w.items():
            node = dot_clean(node)
            # emit edges in surface order ... graphviz seems to respect this a little bit.
            words = sorted(words, key=parse.tokens.index)
            for w in words:
                w = dot_clean(w)
                seen_words.add(w)
                e = '%s -> %s [color=gray weight=1 dir=none]' % (node, w)
                G.append(e)

    '''
    # all the funky node-word edges (e.g. coordinators) are always shown
    for node,conjs,coords in parse.coords:
        node = dot_clean(node)
        for w in coords:
            w = dot_clean(w)
            seen_words.add(w)
            lab = 'Coord'
            e = '{node} -> {w} [color={conjcol} fontcolor={conjcol} fontsize={fontsize} weight=2 dir=none label={lab}]'.format(**locals())
            G.append(e)
    '''
    
    # styling for word boxes
    for word in seen_words:
        col = '"#e0e0e0"'
        G.append("{word} [shape=box fillcolor={col} style=filled color={col} height=0.1 width=0.1 fontsize={wfontsize}]".format(**locals()))

    s = '\n'.join(L+';' for L in G)
    return 'digraph {\n %s \n}' % s

def print_html(out, anno_text, png):
    img = '' if not png else "<img src={}>".format(os.path.basename(png))
    print>>out, u"""
    <hr>
    <pre>{anno_text}</pre>
    <p>{img}
    """.format(**locals())
    #print>>out, """
    #<table><tr><td style="padding-right:20px; vertical-align:top">
    #    <pre>{anno_text}</pre>
    #<td style="vertical-align:top"><img src={png}>
    #</table>
    #""".format(**locals())

def print_header(out):
    print>>out, """
    <style>
    pre {
        font-family: times, serif;
        white-space: pre-wrap;             /* css-3 */
        white-space: -moz-pre-wrap;    /* Mozilla, since 1999 */
        white-space: -pre-wrap;            /* Opera 4-6 */
        white-space: -o-pre-wrap;        /* Opera 7 */
        word-wrap: break-word;             /* Internet Explorer 5.5+ */
    }
    </style>
    <body>
    """

def draw(p, base):
    # base is for OUTPUT
    dot = psf2dot(p)
    with open("{base}.dot".format(**locals()),'w') as f: print>>f, dot
    imgfilename = '{base}.png'.format(base=base)
    cmd = "dot -Tpng < {base}.dot > {imgfilename}".format(**locals())
    print cmd
    os.system(cmd)
    return imgfilename

def desktop_open(filename):
    # TODO how does this work on other platforms
    if 'darwin' in sys.platform:
        os.system("""open "{filename}" """.format(**locals()))
    else:
        print "File is ready to open:    " + filename
        
def process_potentially_multifile(filename):
    # parse container format and return GFL code .. do NOT parse it yet
    with codecs.open(filename, 'r', 'utf-8') as inF:
		anno_text = inF.read().strip()
		if '%' not in anno_text:
			tokens = string.letters
			code = anno_text
			return [(tokens, code, anno_text)]
		anno_text = anno_text.replace('\r\n','\n')
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

def is_json(s):
    try:
        json.loads(s)
        return True
    except ValueError:
        return False

def file_is_json(filename):
    toplines = list(itertools.islice(open(filename), 5))
    toprows = [L.rstrip('\n').split('\t') for L in toplines]
    if all(is_json(row[-1]) for row in toprows):
        return True
    return False

def filesafe_name(s):
    s = s.replace("/",".").replace(" ","_")
    return s

def main(args, show_words=False, suppress_open=False, VERBOSE=False, open_html=False):
	
    import string

    batch_mode = len(args) > 1
    do_open = not batch_mode and not suppress_open
    multi_mode = None
    multi_annos = None
	
	
	
    if not args:
        print "(use -h for help)"
        args = ['/dev/stdin']


    def parseiter(filename):
        if file_is_json(filename):  # JSON input
            assert filename != '/dev/stdin', "can't view JSON on stdin sorry!"
            with codecs.open(filename, 'r', 'utf-8') as inF:
				for i,line in enumerate(inF):
					row = line.rstrip('\n').split('\t')
					sentid = row[0]
					obj = json.loads(row[-1])
					parse = gfl_parser.Parse.from_json(obj)
					anno_text = u' '.join(obj['tokens'])
					yield anno_text,parse
        else:   # GFL annotation input
            tokens_codes_texts = process_potentially_multifile(filename)
            for tokens,code,text in tokens_codes_texts:
                if not code or not tokens:
                    yield text,None
                else:
                    try:
                        if not is_balanced(code):
                            raise Exception("Unbalanced parentheses, brackets, or braces in annotation:\n"+code)
                        if VERBOSE:
                            print 'Parsing: '+str(tokens)
                        parse = gfl_parser.parse(tokens, code, check_semantics=True)
                        yield text,parse
                    except Exception:
                        print code
                        if not batch_mode: raise
                        traceback.print_exc()
                        yield text,None

    def make_images(filename, bigbase):
        for i,(anno_text,parse) in enumerate(parseiter(filename)):
            assert parse,(i,anno_text,parse)
            smallbase = '{}.{}'.format(bigbase,i)
            imgfilename = draw(parse, smallbase)
            yield anno_text,imgfilename

    for filename in args:
        print "FILE",filename
        if filename=='/dev/stdin':
            bigbase = 'tmp'
        else:
            bigbase = re.sub(r'\.(txt|anno)$','', filename)
        
        
        #os.system("rm -f {bigbase}.*.png".format(**locals()))
        
        inputAndImage = list(make_images(filename, bigbase))
        # if processing massive amounts of data, this can be refactored so the parses are 
        # processed one at a time and not stored in memory
        
        ashtml = (open_html or len(inputAndImage)>1)
        if ashtml:
            htmlfilename = bigbase + '.html'
            with codecs.open(htmlfilename, 'w', 'utf-8') as htmlF:
                for anno_text,imgfilename in inputAndImage:
                    print_html(htmlF, anno_text, imgfilename)
                if do_open:
                    desktop_open(htmlfilename)
        else:
            for anno_text,imgfilename in inputAndImage:
                if do_open:
                    desktop_open(imgfilename)
					

	
if __name__=='__main__':
	from optparse import OptionParser
	p = OptionParser(usage="""
	%prog filename.anno  [or multiple files]
	Visualizes a GFL annotations file via GraphViz (as an image file).
	Also can handle a file with multiple annotations in it (outputs HTML)""")
	p.add_option('-w', dest="show_words", action='store_true', help="show words in graph")
	p.add_option('-n', dest="suppress_open", action='store_true', help="force to not open image when done")
	p.add_option('-v', dest="verbose", action='store_true', help="verbose mode")
	p.add_option('-m', dest="open_html", action='store_true', help="force to open html, not png, version")
	(opts, args) = p.parse_args()
	main(args, show_words=opts.show_words, suppress_open=opts.suppress_open, VERBOSE=opts.verbose, open_html=opts.open_html)
    

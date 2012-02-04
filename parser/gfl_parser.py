"""
Parse the high-level annotation format.
("psfParser.py" is the ANTLR parser.)

Run tests with:
  py.test -v gfl_parser.py

Remember: CHILD points to HEAD
HEAD < CHILD
HEAD < {CHILD CHILD}
CHILD > HEAD
"""

import sys,itertools,re,string
from collections import defaultdict
try:
  import ujson as json
except ImportError:
  import json

VERBOSE = False

import antlr3
from psfLexer import psfLexer
from psfParser import psfParser

alltypes = "COMMENT DCOLON DOLLARTOKEN EQ EOF INTTAG LARROW LCB LRB LSB NEWLINE RARROW RCB RRB RSB TOKEN Tokens VOCTAG WS".split()
from psfLexer import COMMENT,DCOLON,DOLLARTOKEN,EOF,EQ,INTTAG,LARROW,LCB,LRB,LSB,NEWLINE,RARROW,RCB,RRB,RSB,TOKEN,Tokens,VOCTAG,WS
import psfLexer as psfLexer_module
TypeNames = {getattr(psfLexer_module,n):n for n in alltypes}
if 0 not in TypeNames: TypeNames[0] = 'type0'

UndirectedEdges = ['Anaph']

class Parse:
  """please only use the methods to manipulate state"""
  def __init__(self):
    self.tokens = []         ## strings
    self.node2words = defaultdict(set)   ## node-word edges, grouped by node
    self.extra_node2words = defaultdict(set)   ## (word,label) pairs
    self.node_edges = set()  ## (head, child, label) ... all strings

    self.node_blacklist = set()  ## just to make correctness easier
    self.node_whitelist = set()
  
    # these get filled only at finalize()
    self.node2id = defaultdict(int)
    self.word2id = {}  ## will be surface positions
    self.word2nodes = defaultdict(set)
    self.nodes = set()
    self.is_finalized = False

  def finalize(self):
    self.gc()
    self.nodes = set(self.node2words)
    for x in flatten((h,c) for h,c,_ in self.node_edges):
      self.nodes.add(x)
    self.node2id = {n:i for i,n in enumerate(sorted(self.nodes))}
    self.word2id = {w:i for i,w in enumerate(self.tokens)} ## overwrites duplicates. assuming duplicates are lame, like punctuation
    for n,words in self.node2words.items():
      for w in words:
        self.word2nodes[w].add(n)
    self.node2words = dict(self.node2words)
    self.extra_node2words = dict(self.extra_node2words)
    self.is_finalized = True

  ## Accessors

  def has_node_edge(head, child, label=None):
    assert False, "unimplemented"

  def wordnode(self, word):
    """Get the node for this word, if any."""
    assert self.is_finalized
    ns = self.word2nodes[word]
    if len(ns)==0: return None
    if len(ns)==1: return list(ns)[0]
    assert len(ns) <= 1, "more than one node for a word... shouldnt this be impossible?"

  def multiword_canonical_node(self, words):
    swords = set(words)
    for n,nodewords in self.node2words.items():
      if swords == nodewords:
        return n
    return None



  ## State manipulation

  def add_node_edge(self, head, child, label=None):
    """
    Default: add a standard directed edge.
    If the label is for an undirected edge, put it in all special.
    """
    #print "ADDING",child," > ", head
    assert (head not in self.node_blacklist) and (child not in self.node_blacklist)
    if label in UndirectedEdges:
      node_order = sorted([head,child])
      self.node_edges.add((node_order[0], node_order[1], label))
    else:
      self.node_edges.add((head,child,label))

  def add_nodeword_edge(self, node, word, label=None):
    """node and word are strings"""
    if label is None:
      self.node2words[node].add(word)
    else:
      self.extra_node2words[node].add((word,label))

  def delete_node(self, node):
    """unfortunately it looks like we need to support this operation"""
    if node in self.node2words: del self.node2words[node]
    if node in self.node2id: del self.node2id[node]
    if any(a==node or b==node for a,b,_ in self.node_edges):
      assert False, "a node is being deleted that already has dependency edges... is something wrong?"
    self.node_blacklist.add(node)

  ## END State manipulation

  def gc(self):
    # need to garbage collect stranded wordnodes
    wordnodes = {n for n in self.node2words if len(self.node2words[n])==1}
    nodes_with_edges = set(flatten((h,c) for h,c,_ in self.node_edges))
    orphan_wordnodes = wordnodes - nodes_with_edges
    orphan_wordnodes = [x for x in orphan_wordnodes if not x.startswith('$')]
    #print "BAD NODES", orphan_wordnodes
    for n in orphan_wordnodes:
      del self.node2words[n]

    
  def to_json(self, numberize=False):
    assert self.is_finalized
    assert not numberize, "numberization not implemented yet"
    d = {}
    d['node2words'] = {k:list(v) for k,v in self.node2words.items()}
    d['extra_node2words'] = {k:list(v) for k,v in self.extra_node2words.items()}
    d['node_edges'] = list(sorted(self.node_edges))
    d['tokens'] = self.tokens
    d['nodes'] = list(sorted(self.nodes))
    #d['node2id'] = dict(self.node2id)
    #d['word2id'] = dict(self.word2id)

    return d

  def __repr__(self):
    d = self.to_json()
    s = "Parse:"
    s += "\n\tnode_edges: " + json.dumps(d['node_edges'])
    s += "\n\tnode2words: " + json.dumps(d['node2words'])
    s += "\n\textra_node2words: " + json.dumps(d['extra_node2words'])
    s += "\n"
    return s

def unicodify(s, encoding='utf8', *args):
  "Safely translate anything into a unicode object"
  if isinstance(s,unicode): return s
  if isinstance(s,str): return s.decode(encoding, *args)
  return unicode(s)

def parse(text_tokens, psf_code):
  """ text_tokens is a list of strings, psf_code is a string """
  text_tokens = [unicodify(x) for x in text_tokens]
  parsetree = antlr_parse(psf_code)
  tree = parsetree.tree
  all_leaves = list(leaves(tree))
  if not all_leaves:
    raise ParseError("no leaves in AST")
  if VERBOSE:
    print text_tokens
    antlr_dump(tree) # DEBUG

  consistency_check(text_tokens, tree)

  p = Parse()
  p.tokens = text_tokens[:]

  if tree.getType() == 0:
    tops = tree.children
  else:
    tops = [tree]

  for fragment in tops:
    typ = fragment.getType()

    if typ == TOKEN:  # singleton
      continue
    elif typ in (LARROW, RARROW, LSB):
      process_chain(p, fragment)
    elif typ == EQ:
      equands = [process_chain(p,c) for c in fragment.children]
      equands = flatten(equands)
      N = len(equands)
      for i in range(N):
        for j in range(i+1, N):
          p.add_node_edge(equands[i], equands[j], 'Anaph')
    elif typ == DCOLON:
      nodevar = fragment.children[0]
      if nodevar.getType() != DOLLARTOKEN:
        raise ParseError("need node variable name at start of double-colon declaration")
      nodename = nodevar.token.text

      head_nodes = process_chain(p, fragment.children[1])
      if len(fragment.children) > 2:
        extra_nodes = process_chain(p, fragment.children[2])
      else:
        extra_nodes = []

      #head_words = flatten(p.node2words[n] for n in head_nodes)
      extra_words = flatten(p.node2words[n] for n in extra_nodes)
      for n in head_nodes:
        p.add_node_edge(nodename, n, 'Conj')
      for w in extra_words:
        p.add_nodeword_edge(nodename, w, 'Coord')

    else:
      assert False, "bad type %s %s" % (typ, TypeNames[typ])
  p.finalize()
  return p

def show(antlr_node):
  n=antlr_node
  print TypeNames[n.getType()], n.token

def process_chain(p, antlr_node):
  """ this function does dispatch among all parse node types """
  n = antlr_node
  #print "PROCESSING",; show(n)
  # return the HEAD(s) of the chain (can be more than one for multiheaded multiwords)
  # ... returned as Node ID's
  # while we're at it, add in all appropriate edges to the Parse 'p'
  if n.getType() == TOKEN:
    nodename = 'W(' + n.token.text + ')'
    p.add_nodeword_edge(nodename, n.token.text)
    return [nodename]
  elif n.getType() == DOLLARTOKEN:
    nodename = n.token.text
    return [nodename]
  elif n.getType() == RARROW:
    return process_head_child(p, n.children[1], n.children[0])
  elif n.getType() == LARROW:
    return process_head_child(p, n.children[0], n.children[1])
  elif n.getType() == LCB:  # {
    children_heads = [process_chain(p,c) for c in n.children]
    nodes = flatten(children_heads)
    return nodes
  elif n.getType() == LSB:  # [
    children_heads = [process_chain(p,c) for c in n.children]
    wordnodes = flatten(children_heads)

    word_lists = [p.node2words[wn] for wn in wordnodes]
    assert all(len(x)==1 for x in word_lists)
    words = flatten(word_lists)
    # sorting is better for string comparability, but order-preserving is nicer for interpretation
    #mw_node = 'MW(' + ','.join(sorted(words)) + ')'
    n = p.multiword_canonical_node(words)
    mw_node = n if n else 'MW(' + ','.join(words) + ')'
    for w in words:
      p.add_nodeword_edge(mw_node, w)
    #for n in wordnodes:
    #  p.add_node_edge(mw_node, n)

    return [mw_node]

  else:
    assert False, "unsupported type %s %s" % (n.getType(), TypeNames[n.getType()])

def flatten(iter):
  return list(itertools.chain.from_iterable(iter))

def process_head_child(p, head, child):
  """ head,child are ANTLR nodes """
  head_headnodes = process_chain(p, head)
  child_headnodes= process_chain(p, child)
  # crossproducting both sides allows multiple parents
  for x in head_headnodes:
    for y in child_headnodes:
      p.add_node_edge(x,y)

  return head_headnodes


def is_node(antlr_node):
  t = antlr_node.token
  return (t is not None) and t.text.startswith('$')

def leaves(antlr_node):
  node = antlr_node
  if not node.children and (node.token is not None):
    yield node
  for child in node.children:
    for x in leaves(child):
      yield x

def consistency_check(text_tokens, tree):
  # References check
  alltoks = set(text_tokens)
  for leaf in leaves(tree):
    if is_node(leaf): continue
    if leaf.token.text not in alltoks:
      raise ParseError("Word %s not in original text" % repr(leaf.token.text))
      
  # Duplicates check
  counts = defaultdict(int)
  for t in text_tokens: counts[t] += 1
  duplicated_tokens = set(k for k in counts if counts[k] > 1)
  for leaf in leaves(tree):    
    t = leaf.token.text
    if t in duplicated_tokens:
      raise ParseError("Reference to a duplicate token: %s" % t)
  
  # TODO special multiword check

class ParseError(Exception): pass

def antlr_parse(code):
  if isinstance(code,str): code = code.decode('utf8')
  char_stream = antlr3.ANTLRStringStream(code)
  lexer = psfLexer(char_stream)
  tokens = antlr3.CommonTokenStream(lexer)
  parser = psfParser(tokens)
  parsetree = parser.annotate()
  if parsetree.tree is None:
    raise ParseError("failed to parse")
  return parsetree

def antlr_dump(node, indent=0):
  print "{indent} {typ} {info}".format(
      indent=' '*(indent*4), 
      typ = TypeNames[node.getType()],
      info=node.token if node.token else repr(node),
      #s=node.token.text if node.token else ''
      )
  if node.children:
    for c in node.children:
      antlr_dump(c, indent=indent+1)

def clean_code(code):
  return re.sub(r'\n +','\n', code.strip())

#############################################

def goparse(tokens, code):
  code = clean_code(code)
  if VERBOSE:
    print "\n---\n" + code
    ap = antlr_parse(code); antlr_dump(ap.tree); print ""
  p = parse(tokens, code)
  if VERBOSE:
    print p; print ""
  return p

def test_simple():
  go = lambda c: goparse(string.letters, c)
  assert_same(go("a < b < c"), go("a < (b < c)"))
  assert_same(go("a < b < c"), go("a < b \n b < c"))
  assert_same(go("a > b"), go("b < a"))
  assert_same(go("a > b > c"), go("(a > b) > c"))

def test_parentheses():
  go = lambda c: goparse(string.letters, c)
  assert_same(go("a < b < c"), go("a < (c > b)"))
  assert_same(go("a < b < c"), go("a < (c > b)"))

def test_curlysets():
  go = lambda c: goparse(string.letters, c)
  assert_same(go("a < {b c}"), go("a < b \n a < c"))
  assert_same(go("a > {b c}"), go("a > b \n a > c"))
  assert_same(go("a > {b c} > d"), go("a > b \n a > c \n b > d \n c > d"))

def test_multiwords():
  go = lambda c: goparse(string.letters, c)
  p = go("[a b]")
  assert len(p.nodes)==1
  mw = list(p.nodes)[0]
  assert set(p.node2words[mw]) == set(['a','b'])

  p = go("z > [a b]")
  assert len(p.nodes)==2
  assert set(p.node2words['MW(a,b)']) == set(['a','b'])
  assert set([('MW(a,b)','W(z)',None)]) == set(p.node_edges)
  p = go("[a b] > {c d}")
  assert_same(go("[a b] > {c d}"), go("[a b] > c \n [a b] > d"))

def test_multiwords_consistency():
  go = lambda c: goparse(string.letters, c)
  p = go("[a b] \n [b a]")
  assert len(p.nodes) == 1

def test_empty_nodes():
  go = lambda c: goparse(string.letters, c)

  def N(p, word):  ## get the node for this word
    ns = p.word2nodes[word]
    assert len(ns)==1
    return list(ns)[0]

  empty = go("a > $x > b")
  print empty
  assert '$x' not in empty.node2words
  assert ('$x', N(empty,'a'),None) in empty.node_edges

def test_coordination():
  go = lambda c: goparse(string.letters, c)
  p = go("$x :: b :: p")
  print p
  p = go("$x :: {b c} :: {p q}")
  print p
  # ugh too annoying to check programmatically.  The following output is correct right now:
#psf_parser.py:328: test_coordination Parse:
#        node_edges: [["$x","W(b)","Conj"]]
#        node2words: {"W(b)":["b"]}
#        extra_node2words: {"$x":[["p","Coord"]]}
#
#Parse:
#        node_edges: [["$x","W(b)","Conj"],["$x","W(c)","Conj"]]
#        node2words: {"W(c)":["c"],"W(b)":["b"]}
#        extra_node2words: {"$x":[["q","Coord"],["p","Coord"]]}

def test_anaphora():
  go = lambda c: goparse(string.letters, c)
  p = go("a > b > c \n a = c")
  assert ('W(a)','W(c)','Anaph') in p.node_edges

def test_complex():
  tokens = "one of the good players".split()
  go = lambda c: goparse(tokens,c)
  assert_same(
    go("one < of < ({the good} > players)"), 
    go("""
      one < of
      of < players
      the > players
      good > players
      """))
  
def test_football_wives():
  tokens = "@ciaranyree it was on football wives , one of the players and his wife own smash burger".split()
  go = lambda c: goparse(tokens,c)
  assert_same(go( """
    @ciaranyree
    it > was < on < [football wives] 
    , 
    one < of < (the > players)
    and
    his > wife 
    $x :: {one wife} :: and
    $x > own < [smash burger]
  """), go("""
    it > was
    was < on
    on < [football wives]
    one < of
    of < players
    the > players
    his > wife
    $x :: {one wife} :: and
    $x > own
    own < [smash burger]
  """))

def test_duplication_checking():
  import pytest
  tokens = "A B C A A".split()
  # This is bad
  with pytest.raises(ParseError):
    goparse(tokens, "A > B")
  # This is OK
  goparse(tokens, "B > C")


def assert_same(p1, p2):
  # Note this is a pretty lame test, it assumes nodes have common names between parses.
  # A better way to do this would be unification with prolog variables binding to nodes,
  # so then you get structure alignment.
  # But in the meantime...
  assert set(p1.node_edges)==set(p2.node_edges)
  assert p1.nodes==p2.nodes

if __name__=='__main__':
  code = '\n'.join(sys.argv[1:])
  VERBOSE = True
  goparse(string.letters, code)

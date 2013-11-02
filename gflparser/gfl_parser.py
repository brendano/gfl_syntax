#!/usr/bin/env python2.7
#coding=utf-8
'''
PEG (parsing expression grammar)-based parser for GFL.
Uses the Parsimonious library (https://github.com/erikrose/parsimonious).
The grammar is loaded from the file gfl1.peg.
When called directly, this script runs some cursory unit tests.

@author: Nathan Schneider (nschneid@cs.cmu.edu)
@since: 2013-03-08
'''
from __future__ import print_function
import os, sys, re, fileinput, json
from pprint import pprint
from collections import defaultdict, namedtuple

from parsimonious.grammar import Grammar

class FixedDict(dict):
    '''Dict subclass which prevents reassignment to existing keys (unless the assigned value matches the stored value).'''
    
    def __setitem__(self, key, newvalue):
        if key in self and self[key]!=newvalue:
            raise KeyError('FixedDict cannot reassign to key {0!r} (current: {1!r}, new value: {2!r})'.format(key,self[key],newvalue))
        dict.__setitem__(self, key, newvalue)


class GFLError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


_GFLParse = namedtuple('GFLParse', 'tokens n2w w2n varnodes ww2fe deps anaph coords')
class GFLParse(_GFLParse):
    @property
    def node_edges(self):
        return {(h,d,l) for h,d,l in self.deps} \
            | {(a,b,'Anaph') for a,b in self.anaph} \
            | {e for v,conjuncts,coordinators in self.coords for h in coordinators for d in conjuncts for e in [(v,d,'Conj'),(v,h,'Coord')]}

    @property
    def nodes(self):
        '''Includes lexical nodes, coordination nodes, fudge nodes, and the special root node ** if it is used'''
        allnodes = self.n2w.keys() + list(self.varnodes) + self.ww2fe.values()
        if any(1 for h,d,l in self.deps if h=='**'):
            allnodes.append('**')
        assert len(set(allnodes))==len(allnodes)
        return allnodes
    
    def to_json(self):
        '''Return an object suitable for serialization into JSON'''
        d = self._asdict()
        d["nodes"] = self.nodes
        d["node_edges"] = self.node_edges
        if "ww2fe" in d:
            del d["ww2fe"] # key is an object (a set), JSON requires a string. remove, convert to pairs, or use repr()?
        for k,v in d.items():
            if k=='coords':
                d[k] = [(a,list(b),list(c)) for a,b,c in v]
            elif isinstance(v,set):
                d[k] = tuple(v)
            elif k=='w2n':
                #d[k] = {tuple(k2): v2 for k2,v2 in v.items()}
                del d[k]    # key is an object (a set), JSON requires a string. remove, convert to pairs, or use repr()?
            elif k=='n2w':
                d[k] = {k2: tuple(v2) for k2,v2 in v.items()}
        return d

def visit(n,l=0):
    '''Visualize the output of the Parsimonious parser'''
    print('.'*l, n.expr_name, '|', n.text)
    for c in n.children:
        visit(c,l+1)

def walk(n):
    '''Simplify the Parsimonious parse tree to a list/tuple/string representation'''
    t = n.expr_name
    if t=='ALL':
        return [walk(c) for c in n.children]
    elif t in ('LINE','L','F','FD'):
        assert len(n.children)==1
        x = walk(n.children[0])
        if t=='L' and len(x)>1:
            assert x[0]=='[' and x[-1]==']',repr(x)
            x = x[1:-1]
        elif t in ('F','FD'):
            assert x[0]=='(' and x[-1]==')',(t,x)
            x = x[1:-1]
        return (t, x)
    elif t in ('E','e','D','d'):
        return filter(None,[walk(c) for c in n.children])
    elif t in ('Fh','FDh'):
        x = filter(None,[walk(c) for c in n.children])
        return (t, x)
    elif t in ('S','s'):
        x = filter(None,[walk(c) for c in n.children])
        assert x[0]=='{' and x[-1]=='}'
        x = x[1:-1]
        x = x[0][0]+([q[0] for q in x[1]] if len(x)==2 else [])
        return (t, x)
    elif t in ('t','v'):
        return [n.text]
    elif t=='':
        if not n.children:
            return n.text.strip()
        elif len(n.children)==1:
            return walk(n.children[0])
        else:
            x = filter(None,[walk(c) for c in n.children])
            return [y for a in x for y in (a if not isinstance(a,(basestring,tuple)) else [a])]
    elif t in ('_backtick', '_'):
        assert not n.children
        return None
    else:
        assert False,(t,n.text,n.children)

def clean(s):
    return re.sub('\n[ \t]+', ' ', re.sub(r'#.*','',s.replace('\t',' ').replace('`','_backtick')))

def analyze(tokens, tree, ignore_order=False):
    '''Analyze the simplified tree into meaningful GFL annotation graph structures (nodes and edges).'''
    n2w = FixedDict()
    w2n = FixedDict()
    ww2fe = FixedDict()
    deps = set()
    anaph = set()
    coords = set()
    coordvars = set()
    varnodes = set()
    # by the end of the annotation, varnodes should be a subset of coordvars
    
    if not ignore_order:
        assert tokens
    
    def traverse(n):
        if isinstance(n,list):
            if len(n)==0: return None   # empty line
            elif len(n)==1: return traverse(n[0])
            elif n[0]=='(' and n[-1]==')':
                n = n[1:-1]
        
        if '=' in n:  # anaphoric link
            assert '**' not in n
            itms = [traverse(c) for c in n[::2]]
            for a,b in zip(itms,itms[1:]):
                anaph.add((a,b))
        elif '::' in n: # coordination
            if n[1]=='**':
                deps.add(('**',n[0]))
                n = n[:1]+n[2:]
            v, a, j, b, c = n
            assert a==b=='::'
            assert v.startswith('$')
            
            j = traverse(j)
            c = traverse(c)
            assert isinstance(j,set)
            if not isinstance(c,set):   # coordinator is a single lexical item
                c = [c]
            coords.add((v,frozenset(j),frozenset(c)))
            coordvars.add(v)
        elif n=='**':   # ** appearing as first item in a fudge expression (FE)
            return n
        elif isinstance(n,basestring) and n.startswith('$'):    # variable
            w2n[frozenset([n])] = n
            n2w[n] = {n}
            varnodes.add(n)
            return n
        elif isinstance(n,tuple):
            t, x = n
            if t=='L':  # lexical node
                # there may be lexical nodes starting with a $ sign, like $250
                for w in x:
                    if not ignore_order and tokens.count(w)!=1:
                        raise GFLError('Token in lexical node must occur exactly once in the input: {}'.format(w))
                nname = 'W('+'_'.join(sorted(x, key=(None if ignore_order else tokens.index)))+')'
                if len(x)>1: nname = 'M'+nname
                if frozenset(x) not in w2n and any(frozenset(x) & k for k in w2n):
                    raise GFLError('Lexical expression must not share any tokens in common with another lexical expression: {}'.format(tuple(x)))
                w2n[frozenset(x)] = nname
                n2w[nname] = set(x)
                return nname
            elif t=='LINE':
                if '=' in x or '::' in x:
                    traverse(x)
                    return
            
                # break into basic expressions, as indicated by vertical bars: a | b > c < d < {e f} | g ** < h
                prevtype = None
                expr = []
                order = ['>', '', '**', '<']
                for c in x:
                    
                    if c=='**':
                        curtype='**'
                        assert prevtype==''
                    elif isinstance(c,tuple):
                        curtype = ''
                    elif isinstance(c,list):
                        if c[0]=='<': curtype = '<'
                        elif c[-1]=='>': curtype = '>'
                        else: curtype = ''
                    else:
                        assert False,c
                        
                    if prevtype is not None and (curtype==prevtype=='' or order.index(curtype)<order.index(prevtype)):
                        traverse(expr)
                        expr = []
                    expr.append(c)
                        
                    prevtype = curtype
                if expr:
                    traverse(expr)
                return
            elif t in ('S','s'):
                return {traverse(c) for c in x}
            elif t in ('F','FD'):
                if isinstance(x[0],tuple) and x[0][0] in ('Fh','FDh'):
                    assert len(x[0][1])==1
                    assert '*' in x[0][1][0]
                    rhs = x[0][1][0]
                else:
                    assert len(x)>1
                    assert '*' not in x
                    rhs = x
                members = []
                rightward = None
                leftward = None
                fehead = None
                for i,c in enumerate(rhs):
                        if c=='*':
                            assert rightward is None
                            assert fehead is None
                            fehead = members[-1]
                            continue
                        if c[-1]=='>':
                            assert len(c)%2==0
                            for k in range(0,len(c),2):   # possibly a chain: d2 > d1 > ...
                                assert c[k+1]=='>'
                                d = traverse(c[k])
                                if rightward is not None:
                                    for rw in (rightward if isinstance(rightward,set) else [rightward]):
                                        deps.add((d,rw))
                                rightward = d
                        elif c[0]=='<':
                            assert len(c)%2==0
                            assert leftward is not None
                            for k in range(1,len(c),2): # possibly a chain: < d1 < d2 ...
                                assert c[k-1]=='<'
                                d = traverse(c[k])
                                for dnode in (d if isinstance(d,set) else [d]):
                                    deps.add((leftward,dnode))
                                leftward = d
                            leftward = None
                        else:
                            c = traverse(c)
                            if c=='**':
                                if i==0:
                                    fehead = c
                                    members.append(c)
                                else:
                                    assert leftward is not None
                                    assert leftward in members
                                    deps.add(('**', leftward))
                            else:
                                members.append(c)
                                if rightward is not None:
                                    if not isinstance(rightward,set):   # TODO: need similar check for leftward?
                                        rightward = {rightward}
                                    for r in rightward:
                                        deps.add((c,r))
                                    rightward = None
                                leftward = c
                        
                
                    
                f = ww2fe.setdefault(frozenset(members), 'FE'+str(len(ww2fe)+1))
                if fehead is not None:
                    deps.add((f,fehead,'fe*'))
                for member in set(members)-{fehead}:
                    deps.add((f,member,'fe'))
                return f
            else:
                assert False,(t,w2n,n)
        
        else:
            assert isinstance(n,list),n
            
            
            if len(n)==1:
                assert '**' not in n
                c = traverse(n)
                return c
                
            starstar = False
            if '**' in n:
                starstar = True # applies to the central item (head) of the expression
                n.remove('**')
                if len(n)==1:
                    c = traverse(n)
                    deps.add(('**',c))
                    return c
            
            if len(n)==3:
                l, c, r = n
            elif len(n)==2:
                assert (n[0][-1]=='>') ^ (n[1][0]=='<'),n
                if n[0][-1]=='>':
                    l, c = n
                    r = []
                else:
                    c, r = n
                    l = []
            else:
                assert False,n
            
            l[::2] = [traverse(q) for q in l[::2]]
            c = traverse(c)
            if starstar:
                deps.add(('**',c))
            r[1::2] = [traverse(q) for q in r[1::2]]
            if l:
                assert set(l[1::2])=={'>'},n
                for dd,h in zip(l[::2],l[2::2]+[c]):
                    for d in (dd if isinstance(dd,set) else [dd]):
                        deps.add((h,d))
            if r:
                assert set(r[::2])=={'<'}
                for h,dd in zip([c]+r[1::2],r[1::2]):
                    for d in (dd if isinstance(dd,set) else [dd]):
                        deps.add((h,d))
            return c
            
    for ln in tree:
        traverse(ln)
    
    if not varnodes<=coordvars:
        raise GFLError('Variable(s) not defined in any coordination: {}'.format(', '.join(varnodes-coordvars)))
    varnodes = coordvars
    
    # remove variables from node-word mappings
    for v in varnodes:
        if v in n2w:    # TODO: why for football_wives but not nietzsche?
            del n2w[v]
            del w2n[frozenset([v])]
    return GFLParse(tokens=tokens, n2w=n2w, w2n=w2n, varnodes=varnodes, ww2fe=ww2fe, deps=[e+(None,) if len(e)==2 else e for e in deps], anaph=anaph, coords=coords)


def graph_semantics_check(parse):
    """Do checks on the final parse graph -- these are linguistic-level checks,
    not graph definition checks.
    
    This doesn't attempt to do fancy reasoning about FEs. 
    E.g., a < (b* c d) precludes a < c, but this conflict will not be caught here.
    """
    # Check tree constraint over each fragment
    roots = set()
    rootFor = {}
    
    for n in parse.nodes:
        outbounds = [(h,c,l) for h,c,l in parse.node_edges if c==n and l not in {'Anaph','fe*','fe'}]
        if len(outbounds) > 1:
            raise GFLError("Violates tree constraint: node {} has {} outbound edges: {}".format(
                                                        repr(n), len(outbounds), repr(outbounds)))
        elif len(outbounds)==0:
            roots.add(n)
        elif n=='**':
            raise GFLError("Special root symbol ** cannot be a dependent")
        else:
            h, c, _ = outbounds[0]
            r = rootFor.setdefault(h,h)
            rootFor[c] = r
            for k,v in rootFor.items():
                if v==c:
                    rootFor[k] = r
    if not roots:
        raise GFLError("Violates tree constraint: no root")
    else:
        for k,v in rootFor.items():
            if v not in roots:
                raise GFLError("Violates tree constraint: no root for node {}".format(repr(k)))


def parse(tokens, gfl, grammar=None, check_semantics=False, ignore_order=False):
    if grammar is None:
        grammar = _grammar  # use module default
    p = grammar.parse(gfl)
    if p is None:
        for ln in gfl.splitlines():
            if grammar.parse(ln) is None:
                raise GFLError('Cannot parse GFL line: '+ln)
        assert False
    # TODO: construct and return the parse data structure
    
    parse = analyze(tokens, walk(p), ignore_order=ignore_order)
    if check_semantics:
        graph_semantics_check(parse)
    
    return parse


def test(inFP):
    with open(inFP) as inF:
        grammar = Grammar(clean(inF.read()))

    good_inputs = ['{the~1 quick brown} > fox > jumps < over < ({the~2 lazy} > dog)', 
                   'They > conspired < to < defenestrate < themselves\n(conspired* to defenestrate on < Tuesday)',
                   'a (** b c) d**', 'a (** b c**)', '::~1 :-)~1 ~(-: (0_0) ~(0_0)~2 *_*~3 )~1 ~( <*_*>',
                   '''
                      Found** < (the scarriest mystery door*)
                      Found < in < (my > school)
                      I’M** < (SO > CURIOUS)
                      D:**
                      my = I’M''',
                   '''
                      thers** < still
                      thers < ((1 1/2) > hours < till < (Biebs > bday))
                      (thers like 1 1/2 hours)
                      thers < here
                      (:P)**''',
                   '''
                      If < (it~1 > 's < restin')
                      I > 'll < [wake up] < it~2
                      If > 'll**
                      it~1 = it~2''',
                   '''
                      {Our three} > weapons > are < $a
                      $a :: {fear surprise efficiency} :: {and~1 and~2}
                      ruthless > efficiency''',
                   '''
                      {Our three} > weapons > are < $a
                      $a** :: {fear surprise efficiency} :: and~1
                      ruthless > efficiency''',
                   '''
                      We > are < knights < the
                      knights < (who > say < Ni)
                      who = knights''',
                   '''
                      (ll > l > (m mm) < r < rr   LL > L > (M < MM) < R < RR)
                   ''',
                   '''
                       ({the~1 whole} > world > returns smile)
                   ''',
                   '''
                       (smile return < world < {the~1 whole})
                   ''']
    bad_inputs = ['{the~1 quick brown} > fox > jumps < over < {the~2 lazy} > dog', 'the~2 > {lazy dog}', 'the~2 < lazy > dog', 
                  'They > conspired* < to < defenestrate < themselves\n(conspired* to defenestrate on < Tuesday)',
                  'big > **', '{** happy} > days', '(my big** fat Greek wedding*)', 'big** > day', 
                  'hi :: there', ':-)', '(-:', '(0_0)~1', '*_*', ') (',
                  '''
                      a > doublehead > b
                      b < c < doublehead
                  ''',
                  '''
                      b > c
                      a > cycle > b
                      a < c
                  ''',
                  '''
                      a > notcycle > c
                      b > c
                      d > cycle > e
                      e > d
                  ''',
                  '''
                     (root and nonroot)**
                     d < (root and nonroot) 
                  ''',
                  #'''    # need fancier checking to catch this conflict
                  #   (root and nonroot)**
                  #   (d* (root and nonroot)) 
                  #''',
                  
                  '''
                      a > cycle
                      $x :: {a b} :: c
                      cycle > b
                   ''']
    for x in bad_inputs:
        try:
            p = parse([], x, grammar, check_semantics=True, ignore_order=True)
            assert False
        except GFLError as ex:
            print(ex)
    for x in good_inputs:
        p = grammar.parse(x)
        assert p is not None
        print(x)
        pprint(analyze([], walk(p), ignore_order=True))

if __name__=='__main__':
    test('gfl1.peg')
else:    # load the default GFL grammar
    with open(os.path.dirname(__file__)+'/gfl1.peg') as inF:
        _grammar = Grammar(clean(inF.read()))


# TODO: error-checking, e.g. at most one fehead per FE, all tokens are unambiguous in input, etc.
# TODO: when naming MW nodes, use token order in input

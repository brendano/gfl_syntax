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
import os, sys, re, fileinput
from pprint import pprint
from collections import defaultdict

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
    elif t=='S':
        x = filter(None,[walk(c) for c in n.children])
        assert x[0]=='{' and x[-1]=='}'
        x = x[1:-1]
        assert len(x)==2
        x = x[0][0]+[q[0] for q in x[1]]
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

def analyze(tree):
    '''Analyze the simplified tree into meaningful GFL annotation graph structures (nodes and edges).'''
    n2w = FixedDict()
    w2n = FixedDict()
    ww2cbb = FixedDict()
    deps = set()
    anaph = set()
    coords = set()
    
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
            v, a, j, b, c = n
            assert a==b=='::'
            assert v.startswith('$')
            j = traverse(j)
            c = traverse(c)
            assert isinstance(j,set) and isinstance(c,set)
            coords.add((v,frozenset(j),frozenset(c)))
        elif n=='**':   # ** appearing as first item in a CBB
            return n
        elif isinstance(n,tuple):
            t, x = n
            if t=='L':  # lexical node
                nname = 'W('+'_'.join(sorted(x))+')'
                if len(x)>1: nname = 'M'+nname
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
            elif t=='S':
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
                cbbhead = None
                for i,c in enumerate(rhs):
                        if c=='*':
                            assert rightward is None
                            assert cbbhead is None
                            cbbhead = members[-1]
                            continue
                        if c[-1]=='>':
                            assert len(c)==2
                            c = traverse(c[0])
                            if rightward is not None:
                                deps.add((c,rightward))
                            rightward = c
                        elif c[0]=='<':
                            assert len(c)==2
                            c = traverse(c[1])
                            assert leftward is not None
                            deps.add((leftward,c))
                            leftward = c
                        else:
                            c = traverse(c)
                            if c=='**':
                                if i==0:
                                    cbbhead = c
                                    members.append(c)
                                else:
                                    assert leftward is not None
                                    assert leftward in members
                                    deps.add(('**', leftward))
                            else:
                                members.append(c)
                                leftward = c
                        
                
                    
                f = ww2cbb.setdefault(frozenset(members), 'CBB'+str(len(ww2cbb)+1))
                if cbbhead is not None:
                    deps.add((f,cbbhead,'cbbhead'))
                for member in set(members)-{cbbhead}:
                    deps.add((f,member,'unspec'))
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
    return n2w, w2n, ww2cbb, deps, anaph, coords


def parse(gfl, grammar):
    p = grammar.parse(gfl)
    if p is None:
        for ln in gfl.splitlines():
            if grammar.parse(ln) is None:
                raise GFLError('Cannot parse GFL line: '+ln)
        assert False
    # TODO: construct and return the parse data structure


def test(inFP):
    with open(inFP) as inF:
        grammar = Grammar(clean(inF.read()))

    good_inputs = ['{the quick brown} > fox > jumps < over < ({the lazy} > dog)', 
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
                      We > are < knights < the
                      knights < (who > say < Ni)
                      who = knights''']
    bad_inputs = ['{the quick brown} > fox > jumps < over < {the lazy} > dog', 'the > {lazy dog}', 'the < lazy > dog', 
                  'They > conspired* < to < defenestrate < themselves\n(conspired* to defenestrate on < Tuesday)',
                  'big > **', '{** happy} > days', '(my big** fat Greek wedding*)', 'big** > day', 
                  'hi :: there', ':-)', '(-:', '(0_0)~1', '*_*', ') (']
    for x in bad_inputs:
        try:
            parse(x, grammar)
            assert False
        except GFLError as ex:
            print(ex)
    for x in good_inputs:
        p = grammar.parse(x)
        assert p is not None
        print(x)
        pprint(analyze(walk(p)))

if __name__=='__main__':
    test('gfl1.peg')

# TODO: error-checking, e.g. at most one cbbhead per CBB, all tokens are unambiguous in input, etc.
# TODO: when naming MW nodes, use token order in input

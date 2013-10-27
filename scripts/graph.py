#!/usr/bin/env python2.7
"""
FUDG graph data structures and algorithms for reasoning about possible FE heads 
(internal a.k.a. 'topcandidates' and external a.k.a. 'parentcandidates').

Some things done here but not in the parser:
- ensure only one fehead child per FE
- ensure no token appears in more than one lexical node
- ensure the root is never attached to anything else
- ensure FEs with identical childsets are merged, without losing fehead information

TODO:
- ensure nodes attaching to root can't also attach to something else unless it is an FE
  (or is this enforced already via the forest-except-FE-edges constraint?)

- prohibit:
[a b]
c > b

[a b]
(b c)

(a* b c)
(a b* c)

@author: Nathan Schneider (nschneid@cs.cmu.edu)
@since: 2013-02-14
"""
from __future__ import print_function, division
import os, sys, re, itertools


class FixedDict(dict):
    '''Dict subclass which prevents reassignment to existing keys.'''
    
    def __setitem__(self, key, newvalue):
        if key in self:
            raise KeyError('FixedDict cannot reassign to key {0!r} (current: {1!r}, new value: {2!r})'.format(key,self[key],newvalue))
        dict.__setitem__(self, key, newvalue)

# from Naomi's code:
class TreeNode(object):
    def __init__(self, name, children):
        self.name = name
        self.children = set(children)

    def add_child(self, child):
        self.children.add(child)

    def remove_child(self, child):
        self.children.remove(child)

    def deepcopy(self):
        return TreeNode(self.name,
                        [child.deepcopy() for child in self.children])
                        

def reachable(n1,n2):
    if n1 is n2: return True
    for c in n1.children:
        if reachable(c,n2): return True

class FUDGNode(TreeNode):
    def __init__(self, *args, **kwargs):
        TreeNode.__init__(self, *args, **kwargs)
        self.childedges = set()
        self.parentedges = set()
        self.parents = set()
        self.height = 0 # length of longest path from this node to a leaf
        self.depth = -1 # length of longest path from a parentless node to this one
        self.frag = Fragment({self}, {self})
    
    def add_child(self, node, label=None):
        assert self.name!=node.name,(self.name,node.name)
        assert not node.isRoot or (self.isFE and label is not None)
        TreeNode.add_child(self, node)
        self.childedges.add((node, label))
        # check for cycles
        if reachable(node, self):
            raise Exception('Adding {0} as a child of {1} would create a cycle!'.format(node,self))
        
        node.parentedges.add((self, label))
        node.parents.add(self)
        self._setMinHeight(node.height+1)
        
        #print(self,'.add_child',node)
        self.frag |= node.frag  # unify the fragments, updating all references from member nodes
        #self.frag.roots.remove(node)   # no longer a root because it has a parent
        self.frag.roots -= {node}   # TODO

        # recompute depths in the entire fragment
        for n in self.frag.nodes:
            n.depth = -1
        for n in self.frag.roots:
            n._setMinDepth(0)
    
    def remove_child(self, child):
        raise Exception('Not supported')
    
    def _setMinHeight(self, h):
        if self.height<h:
            self.height = h
            for p in self.parents:
                assert p.name!=self.name,(self,self.parents)
                p._setMinHeight(h+1)
    
    def _setMinDepth(self, d):
        if self.depth<d:
            self.depth = d
            #print(self,d,self.children)
            for c in self.children:
                c._setMinDepth(d+1)
    
    def __repr__(self):
        return '<'+self.name.encode('utf-8')+'>'
    
    def descendantsIter(self): return itertools.groupby(itertools.chain(self.children, itertools.imap(FUDGNode.descendantsIter, self.children)))
    @property
    def descendants(self): return set(self.descendantsIter())
    
    def get_yield(self): return {tkn for c in self.children for tkn in c.get_yield()}
    
    @property
    def isRoot(self): return isinstance(self, RootNode)
    @property
    def isCoord(self): return isinstance(self, CoordinationNode)
    @property
    def isLexical(self): return isinstance(self, LexicalNode)
    @property
    def isFE(self): return isinstance(self, FENode)
    @property
    def isFirm(self):
        '''i.e. anything but a FE (fudge) node'''
        return self.isRoot or self.isLexical or self.isCoord

class LexicalNode(FUDGNode):
    parentcandidates = None
    
    def __init__(self, name, tokens, token2lexnode):
        assert name!='**'
        FUDGNode.__init__(self, name, [])
        self.tokens = tokens
        for tkn in tokens:
            #assert tkn not in token2lexnode,(tkn,token2lexnode)
            token2lexnode[tkn] = self
            
    def get_yield(self):
        return set(self.tokens) | FUDGNode.get_yield(self)
    
    @property
    def json_name(self):    # not guaranteed to be consistent across invocations!
        return ('M' if len(self.tokens)>1 else '') + 'W('+self.name+')'

class RootNode(FUDGNode):
    def __init__(self, children=None):
        FUDGNode.__init__(self, '**', children or set())
        self.parentcandidates = None
    
    @property
    def json_name(self):
        return '**'

class CoordinationNode(FUDGNode):
    def __init__(self, name, coords, conjuncts=None, modifiers=None):
        FUDGNode.__init__(self, name, [])   # no TreeNode children, as we won't be traversing CoordinationNodes anyway
        self.coords = coords
        self.conjuncts = conjuncts or set()

class FENode(FUDGNode):
    def __init__(self, name, members=None, externalchildren=None, top=None):
        self.top = top
        self.members = members or set()
        self.externalchildren = externalchildren or set()
        self._pointerto = None
        FUDGNode.__init__(self, name, self.members | self.externalchildren)
        self._parentcandidates = None
        self._topcandidates = None

        
    def add_member(self, node, specified_top):
        self.members.add(node)
        if specified_top:
            assert self.top is None,'FE can only have one specified top: '+repr(self.top)+', '+repr(node)
            self.top = node
        FUDGNode.add_child(self, node, label=('top' if specified_top else 'fe'))
        
    def add_child(self, node, **kwargs):
        self.externalchildren.add(node)
        FUDGNode.add_child(self, node, **kwargs)
        
    def become_pointer(self, node):
        '''Merge the two FEs and assume a reference to the other instance'''
        print('MERGE FE ',self,'into',node, file=sys.stderr)
        assert node.isFE
        assert node.members==self.members
        assert (node.top is None) or (self.top is None) or node.top==self.top
        if node.top is None: node.top = self.top
        else: self.top = node.top
        node.height = max(self.height,node.height)
        node.depth = max(self.depth,node.depth)
        for c in self.externalchildren:
            node.add_child(c)
        self.externalchildren = node.externalchildren
        self.members = node.members
        self.children = node.children
        self.parents = node.parents
        self.childedges = node.childedges
        self.parentedges = node.parentedges
        self._pointerto = node
        #assert False
        
    @property
    def json_name(self): return self.name if self._pointerto is None else self._pointerto.name
    
    def __getattr__(self, name):
        if name not in ('parentcandidates', 'topcandidates', 'height', 'depth'):
            raise AttributeError(name)
        if self._pointerto is not None:
            #assert getattr(self._pointerto, '_'+name) is not None,self.__dict__
            return getattr(self._pointerto, '_'+name)
        return self.__dict__['_'+name]
    def __setattr__(self, name, val):
        if name in ('parentcandidates', 'topcandidates', 'height', 'depth'):
            if self._pointerto is not None:
                self._pointerto.__setattr__(name, val)
            else:
                FUDGNode.__setattr__(self, '_'+name, val)
        else:
            FUDGNode.__setattr__(self, name, val)
    
class Fragment(object):
    def __init__(self, roots, nodes):
        self.roots = roots
        for root in roots:
            assert root in nodes
        self.nodes = nodes
        
    def __or__(self, that):
        if self is not that:
            # merge 'that' contents in with 'self'
            self.roots |= that.roots
            self.nodes |= that.nodes
            
            # update node references from 'that' to point to 'self'
            for n in that.nodes:
                n.frag = self
            
        return self

    def __repr__(self):
        return '<Fragment@'+str(id(self))+'> '+str(self.roots)+' '+str(self.nodes)
    
class Graph(object):
    def __init__(self, nodes):
        self.nodes = nodes
        
    @property
    def firmNodes(self):
        return {n for n in self.nodes if n.isFirm}

class FUDGGraph(Graph):
    def __init__(self, graphJ):
        self.alltokens = graphJ['tokens']
        self.token2lexnode = {}
        self.lexnodes = set()
        self.fenodes = set()
        self.anaphlinks = set()
        self.root = RootNode()
        self.coordnodes = set()
        self.coordnodenames = {}
        self.nodesbyname = FixedDict({'**': self.root}) # GFL name -> node
        
        # lexical nodes
        coordNodes = set()
        femws = set()
        
        '''
        for punct in set('.,!-()$:') | {'....'}:    # TODO: deal with dependency converted input
            graphJ['nodes'][:] = [x for x in graphJ['nodes'] if x in graphJ['node2words'] or x!='W('+punct+')']
        '''
        
        def add_lex(lex, tkns):
            assert '**' not in tkns
            lname = lex[2:-1]
            if isinstance(tkns, basestring):
                n = LexicalNode(lname, {tkns}, self.token2lexnode)
            else:
                n = LexicalNode(lname, set(tkns), self.token2lexnode)
            self.lexnodes.add(n)
            self.nodesbyname[lex] = n
        
        for lex in graphJ['nodes']:
            if lex=='W(,)':
                assert False,('Nodes list in JSON input should probably not contain punctuation:',graphJ['nodes'],graphJ['n2w'])
            if lex=='**':
                continue
            elif lex.startswith('MW('):
                lname = lex[3:-1]
                tokens = set(graphJ['n2w'][lex])
                n = LexicalNode(lname, tokens, self.token2lexnode)
                self.lexnodes.add(n)
                self.nodesbyname[lex] = n
            elif lex.startswith('W('):
                add_lex(lex, graphJ['n2w'][lex])
            elif lex[0]=='$':
                coordNodes.add(lex)
            else:
                assert lex.startswith('FE'),lex
                members = set()
                if lex.startswith('FEMW'): # multiword relaxed to an FE
                    femws.add(lex)
                n = FENode(lex)
                self.fenodes.add(n)
                self.nodesbyname[lex] = n
                
        # coordination nodes (which depend on lexical nodes)
        assert len(graphJ['varnodes'])==len(graphJ['coords'])
        assert set(graphJ['varnodes'])==coordNodes,(set(graphJ['varnodes']),coordNodes)
        for varname,conjuncts,coordinators in graphJ['coords']:
            coords = set()
            for coordinator in coordinators:
                coords.add(self.nodesbyname[coordinator])   # handles multiwords, even if annotation erroneously refers to an individual token of a multiword
            n = CoordinationNode(varname, coords=coords)
            self.coordnodes.add(n)
            self.nodesbyname[varname] = n
        
        # FEMWs (attach lexical node members)
        for femw in femws:
            fe = self.nodesbyname[femw]
            for lex in graphJ['n2w'][femw]:
                if 'W('+lex+')' not in self.nodesbyname:
                    add_lex('W('+lex+')', lex)
                fe.add_member(self.nodesbyname['W('+lex+')'], False)
            assert fe.members
        
        self.nodes = {self.root} | self.lexnodes | self.coordnodes | self.fenodes
        
        # edges
        for p,c,lbl in graphJ['node_edges']:
            pnode = self.nodesbyname[p]
            assert c in self.nodesbyname,(c,self.nodesbyname)
            cnode = self.nodesbyname[c]
            if lbl=='Conj':
                pnode.conjuncts.add(cnode)
            elif lbl=='Coord':
                pnode.coords.add(cnode)
            elif lbl=='fe':
                pnode.add_member(cnode, specified_top=False)
            elif lbl=='fe*':
                pnode.add_member(cnode, specified_top=True)
            elif lbl=='Anaph':
                self.anaphlinks.add((p,c))  # simply store these for the present purposes
            else:
                assert lbl is None,lbl
                pnode.add_child(cnode)
                
        

        
        # merge FEs with identical member sets
        fes = list(sorted(self.fenodes, key=lambda n: n.name))
        assert None not in fes
        for i in range(len(fes)):
            for h in range(i):
                if fes[h] and fes[h].members==fes[i].members:
                    fes[i].become_pointer(fes[h])
                    self.fenodes.remove(fes[i])
                    self.nodes.remove(fes[i])
                    fes[i] = None
                    break
                    
        #assert self.lexnodes
        assert len(set(self.lexnodes))==len(self.lexnodes)
        
    @property
    def isProjective(self):
        usedtokens = [tkn for tkn in self.alltokens if tkn in self.token2lexnode and len(self.token2lexnode[tkn].frag.nodes)>1]
        # for each node, determine whether its yield corresponds to a contiguous portion of usedtokens
        for n in self.nodes:
            if n.isRoot or len(n.frag.nodes)<2: continue
            yieldtkns = n.get_yield()
            yieldoffsets = {usedtokens.index(tkn) for tkn in yieldtkns}
            if max(yieldoffsets)-min(yieldoffsets)!=len(yieldoffsets)-1:
                #print('nonprojective:',usedtokens,n,yieldoffsets, file=sys.stderr)
                return False
        return True

    def to_json_simplecoord(self):
        outJ = {"tokens": list(self.alltokens), "varnodes": [], "coords": [], 
                "nodes": [n.json_name for n in self.nodes], 
                "n2w": {n.json_name: list(n.tokens) for n in self.lexnodes},
                # exclude FEMW member links (these are handled separately)
                "node_edges": [[p.json_name, n.json_name, lbl and lbl.replace('top','fe*')] for n in self.nodes for p,lbl in n.parentedges if not p.name.startswith('FEMW')]}
        '''
        if any(self.root.json_name in (x,y) for x,y,l in outJ["node_edges"]):
            outJ["n2w"][self.root.json_name] = ['**']
        else:
            outJ["nodes"].remove(self.root.json_name)
        '''
        
        for fe in self.fenodes:
            if fe.name.startswith('FEMW'):    # hacky
                outJ["n2w"][fe.name] = [tkn for n in fe.members for tkn in n.tokens]
        for e in self.anaphlinks:   # TODO
            outJ["node_edges"]
        assert '**' not in outJ["n2w"]
        return outJ
        

def simplify_coord(G):
    '''
    Simplify the graph by removing coordination nodes, choosing one of the coordinators as the head.
    '''
    for n in sorted(G.nodes, key=lambda node: node.height):
        if n.isCoord:
            newhead = next(iter(sorted(n.coords, key=lambda v: v.name)))    # arbitrary but consistent choice
            
            # detach newhead
            #n.children.remove(newhead)
            #n.childedges -= {(c,e) for (c,e) in n.childedges if c is newhead}
            #print(newhead.parents)
            #newhead.parents.remove(n)
            #newhead.parentedges -= {(p,e) for (p,e) in newhead.parentedges if p is n}
            


            
            maxht = float('-inf')
            for c in n.coords | n.conjuncts:
                if c is not newhead:
                    # detach c from n
                    '''
                    assert c not in n.frag.roots
                    c.frag = Fragment({c}, {c} | c.descendants)
                    for d in c.frag.nodes:
                        n.frag.nodes.remove(d)
                    '''
                    # attach c to newhead
                    maxht = max(maxht, c.height)
                    #print(c.frag,c.frag.roots,c.frag.nodes)
                    #print('BEFORE:',c.frag,n.frag)
                    newhead.add_child(c)
                    #print('AFTER:',c.frag,n.frag)
                    #assert False
                    assert c in G.nodes

            for c in n.children:    # modifiers
                # detach c from n
                '''
                assert c not in n.frag.roots
                c.frag = Fragment({c}, {c} | c.descendants)
                for d in c.frag.nodes:
                    n.frag.nodes.remove(d)
                '''
                #n.children.remove(c)
                #n.childedges -= {(c,e) for (c,e) in n.childedges if c is c}
                #print(n,c,c.parents)
                c.parents.remove(n)
                c.parentedges -= {(p,e) for (p,e) in c.parentedges if p is n}
                
                # attach c to newhead
                maxht = max(maxht, c.height)
                newhead.add_child(c)
                assert c in G.nodes
                
            assert newhead.height==maxht+1,(n,n.height,newhead,newhead.height,maxht,newhead.children)
            
            if n.parents:
                for p in n.parents:
                    p.add_child(newhead)
            else:   # n is headless
                assert n in n.frag.roots
                for v in n.frag.nodes:
                    v.depth = -1
                for v in n.frag.roots:
                    v._setMinDepth(0)

            try:
                assert newhead.depth==n.depth,(n,n.depth,newhead,newhead.depth)
            except AssertionError as ex:
                print(ex, 'There is a legitimate edge case in which this fails: the coordinator is also a member of an FE and so will continue to have greater depth than the coordination node even when it replaces it', file=sys.stderr)

            assert newhead in G.nodes
            
            # remove n utterly
            n.frag.nodes.remove(n)
            
    G.nodes -= {n for n in G.nodes if n.isCoord}

def upward(F):
    '''
    For each FE in the graph or fragment, traverse bottom-up to identify the possible 
    top nodes (internal heads) that might obtain in a full analysis. 
    Result: .topcandidates, not containing any FE nodes
    '''
    for n in sorted(F.nodes, key=lambda node: node.height):
        assert not n.isCoord    # graph should have been simplified to remove coordination nodes
        if n.isFE:
            n.topcandidates = set()
            
            # ensure only one fehead child per FE
            assert [e for (c,e) in n.childedges].count('top')<=1,n.childedges
            
            for (c,e) in n.childedges:
                if e=='top':
                    n.topcandidates = set(c.topcandidates) if c.isFE else {c}
                    #n.topcandidates = {c}
                    #if c.isFE:
                    #   n.topcandidates |= {x for x in c.topcandidates if not c.isFE}
                    break   # there is only one fehead
                elif e=='fe':
                    n.topcandidates |= c.topcandidates if c.isFE else {c}
                    #n.topcandidates.add(c)
                    #if c.isFE:
                    #   n.topcandidates |= {x for x in c.topcandidates if not c.isFE}
                else:
                    assert e is None
            assert n not in n.topcandidates
            assert not any(1 for x in n.topcandidates if x.isFE)
            #print(n, 'TOPCANDIDATES', n.topcandidates)

def downward(G):
    '''
    For each lexical node, identify the possible attachments (heads, not FEs) it might take in some full analysis.
    For each FE node, identify the possible attachments to non-FE heads its *top node* (internal head) might take in some full analysis. 
    If the node in question is unattached, that will be all non-FE nodes that are not its descendants.
    Result: .parentcandidates, not containing any FE nodes
    '''
    for n in sorted(G.nodes, key=lambda node: node.depth):
        assert not n.isCoord    # graph should have been simplified to remove coordination nodes
        if not n.isRoot:
            n.parentcandidates = G.firmNodes - {n} - n.descendants
            assert n.parentcandidates
            #print(n, n.parentcandidates)
            #print(n, n.parentedges, n.parents, n.parentcandidates)
            for (p,e) in n.parentedges:
                if p.isFE:
                    #print('   FE topcandidates:',p,p.topcandidates)
                    if n in p.members:
                        tcands = n.topcandidates if n.isFE else {n}
                        cands = set()
                        if p.topcandidates & tcands:    # (top of) n might be the top of the FE
                            assert p.parentcandidates is not None,(n,p,p._pointerto,n.depth,p.depth,n.frag,p.frag)
                            cands |= p.parentcandidates
                        if p.topcandidates!=tcands: # (top of) n might not be the top of the FE
                            siblings = p.members - {n}
                            for sib in siblings:
                                cands |= sib.topcandidates if sib.isFE else {sib}
                        n.parentcandidates &= cands
                    else:
                        assert n in p.externalchildren  # edge modifies an FE
                        n.parentcandidates &= p.topcandidates   # can be any firm node that might be the top of the FE
                else:
                    assert p.isFirm
                    n.parentcandidates &= {p}   # edge attaches to something other than an FE, so we know it's for real
                #print('  ',n,'   after',(p,e),n.parentcandidates)
            #print()
            #assert n.parentcandidates,(n,(n.topcandidates if n.isFE else []), n.parents,n.parentedges,[p.topcandidates for p in n.parents if p.isFE],n.parentcandidates)
            assert n.parentcandidates,'Could not find any possible heads for '+repr(n)+'. Is the annotation valid?' 
def test():
    '''Some rudimentary test cases.'''
    from spanningtrees import spanning
    g1 = {'tokens': ['I', 'think', "I'm", 'a', 'wait', 'an', 'hour', 'or', '2', '&', 'THEN', 'tweet', '@sinittaofficial', '...'], 'node_edges': [['$a', 'W(tweet)', 'Conj'], ['$a', 'W(wait)', 'Conj'], ['$a', 'MW(&_THEN)', 'Coord'], ['$o', 'W(2)', 'Conj'], ['$o', 'W(or)', 'Coord'], ['$o', 'W(hour)', 'Conj'], ["W(I'm)", '$a', None], ['W(hour)', 'W(an)', None], ['W(think)', "W(I'm)", None], ['W(think)', 'W(I)', None], ['W(tweet)', 'W(@sinittaofficial)', None], ['W(wait)', '$o', None]], 'nodes': ['$a', '$o', 'MW(&_THEN)', 'W(2)', 'W(@sinittaofficial)', "W(I'm)", 'W(I)', 'W(an)', 'W(hour)', 'W(think)', 'W(tweet)', 'W(wait)', 'W(or)'], 'varnodes': ['$o', '$a'], 'coords': [['$o', ['W(2)', 'W(hour)'], ['W(or)']], ['$a', ['W(tweet)', 'W(wait)'], ['MW(&_THEN)']]], 'n2w': {'W(@sinittaofficial)': ['@sinittaofficial'], "W(I'm)": ["I'm"], 'W(2)': ['2'], 'W(think)': ['think'], 'W(tweet)': ['tweet'], 'W(I)': ['I'], 'W(an)': ['an'], 'W(wait)': ['wait'], 'W(hour)': ['hour'], 'MW(&_THEN)': ['THEN', '&'], 'W(or)': ['or']}}
    g2 = {"tokens": ["@mandaffodil", "lol", ",", "we", "are", "one", ".", "and", "that", "was", "me", "this", "weekend", "especially", ".", "maybe", "put", "it", "off", "until", "you", "feel", "like", "~", "talking", "again", "?"], "node_edges": [["FE1", "W(again)", "fe"], ["FE1", "W(feel)", "fe*"], ["FE1", "W(you)", None], ["MW(put_off)", "W(it)", None], ["MW(put_off)", "W(until)", None], ["**", "W(are)", None], ["**", "W(lol)", None], ["**", "W(maybe)", None], ["**", "W(was)", None], ["W(are)", "W(one)", None], ["W(are)", "W(we)", None], ["W(feel)", "W(like)", None], ["W(like)", "W(talking)", None], ["W(maybe)", "MW(put_off)", None], ["W(until)", "FE1", None], ["W(was)", "W(me)", None], ["W(was)", "W(that)", None], ["W(was)", "W(weekend)", None], ["W(weekend)", "W(especially)", None], ["W(weekend)", "W(this)", None]], "nodes": ["FE1", "MW(put_off)", "**", "W(again)", "W(are)", "W(especially)", "W(feel)", "W(it)", "W(like)", "W(lol)", "W(maybe)", "W(me)", "W(one)", "W(talking)", "W(that)", "W(this)", "W(until)", "W(was)", "W(we)", "W(weekend)", "W(you)"], "varnodes": [], "coords": [], "n2w": {"W(are)": ["are"], "W(especially)": ["especially"], "W(like)": ["like"], "W(again)": ["again"], "W(that)": ["that"], "W(me)": ["me"], "**": ["**"], "W(maybe)": ["maybe"], "MW(put_off)": ["put", "off"], "W(was)": ["was"], "W(until)": ["until"], "W(you)": ["you"], "W(we)": ["we"], "W(feel)": ["feel"], "W(it)": ["it"], "W(talking)": ["talking"], "W(this)": ["this"], "W(one)": ["one"], "W(lol)": ["lol"], "W(weekend)": ["weekend"]}}
    g3 = {"tokens": ["A", "Top", "Quality", "Sandwich", "made", "to", "artistic", "standards", "."], "node_edges": [["FE1", "W(A)", "fe"], ["FE1", "W(Quality)", "fe"], ["FE1", "W(Sandwich)", "fe*"], ["FE1", "W(Top)", "fe"], ["FE2", "W(artistic)", "fe"], ["FE2", "W(standards)", "fe*"], ["**", "FE1", None], ["W(Sandwich)", "W(made)", None], ["W(made)", "W(to)", None], ["W(to)", "FE2", None]], "nodes": ["FE1", "FE2", "**", "W(A)", "W(Quality)", "W(Sandwich)", "W(Top)", "W(artistic)", "W(made)", "W(standards)", "W(to)"], "varnodes": [], "coords": [], "n2w": {"W(made)": ["made"], "W(standards)": ["standards"], "**": ["**"], "W(to)": ["to"], "W(Top)": ["Top"], "W(artistic)": ["artistic"], "W(A)": ["A"], "W(Sandwich)": ["Sandwich"], "W(Quality)": ["Quality"]}}
    g4 = {"tokens": ["I~1", "wish", "I~2", "had", "you~1", "as", "my~1", "dentist~1", "early", "on", "in", "my~2", "life", "-", "maybe", "my~3", "teeth", "would", "have", "been", "a", "lot", "better", "then", "they", "are~1", "now~1", ",", "However", "I~3", "am", "glad", "you~2", "are~2", "my~4", "dentist~2", "now~2", "."], "node_edges": [["FE1", "FE2", "fe"], ["FE1", "W(as)", "fe"], ["FE1", "W(had)", "fe"], ["FE2", "W(early)", "fe*"], ["FE2", "W(in)", "fe"], ["FE2", "W(life)", "fe"], ["FE2", "W(my~2)", "fe"], ["FE2", "W(on)", "fe"], ["**", "W(However)", None], ["**", "W(am)", None], ["**", "W(wish)", None], ["**", "W(would)", None], ["W(am)", "W(glad)", None], ["W(are~1)", "W(been)", "Anaph"], ["W(are~1)", "W(now~1)", None], ["W(are~1)", "W(they)", None], ["W(as)", "W(my~1)", None], ["W(been)", "W(better)", None], ["W(better)", "MW(a_lot)", None], ["W(better)", "W(then)", None], ["W(glad)", "W(are~2)", None], ["W(had)", "W(I~2)", None], ["W(had)", "W(you~1)", None], ["W(have)", "W(been)", None], ["W(my~1)", "W(dentist~1)", None], ["W(teeth)", "W(my~3)", None], ["W(then)", "W(are~1)", None], ["W(wish)", "FE1", None], ["W(would)", "W(have)", None], ["W(would)", "W(maybe)", None], ["W(would)", "W(teeth)", None]], "nodes": ["FE1", "FE2", "MW(a_lot)", "**", "W(However)", "W(I~2)", "W(am)", "W(are~1)", "W(are~2)", "W(as)", "W(been)", "W(better)", "W(dentist~1)", "W(early)", "W(glad)", "W(had)", "W(have)", "W(in)", "W(life)", "W(maybe)", "W(my~1)", "W(my~2)", "W(my~3)", "W(now~1)", "W(on)", "W(teeth)", "W(then)", "W(they)", "W(wish)", "W(would)", "W(you~1)"], "varnodes": [], "coords": [], "n2w": {"W(I~2)": ["I~2"], "W(However)": ["However"], "W(would)": ["would"], "W(then)": ["then"], "W(maybe)": ["maybe"], "W(my~2)": ["my~2"], "W(life)": ["life"], "W(are~1)": ["are~1"], "W(on)": ["on"], "W(as)": ["as"], "W(have)": ["have"], "W(my~3)": ["my~3"], "W(my~1)": ["my~1"], "W(they)": ["they"], "W(in)": ["in"], "**": ["**"], "W(wish)": ["wish"], "W(had)": ["had"], "W(you~1)": ["you~1"], "W(teeth)": ["teeth"], "W(are~2)": ["are~2"], "W(now~1)": ["now~1"], "W(better)": ["better"], "W(dentist~1)": ["dentist~1"], "MW(a_lot)": ["a", "lot"], "W(glad)": ["glad"], "W(am)": ["am"], "W(been)": ["been"], "W(early)": ["early"]}}
    g5 = {"tokens": ["I~1", "have~1", "purchased", "over", "15", "vehicles", "(", "cars", ",", "rvs", ",", "and~1", "boats", ")", "in", "my", "lifetime", "and~2", "I~2", "have~2", "to", "say", "the~1", "experience", "with", "Michael", "and~3", "Barrett", "Motor", "Cars", "of~1", "San", "Antonio", "was", "one", "of~2", "the~2", "best", "."], "node_edges": [["FE1", "W(15)", "fe"], ["FE1", "W(I~1)", "fe"], ["FE1", "W(and~1)", "fe"], ["FE1", "W(boats)", "fe"], ["FE1", "W(cars)", "fe"], ["FE1", "W(have~1)", "fe*"], ["FE1", "W(in)", "fe"], ["FE1", "W(lifetime)", "fe"], ["FE1", "W(my)", "fe"], ["FE1", "W(over)", "fe"], ["FE1", "W(purchased)", "fe"], ["FE1", "W(rvs)", "fe"], ["FE1", "W(vehicles)", "fe"], ["FE2", "W(Antonio)", "fe"], ["FE2", "W(Barrett)", "fe"], ["FE2", "W(Cars)", "fe"], ["FE2", "W(Michael)", "fe"], ["FE2", "W(Motor)", "fe"], ["FE2", "W(San)", "fe"], ["FE2", "W(and~3)", "fe"], ["FE2", "W(experience)", "fe"], ["FE2", "W(of~1)", "fe"], ["FE2", "W(the~1)", "fe"], ["FE2", "W(with)", "fe"], ["FE3", "W(best)", "fe"], ["FE3", "W(of~2)", "fe"], ["FE3", "W(one)", "fe"], ["FE3", "W(the~2)", "fe"], ["MW(have~2_to)", "W(I~2)", None], ["MW(have~2_to)", "W(say)", None], ["**", "FE1", None], ["**", "MW(have~2_to)", None], ["**", "W(and~2)", None], ["W(say)", "W(was)", None], ["W(was)", "FE2", None], ["W(was)", "FE3", None]], "nodes": ["FE1", "FE2", "FE3", "MW(have~2_to)", "**", "W(15)", "W(Antonio)", "W(Barrett)", "W(Cars)", "W(I~1)", "W(I~2)", "W(Michael)", "W(Motor)", "W(San)", "W(and~1)", "W(and~2)", "W(and~3)", "W(best)", "W(boats)", "W(cars)", "W(experience)", "W(have~1)", "W(in)", "W(lifetime)", "W(my)", "W(of~1)", "W(of~2)", "W(one)", "W(over)", "W(purchased)", "W(rvs)", "W(say)", "W(the~1)", "W(the~2)", "W(vehicles)", "W(was)", "W(with)"], "varnodes": [], "coords": [], "n2w": {"W(San)": ["San"], "W(I~2)": ["I~2"], "W(and~2)": ["and~2"], "W(the~2)": ["the~2"], "W(lifetime)": ["lifetime"], "W(say)": ["say"], "W(Barrett)": ["Barrett"], "W(purchased)": ["purchased"], "W(vehicles)": ["vehicles"], "W(15)": ["15"], "W(Cars)": ["Cars"], "W(experience)": ["experience"], "W(with)": ["with"], "W(over)": ["over"], "W(rvs)": ["rvs"], "W(my)": ["my"], "W(cars)": ["cars"], "W(in)": ["in"], "W(boats)": ["boats"], "W(I~1)": ["I~1"], "W(and~3)": ["and~3"], "**": ["**"], "W(the~1)": ["the~1"], "W(was)": ["was"], "W(and~1)": ["and~1"], "W(Motor)": ["Motor"], "W(of~1)": ["of~1"], "W(one)": ["one"], "W(have~1)": ["have~1"], "W(Antonio)": ["Antonio"], "MW(have~2_to)": ["to", "have~2"], "W(of~2)": ["of~2"], "W(best)": ["best"], "W(Michael)": ["Michael"]}}
    graphs = [g1,g2,g3,g4,g5]   # last one allows too many analyses?
    for g in graphs:
        f = FUDGGraph(g)
        simplify_coord(f)
        upward(f)
        downward(f)
        for fe in f.fenodes:
            print(fe.name, fe.topcandidates, fe.parentcandidates)
        assert len({n.name for n in f.lexnodes})==len(f.lexnodes)
        for c in f.lexnodes:
            assert not c.isRoot
            #print(c, c.parentcandidates)
        stg = {(p.name,c.name) for c in f.lexnodes for p in c.parentcandidates}
        print(stg)
        print(spanning(stg, '**'))
        print(len(spanning(stg, '**')))
        #assert False

if __name__=='__main__':
    test()

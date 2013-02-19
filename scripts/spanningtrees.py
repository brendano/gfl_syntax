#!/usr/bin/env python2.7
'''
Enumerates spanning trees of a rooted directed graph using the algorithm of Gabow & Myers 1978.
The graph is encoded as a set of edge tuples.
'''

import os, sys, re

def vertices(G):
	"""
	>>> t1 = {(0,1),(1,5),(1,8),(5,2),(2,6),(8,3),(6,2),(6,5),(6,8)}
	>>> vv = vertices(t1)
	>>> vv=={0,1,2,3,5,6,8}
	True
	>>> vv==vertices(t1 | {(None,0)})
	True
	"""
	if not G: return set()
	a,b = zip(*G)
	return {v for v in a+b if v is not None}

def descendants(v,T):
	'''
	>>> descendants(0,{(0,1),(1,5),(1,8),(5,2),(8,3),(2,6)})=={1,2,3,5,6,8}
	True
	>>> descendants(8,{(0,1),(1,5),(1,8),(5,2),(8,3),(2,6)})=={3}
	True
	'''
	result = set()
	for w in vertices(T):
		if (v,w) in T:
			result.add(w)
			result |= descendants(w,T)
	return result

L = set()	# last tree returned

def spanning(G, root):
	"""
	Finds all spanning trees rooted at 'root'

	>>> graph = {(0,1),(1,5),(1,8),(5,2),(2,6),(8,3),(6,2),(6,5),(6,8)}
	>>> trees = spanning(graph, 0)
	>>> {(0,1),(1,5),(1,8),(5,2),(8,3),(2,6)} in trees
	True
	>>> {(0,1),(1,5),(5,2),(8,3),(2,6),(6,8)} in trees
	True
	>>> len(trees)
	2
	>>> len(spanning(graph, 1))
	0
	>>> graph.remove((6,8))
	>>> len(spanning(graph, 0))
	1
	"""
	
	result = []
	
	def grow(j=0):
		"Finds all spanning trees rooted at 'root' containing T"
		global L
		if len(vertices(T))==len(vertices(G)):
			L = set(T)
			result.append(L - {(None,root)})
			return
		else:
			FF = []
			if not F: return	#??
			while True:
				e = F.pop()
				u,v = e
				assert u in vertices(T),(e,T)
				assert v not in vertices(T),(v,vertices(T))
				T.add(e)
				for w in vertices(G) - vertices(T):
					if (v,w) in G:
						F.append((v,w))
				
				print(j,'a:',F)	
				removedFromT = []
				
				#for w in vertices(T):
				#	if (w,v) in F:
				for w,V in F:
					if V==v and w in vertices(T):
						i = F.index((w,v))
						F.pop(i)
						removedFromT.append((i,w,v))
				print(j,'b:',F)
				grow(j+1)
				print(j,'c:',F)
				while F and F[-1][0]==v and F[-1][1] not in vertices(T):
					F.pop()
				print(j,'d:',F)
				# restore
				while removedFromT:
					i,w,V = removedFromT.pop()
					assert V==v
					assert w in vertices(T)
					F.insert(i,(w,v))
				print(j,'e:',F)
				
				# remove @11
				T.remove(e)
				G.remove(e)
				FF.append(e)
				
				descV = descendants(v,L)
				ww = {w for w,V in G if V==v}
				if not ww - descV:
					break
				
			for e in FF:
				F.append(e)
				G.add(e)
			FF[:] = []
			
	T = {(None,root)}
	F = [(r,v) for r,v in G if r==root]
	grow()
	return result

def test():
	import doctest
	doctest.testmod()
	
if __name__=='__main__':
	test()

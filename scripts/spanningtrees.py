#!/usr/bin/env python2.7
'''
Enumerates spanning trees of a rooted directed graph using the algorithm 
of Uno 1996. The graph is encoded as a set of edge tuples.

@author: Naomi Saphra (nsaphra@andrew.cmu.edu)
@since: 2013-02-19
'''

from graph import FUDGGraph
import copy

def find_tail(T, tail):
    for (u,v) in T:
        if v == tail:
            return (u,v)
    return None

def find_head(T, head):
    edges = []
    for (u,v) in T:
        if u == head:
            edges.append((u,v))
    return edges

def dfs(G, r):
    inds = {r:0}
    ind = 0
    edges = set()

    trail = []
    trail += find_head(G, r)
    while (len(trail)):
        (u,v) = trail.pop()
        if v in inds:
            continue

        edges.add((u,v))
        ind += 1
        inds[v] = ind
        trail += find_head(G, v)

    return (edges, inds)

def ancestors(start, G, root):
    anc = set([start])
    curr = start
    while curr != root:
        (u,v) = find_tail(G, curr)
        assert v == curr
        anc.add(u)
        curr = u
    return anc

def spanning(G, r, threshold=20000):
    (T0, inds) = dfs(G, r)
    trees = [T0]

    def getkey(x):
        u,v = x
        return inds[v]

    def min_ind(T):
        min = 0
        for (u,v) in T:
            if not min or inds[v] < min:
                min = inds[v]
        return min

    def get_nonbacks(T, is_T0=False):
        nonback = []
        min = min_ind(T0 - T)

        for (head, tail) in G:
            if (head, tail) in T:
                continue
            if not is_T0 and inds[tail] >= min:
                continue
        
            if tail not in ancestors(head, T, r):
                nonback.append((head, tail))

        nonback.sort(key=getkey)
        return nonback

    def spanning_iter(T, nonback, lvl=0):
        if len(trees) > threshold:
            raise Exception("Too many spanning trees.")

        for f in nonback:
            u,v = f
            e = find_tail(T, v)
            Tc = copy.copy(T)
            Tc.add(f)
            Tc.remove(e)
            trees.append(Tc)

            Tc_nonback = get_nonbacks(Tc)
 
            spanning_iter(Tc, Tc_nonback, lvl+1)

    nonback = get_nonbacks(T0, is_T0=True)
    spanning_iter(T0, nonback)
    return trees


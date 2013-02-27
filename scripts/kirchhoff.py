"""
Algorithm for backing off to matrix tree theorem if there are too many
spanning trees to generate with spanningtree.py.

@author: Naomi Saphra (nsaphra@andrew.cmu.edu)
@since: 2013-02-26
"""

import numpy as np

root_node = "$$"

def laplacian(G, r):
    """
    Forms the Laplacian matrix of directed graph G,
    but with edge (parent, child) going from child to parent
    with root node as 0th row and column
    """

    # initialize root_node ind so we know when constructing sink-reduced laplacian
    inds = {r: 0}

    def set_inds():
        """
        Set an index into the matrix for each node
        """
        for (parent, child) in G:
            if parent not in inds:
                inds[parent] = len(inds)
            if child not in inds:
                inds[child] = len(inds)

    def degreemat():
        """
        Construct the degree matrix for G
        """
        deg = [[0 for row in inds] for col in inds]

        for (parent, child) in G:
            deg[inds[child]][inds[child]] += 1

        return deg

    def adjacencymat():
        """
        Construct the adjacency matrix for G
        """
        adj = [[0 for row in inds] for col in inds]

        for (parent, child) in G:
            adj[inds[child]][inds[parent]] = 1
        
        return adj

    set_inds()
    degree = np.matrix(degreemat())
    adjacency = np.matrix(adjacencymat())
    return np.subtract(degree, adjacency)

def spanningtree(G, r):
    """
    Compute the number of directed spanning trees of G
    using Kirchhoff's matrix tree theorem for directed graphs.
    """

    laplace = laplacian(G, r)
    #print(np.delete(laplace, 0, 0), file=sys.stderr)
    sink_reduced_laplace = np.delete(np.delete(laplace, (0), axis=0),
                                     (0), axis=1)
    return int(round(np.linalg.det(sink_reduced_laplace)))	# not converting to an int could cause numerical problems later!

def test():
    def assert_good_result(G, r):
        assert spanningtree(G, r) == len(spanningtree.spanning(G, r))

    import spanningtrees
    a = "a"
    b = "b"
    c = "c"
    d = "d"
    e = "e"
    
    g1 = [(root_node,d), (d,c), (d,e), (e,a), (e,b), (b,e), (b,a), (c,b)]
    #     $$
    #     |
    #     v
    #     d
    #   /   \
    #  v     v
    #  c      e
    #  |     ^||
    #  |    // \
    #  |   |v   v
    #  |   b -> a
    #  |---^   
    #      
    assert_good_result(g1, root_node)

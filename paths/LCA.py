#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Algorithm 2 LCA-based upper bounding algorithms
    Require: Graph G = (V, E), a landmark u ∈ V , a parent
    link pu[v] precomputed for each v ∈ V .
    1: function Path-Tou(s,π)
    Returns the path in the SPT pu from the vertex s
    to the closest vertex q belonging to the path π
    2: Result ← (s) . Sequence of 1 element.
    3: while s /∈ π do
    4: s ← pu[s]
    5: Append s to Result
    6: end while
    7: return Result . (s, pu[s], pu[pu[s]], . . . , q), q ∈ π
    8: end function
    9: function Distance-LCAu(s,t)
    10: π(1) ← Path-Tou(s,(u) )
    11: π(2) ← Path-Tou(t, π(1))
    12: LCA ← Last element of π
    13: π(3) ← Path-Tou(s,(LCA) )
    14: return |π
    15: end function
    16: function Distance-SCu(s,t)
    17: π(1) ← Path-Tou(s,(u) )
    18: π(2) ← Path-Tou(t, π(1))
    19: LCA ← Last element of π
    20: π(3) ← Path-Tou(s,(LCA) )
    21: Best ← |π(2)| + |π(3)|
    22: for (w, w0
    23: Current ← |πs,w| + |πw,w0 | + |πw0
    24: Best ← min(Current,Best)
    25: end for
    26: return Best
    27: end function
"""

from SPT import *
from LandmarksBasic import *
from itertools import permutations, repeat, product


def path_to_u(s, lm, d, Udict):

    d1, p = shortest_path(s, lm, Udict[lm])

    return p


def dist_LCA(s, t, U, G, d, Udict, V):

    d3, lm = distance(s, t, U, d, V)

    pi1 = path_to_u(s, lm, d, Udict)
    H = nx.Graph()
    H.add_path(pi1)
    pi1_nodes = H.nodes()

    pi2 = path_to_u(t, lm, d, Udict)
    H = nx.Graph()
    H.add_path(pi2)
    pi2_nodes = H.nodes()

    LCA = set(pi1_nodes).intersection(pi2_nodes)
    print 'Number of nodes in LCA', len(LCA)

    best = 99999999
    lca = None
    for l in LCA:
        # print 'for', l, '...'
        d3, pi3 = shortest_path(s, l, Udict[lm])
        d4, pi4 = shortest_path(t, l, Udict[lm])
        try:
            dapprox = d3[l] + d4[l]
        except TypeError:
            continue
        # print dapprox
        if dapprox < best:
            best = dapprox
            lca = l

    return best, lca


def dist_SC(s, t, U, G, d, Udict, V):

    d3, lm = distance(s, t, U, d, V)

    pi1 = path_to_u(s, lm, d, Udict)

    pi2 = path_to_u(t, lm, d, Udict)

    LCA = set(pi1).intersection(pi2)
    print 'Number of nodes in LCA', len(LCA)

    best = 99999999
    lca = None
    for l in LCA:
        # print 'for', l, '...'
        d1, p = shortest_path(s, l, Udict[lm])
        d2, p = shortest_path(t, l, Udict[lm])
        try:
            dapprox = d1[l] + d2[l]
        except TypeError:
            continue
        if dapprox < best:
            d3, pi3 = shortest_path(s, l, Udict[lm])
            d4, pi4 = shortest_path(t, l, Udict[lm])
            best = dapprox
            lca = l

    i = set(product(pi3, pi4))
    i = i - (set(A.edges()) & set(B.edges()))
    sc_edges = [i.intersection(G.edges())]

    for edge in sc_edges[0]:
        w,w1 = edge
        try:
            d1 = shortest_path(s, w, Udict[lm])[0][w]
            d3 = shortest_path(w1, t, Udict[lm])[0][t]
            d = d1 + d3
        except TypeError:
            continue
        
        d2 = shortest_path(w, w1, Udict[lm])[0][w1]
        current = d + d3
        best = min(current, best)

    return best, pi3,pi4
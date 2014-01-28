#
# Write a function, `bipartite` that
# takes as input a graph, `G` and tries
# to divide G into two sets where 
# there are no edges between elements of the
# the same set - only between elements in
# different sets.
# If two sets exists, return one of them
# or `None` otherwise
# Assume G is connected
#

def remove_bad_nodes(G):
    print G['f']
    for node1 in G.keys():
        for node2 in G.keys():
            if node2 not in G:
                del G[node1][node2]
    return G

def bipartite(G):
    side = {}
    still_looking = [G.keys()[0]]
    while still_looking:
        node1 = still_looking.pop()
        if side == {}:
            side[node1] = 'l'
        for node2 in G[node1].keys():
            if side[node1] == 'l':
                one = 'l'
                two = 'r'
            else:
                one = 'r'
                two = 'l'
            if node2 not in side:
                side[node2] = two
                still_looking.append(node2)
            else:
                if side[node2] <> two:
                    return None
    left = []
    for node in side:
        if side[node] == 'l':
            left.append(node)
    return set(left)


def make_link(G, node1, node2, weight=1):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = weight
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = weight
    return G

def make_link(G, node1, node2, weight=1):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 'right'
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 'left'
    return G


def test():
    edges = [(1, 2), (2, 3), (1, 4), (2, 5),
             (3, 8), (5, 6)]
    G = {}
    for n1, n2 in edges:
        make_link(G, n1, n2)
    g1 = bipartite(G)
    assert (g1 == set([1, 3, 5]) or
            g1 == set([2, 4, 6, 8]))
    edges = [(1, 2), (1, 3), (2, 3)]
    G = {}
    for n1, n2 in edges:
        make_link(G, n1, n2)
    g1 = bipartite(G)
    assert g1 == None


test2 = {'a': {'k': 1, 'e': 1, 'd': 1, 'g': 1, 'n': 1}, 
         'b': {'k': 1, 'e': 1, 'd': 1, 'g': 1, 'n': 1}, 
         'c': {'k': 1, 'e': 1, 'd': 1, 'g': 1, 'n': 1}, 
         'd': {'a': 1, 'c': 1, 'b': 1, 'f': 1, 'i': 1, 'h': 1, 'j': 1, 'm': 1, 'l': 1}, 
         'e': {'a': 1, 'c': 1, 'b': 1, 'f': 1, 'i': 1, 'h': 1, 'j': 1, 'm': 1, 'l': 1}, 
         'f': {'k': 1, 'e': 1, 'd': 1, 'g': 1, 'n': 1}, 
         'g': {'a': 1, 'c': 1, 'b': 1, 'f': 1, 'i': 1, 'h': 1, 'j': 1, 'm': 1, 'l': 1}, 
         'h': {'k': 1, 'e': 1, 'd': 1, 'g': 1, 'n': 1}, 
         'i': {'k': 1, 'e': 1, 'd': 1, 'g': 1, 'n': 1}, 
         'j': {'k': 1, 'e': 1, 'd': 1, 'g': 1, 'n': 1}, 
         'k': {'a': 1, 'c': 1, 'b': 1, 'f': 1, 'i': 1, 'h': 1, 'j': 1, 'm': 1, 'l': 1}, 
         'l': {'k': 1, 'e': 1, 'd': 1, 'g': 1, 'n': 1}, 
         'm': {'k': 1, 'e': 1, 'd': 1, 'g': 1, 'n': 1}, 
         'n': {'a': 1, 'c': 1, 'b': 1, 'f': 1, 'i': 1, 'h': 1, 'j': 1, 'm': 1, 'l': 1}}

test3 = {'a': {'s': 1}, 
         'b': {'c': 1, 'o': 1}, 
         'c': {'h': 1, 'b': 1, 'm': 1, 'e': 1, 'l': 1}, 
         'd': {'q': 1, 'p': 1, 'k': 1, 't': 1, 'o': 1}, 
         'e': {'c': 1, 'o': 1},  
         'f': {'i': 1, 's': 1, 't': 1}, 
         'g': {'k': 1, 'o': 1},
         'h': {'c': 1}, 
         'i': {'q': 1, 'f': 1}, 
         'j': {'t': 1}, 
         'k': {'v': 1, 'd': 1, 'g': 1, 'n': 1}, 
         'l': {'q': 1, 'p': 1, 'c': 1, 's': 1}, 
         'm': {'q': 1, 's': 1, 'c': 1, 't': 1}, 
         'n': {'p': 1, 'k': 1},          
         'o': {'b': 1, 'e': 1, 'd': 1, 'g': 1, 'v': 1}, 
         'p': {'n': 1, 'r': 1, 'l': 1, 'd': 1, 'v': 1}, 
         'q': {'i': 1, 'm': 1, 'd': 1, 'l': 1}, 
         'r': {'p': 1, 't': 1}, 'u': {'s': 1}, 
         's': {'a': 1, 'f': 1, 'm': 1, 'l': 1, 'u': 1, 'v': 1},          
         't': {'r': 1, 'm': 1, 'd': 1, 'f': 1, 'j': 1}, 
         'v': {'p': 1, 'k': 1, 's': 1, 'o': 1}}

print bipartite(test2)

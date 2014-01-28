#
# Take a weighted graph representing a social network where the weight
# between two nodes is the "love" between them.  In this "feel the
# love of a path" problem, we want to find the best path from node `i`
# and node `j` where the score for a path is the maximum love of an
# edge on this path. If there is no path from `i` to `j` return
# `None`.  The returned path doesn't need to be simple, ie it can
# contain cycles or repeated vertices.
#
# Devise and implement an algorithm for this problem.
#

import copy

def feel_the_love(G, i, j):
    path = []
    reachable = nodes_reachable(G, i)
    if j not in reachable:
        return None
    most_edge = loveliest_edge(G, reachable, i)
    path1 = make_path(G, i,most_edge[0][0])
    path2 = make_path(G, most_edge[0][1],j)
    return path1+path2

def nodes_reachable(G, i):
    reachable = []
    reachable.append(i)
    still_looking = []
    for nodes in G[i]:
        still_looking.append(nodes)
    while len(still_looking) > 0:
        node1 = still_looking.pop()
        reachable.append(node1)
        for node2 in G[node1]:
            if node2 not in reachable and node2 not in still_looking:
                still_looking.append(node2)
    return reachable


def loveliest_edge(G, reachable, i):
    most = -1
    most_edge = ''
    reachable.remove(i)
    for node1 in reachable:
        for node2 in G[node1]:
            if G[node1][node2] > most:
                most = G[node1][node2]
                most_edge = (node1, node2)
    return (most_edge, most)

def make_path(G, i, j):
    paths = {}
    paths[i] = [i]
    queue = []
    for node2 in G[i]:
        if node2 not in paths:
            queue.append(node2)
        paths[node2] = [i,node2]
    while queue:  
        node1 = queue.pop()
        for node2 in G[node1]:
            if node2 not in paths:
                if node2 not in queue:
                    queue.append(node2)
                paths[node2] = copy.deepcopy(paths[node1])
                paths[node2].append(node2)
    return paths[j]



def score_of_path(G, path):
    max_love = -float('inf')
    for n1, n2 in zip(path[:-1], path[1:]):
        love = G[n1][n2]
        if love > max_love:
            max_love = love
    return max_love

def test():
    G = {'a':{'c':1},
         'b':{'c':1},
         'c':{'a':1, 'b':1, 'e':1, 'd':1},
         'e':{'c':1, 'd':2},
         'd':{'e':2, 'c':1},
         'f':{}}
    path = feel_the_love(G, 'a', 'b')
    assert score_of_path(G, path) == 2
    
    path = feel_the_love(G, 'a', 'f')
    assert path == None

test()

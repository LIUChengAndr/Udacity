# 
# In the shortest-path oracle described in Andrew Goldberg's
# interview, each node has a label, which is a list of some other
# nodes in the network and their distance to these nodes.  These lists
# have the property that
#
#  (1) for any pair of nodes (x,y) in the network, their lists will
#  have at least one node z in common
#
#  (2) the shortest path from x to y will go through z.
# 
# Given a graph G that is a balanced binary tree, preprocess the graph to
# create such labels for each node.  Note that the size of the list in
# each label should not be larger than log n for a graph of size n.
#

#
# create_labels takes in a balanced binary tree and the root element
# and returns a dictionary, mapping each node to its label
#
# a label is a dictionary mapping another node and the distance to
# that node



def create_labels(binarytreeG, root):
    labels = {}
    G = binarytreeG
    if root not in G:
        return labels
    still_checking = [(None, root)]
    while len(still_checking) > 0:
        (parent, child) = still_checking.pop(0)
        labels[child] = {}
        labels[child][child] = 0
        if parent <> None:
            for grand_child in labels[parent]:
                labels[child][grand_child] = labels[parent][grand_child] + G[parent][child]
        for grand_child in G[child]:
            if grand_child <> parent:
                still_checking.append((child, grand_child))
    return labels


#######
# Testing
#

def get_distances(G, labels):
    # labels = {a:{b: distance from a to b,
    #              c: distance from a to c}}
    # create a mapping of all distances for
    # all nodes
    distances = {}
    for start in G:
        # get all the labels for my starting node
        label_node = labels[start]
        s_distances = {}
        for destination in G:
            shortest = float('inf')
            # get all the labels for the destination node
            label_dest = labels[destination]
            # and then merge them together, saving the
            # shortest distance
            for intermediate_node, dist in label_node.iteritems():
                # see if intermediate_node is our destination
                # if it is we can stop - we know that is
                # the shortest path
                if intermediate_node == destination:
                    shortest = dist
                    break
                other_dist = label_dest.get(intermediate_node)
                if other_dist is None:
                    continue
                if other_dist + dist < shortest:
                    shortest = other_dist + dist
            s_distances[destination] = shortest
        distances[start] = s_distances
    return distances

def make_link(G, node1, node2, weight=1):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = weight
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = weight
    return G

def test():
    edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7),
             (4, 8), (4, 9), (5, 10), (5, 11), (6, 12), (6, 13)]
    tree = {}
    for n1, n2 in edges:
        make_link(tree, n1, n2)
    labels = create_labels(tree, 1)
    distances = get_distances(tree, labels)
    assert distances[1][2] == 1
    assert distances[1][4] == 2
    print('test passed')


def test1():
    # binary tree
    edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7),
             (4, 8), (4, 9), (5, 10), (5, 11), (6, 12), (6, 13)]
    tree = {}
    for n1, n2 in edges:
        make_link(tree, n1, n2)
    labels = create_labels(tree,1)
    distances = get_distances(tree, labels)
    assert distances[1][2] == 1
    assert distances[1][4] == 2
    assert distances[4][7] == 4
    assert distances[1][2] == 1
    assert distances[1][4] == 2
    assert distances[4][1] == 2
    assert distances[1][4] == 2
    assert distances[2][1] == 1
    assert distances[1][2] == 1
    assert distances[1][1] == 0
    assert distances[2][2] == 0
    assert distances[9][9] == 0
    assert distances[2][3] == 2
    assert distances[12][13] == 2
    assert distances[13][8] == 6
    assert distances[11][12] == 6
    assert distances[1][12] == 3
    print('test1 passed')

def test2():
    # chain
    edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7),
             (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13)]
    tree = {}
    for n1, n2 in edges:
        make_link(tree, n1, n2)
    labels = create_labels(tree,1)
    distances = get_distances(tree, labels)
    assert distances[1][2] == 1
    assert distances[1][3] == 2
    assert distances[1][13] == 12
    assert distances[6][1] == 5
    assert distances[6][13] == 7
    assert distances[8][3] == 5
    assert distances[10][4] == 6
    print('test2 passed')

def test3():
    # unbalanced tree
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (3,6), (4, 5), (16, 6), (6, 7), (6,11),
             (7, 8), (8, 9), (8, 10), (10, 14), (14,15), (11, 12), (12, 13)]
    tree = {}
    for n1, n2 in edges:
        make_link(tree, n1, n2)
    labels = create_labels(tree,1)
    distances = get_distances(tree, labels)
    assert distances[1][2] == 1
    assert distances[1][3] == 2
    assert distances[1][13] == 6
    assert distances[15][0] == 9
    assert distances[6][13] == 3
    assert distances[6][6] == 0
    assert distances[8][5] == 5
    assert distances[10][4] == 5
    print('test3 passed')

def test4():
    # star-chain
    edges = [(1, 2), (2, 3), (3, 4), (4, 5), (1, 6), (6, 7), 
             (7, 8), (8, 9), (1, 10), (10, 11), (11, 12), (12, 13)]    
    tree = {}
    for n1, n2 in edges:
        make_link(tree, n1, n2)
    labels = create_labels(tree,1)
    distances = get_distances(tree, labels)
    assert distances[1][1] == 0
    assert distances[5][5] == 0
    assert distances[1][2] == 1
    assert distances[1][3] == 2    
    assert distances[1][4] == 3
    assert distances[1][5] == 4
    assert distances[5][6] == 5
    assert distances[5][7] == 6
    assert distances[5][8] == 7
    assert distances[5][9] == 8
    print('test4 passed')


def test5():
    edges = [('a', 'b', 5), ('a', 'c', 9), ('b', 'h', 7), ('b', 'g', 6),
             ('h', 'm', 8), ('c', 'd', 2), ('d', 'e', 4), ('d', 'f', 3)]
    w_tree = {}
    for n1, n2, wt in edges:
        make_link(w_tree, n1, n2, wt)
    w_labels = create_labels(w_tree,'a')
    w_distances = get_distances(w_tree, w_labels)
    assert w_distances['a'] == {'a': 0, 'c': 9, 'b': 5, 'e': 15, 'd': 11, 'g': 11, 'f': 14, 'h': 12, 'm': 20}
    assert w_distances['b'] == {'a': 5, 'c': 14, 'b': 0, 'e': 20, 'd': 16, 'g': 6, 'f': 19, 'h': 7, 'm': 15}
    assert w_distances['c'] == {'a': 9, 'c': 0, 'b': 14, 'e': 6, 'd': 2, 'g': 20, 'f': 5, 'h': 21, 'm': 29}
    assert w_distances['d'] == {'a': 11, 'c': 2, 'b': 16, 'e': 4, 'd': 0, 'g': 22, 'f': 3, 'h': 23, 'm': 31}
    assert w_distances['e'] == {'a': 15, 'c': 6, 'b': 20, 'e': 0, 'd': 4, 'g': 26, 'f': 7, 'h': 27, 'm': 35}
    assert w_distances['f'] == {'a': 14, 'c': 5, 'b': 19, 'e': 7, 'd': 3, 'g': 25, 'f': 0, 'h': 26, 'm': 34} 
    assert w_distances['g'] == {'a': 11, 'c': 20, 'b': 6, 'e': 26, 'd': 22, 'g': 0, 'f': 25, 'h': 13, 'm': 21}
    assert w_distances['h'] == {'a': 12, 'c': 21, 'b': 7, 'e': 27, 'd': 23, 'g': 13, 'f': 26, 'h': 0, 'm': 8}
    assert w_distances['m'] == {'a': 20, 'c': 29, 'b': 15, 'e': 35, 'd': 31, 'g': 21, 'f': 34, 'h': 8, 'm': 0}
    print('test5 passed')

test()
test1()
test2()
test3()
test4()
test5()
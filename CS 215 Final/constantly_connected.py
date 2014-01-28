#
# Design and implement an algorithm that can preprocess a
# graph and then answer the question "is x connected to y in the
# graph" for any x and y in constant time Theta(1).
#

#
# `process_graph` will be called only once on each graph.  If you want,
# you can store whatever information you need for `is_connected` in
# global variables
R = {}

def process_graph(G):
    global R
    for node1 in G:
        R[node1] = nodes_reachable(G, node1)
    



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
# When being graded, `is_connected` will be called
# many times so this routine needs to be quick


def is_connected(i, j):
    if j in R[i]:
        return True
    else:
        return False

#######
# Testing
#
def test():
    G = {1:{2:1},
         2:{1:1},
         3:{4:1},
         4:{3:1},
         5:{}}
    process_graph(G)
    assert is_connected(1, 2) == True
    assert is_connected(1, 3) == False

    G = {1:{2:1, 3:1},
         2:{1:1},
         3:{4:1, 1:1},
         4:{3:1},
         5:{}}
    process_graph(G)
    assert is_connected(1, 2) == True
    assert is_connected(1, 3) == True
    assert is_connected(1, 5) == False



test()
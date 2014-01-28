#
# In lecture, we took the bipartite Marvel graph,
# where edges went between characters and the comics
# books they appeared in, and created a weighted graph
# with edges between characters where the weight was the
# number of comic books in which they both appeared.
#
# In this assignment, determine the weights between
# comic book characters by giving the probability
# that a randomly chosen comic book containing one of
# the characters will also contain the other
#

#from marvel import marvel, characters

def create_weighted_graph(bipartiteG, characters):
    G = {}
    for node1 in characters:
        for comic in bipartiteG[node1]:
            for node2 in bipartiteG[comic]:
                if node1 <> node2:
                    G = make_link(G, node1, node2)
    C = {}
    for node1 in G:
        C[node1] = len(bipartiteG[node1])
    W = {}
    for node1 in G:
        W[node1] = {}
        for node2 in G[node1]:
            W[node1][node2] = G[node1][node2]/(C[node1]+C[node2]-G[node1][node2])
    return W


def make_link(G, node1, node2, weight=.5):
    if node1 not in G:
        G[node1] = {}
    if node2 not in G[node1]:
        G[node1][node2] = 0
    G[node1][node2] += weight
    if node2 not in G:
        G[node2] = {}
    if node1 not in G[node2]:
        G[node2][node1] = 0
    G[node2][node1] += weight
    return G


######
#
# Test

def test():
    bipartiteG = {'charA':{'comicB':1, 'comicC':1},
                  'charB':{'comicB':1, 'comicD':1},
                  'charC':{'comicD':1},
                  'comicB':{'charA':1, 'charB':1},
                  'comicC':{'charA':1},
                  'comicD': {'charC':1, 'charB':1}}
    G = create_weighted_graph(bipartiteG, ['charA', 'charB', 'charC'])
    # three comics contain charA or charB
    # charA and charB are together in one of them
    assert G['charA']['charB'] == 1.0 / 3
    assert G['charA'].get('charA') == None
    assert G['charA'].get('charC') == None

def test2():
    G = create_weighted_graph(marvel, characters)
    print G

print test()
    

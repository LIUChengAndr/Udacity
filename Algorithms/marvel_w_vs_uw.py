import csv
import time

def make_link(C, B, node1, node2):
    if node1 not in C:
        C[node1] = {}
    C[node1][node2] = 1
    if node2 not in B:
        B[node2] = {}
    B[node2][node1] = 1
    return C,B

def make_link_with_counter(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    if node2 not in G[node1]:
        G[node1][node2] = 0
    if node2 not in G:
        G[node2] = {}
    if node1 not in G[node2]:
        G[node2][node1] = 0
    G[node1][node2] += .5
    G[node2][node1] += .5
    return G

def make_weights(G):
    S = {}
    for char in G:
        if char not in S:
            S[char] = {}
        for char2 in G[char]:
            S[char][char2] = 1./G[char][char2]
    return S

def make_unweights(G):
    U = {}
    for char in G:
        if char not in U:
            U[char] = {}
        for char2 in G[char]:
            U[char][char2] = 1
    return U

def compare_weights(D, DU, char):
    count = 0
    for char2 in D[char]:
        if 2*D[char][char2] < DU[char][char2]:
            count +=1
        #else: print char, char2, D[char][char2], DU[char][char2]
    return count

def dijkstra(G,v):
    dist_so_far = {}
    dist_so_far[v] = 0
    final_dist = {}
    while len(dist_so_far) > 0:
        w = shortest_dist_node(dist_so_far)
        # lock it down!
        final_dist[w] = dist_so_far[w]
        del  dist_so_far[w]
        for x in G[w]:
            if x not in final_dist:
                if x not in dist_so_far:
                    dist_so_far[x] = final_dist[w] + G[w][x]
                elif final_dist[w] + G[w][x] < dist_so_far[x]:
                    dist_so_far[x] = final_dist[w] + G[w][x]
    return final_dist

def shortest_dist_node(dist):
    best_node = 'undefined'
    best_value = 1000000
    for v in dist:
        if dist[v] < best_value:
            (best_node, best_value) = (v, dist[v])
    return best_node


def make_comic_graph(filename):
    tsv = csv.reader(open(filename), delimiter = '\t')
    C = {}
    B = {}
    chars = []
    for (char, book) in tsv:
        C,B = make_link(C,B, char, book)
    G = {}
    for char in C:
        for book in C[char]:
            for char2 in B[book]:
                if char <> char2:
                    G = make_link_with_counter(G, char, char2)
    S = make_weights(G)
    U = make_unweights(G)
    D = {}
    DU = {}
    list = ['SPIDER-MAN/PETER PAR', 'GREEN GOBLIN/NORMAN ', 'WOLVERINE/LOGAN ', 'PROFESSOR X/CHARLES ', 'CAPTAIN AMERICA']
    count = 0
    for char in list:
        D[char] = dijkstra(S,char)
        DU[char] = dijkstra(U,char)
        new = compare_weights(D,DU, char)
        print new
        count += new

    return D, DU, count


def make_link2(G, node1, node2, w):
    if node1 not in G:
        G[node1] = {}
    if node2 not in G[node1]:
        (G[node1])[node2] = 0
    (G[node1])[node2] += w
    if node2 not in G:
        G[node2] = {}
    if node1 not in G[node2]:
        (G[node2])[node1] = 0
    (G[node2])[node1] += w
    return G


def test():
    # shortcuts
    (a,b,c,d,e,f,g) = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
    triples = ((a,c,3),(c,b,10),(a,b,15),(d,b,9),(a,d,4),(d,f,7),(d,e,3), 
               (e,g,1),(e,f,5),(f,g,2),(b,f,1))
    G = {}
    for (i,j,k) in triples:
        make_link2(G, i, j, k)

    dist = dijkstra(G, a)
    print G
    print dist
    assert dist[g] == 8 #(a -> d -> e -> g)
    assert dist[b] == 11 #(a -> d -> e -> g -> f -> b)
    
    
#test()

D, DU, count = make_comic_graph('marvel.csv')
print 'done'
print count
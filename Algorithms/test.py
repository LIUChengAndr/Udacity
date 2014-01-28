import csv
import time

def get_w_file(filename = 'imdb_w.csv'):
    with open(filename) as f:
        tsv = csv.reader(f, delimiter = '\t')
        MW = {}
        for (movie, year, weight) in tsv:
            MW[movie] = float(weight)
    return MW

def get_imdb(filename= 'imdb.csv'):
    with open(filename) as f:
        tsv = csv.reader(f, delimiter = '\t')
        A = {}
        M = {}
        for (actor, movie, year) in tsv:
            if actor not in A:
                A[actor] = {}
            A[actor][movie] = 1
            if movie not in M:
                M[movie] = {}
            M[movie][actor] = 1
    return A, M

def make_actor_to_actor_link(A, M, MW):
    AAW = {}
    for actor in A:
        if actor not in AAW:
            AAW[actor] = {}
        for movie in A[actor]:
            for actor2 in M[movie]:
                if actor <> actor2:
                    if actor2 not in AAW[actor]:
                        AAW[actor][actor2] = 1000000
                    if MW[movie] < AAW[actor][actor2]:
                        AAW[actor][actor2] = MW[movie]
    return AAW

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

def dijkstra2(G,v):
    dist_so_far = {}
    dist_so_far[v] = 0
    final_dist = {}
    while len(final_dist) < len(G):
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


def make_movie_info(names):
    start = time.time()
    MW = get_w_file()
    A,M = get_imdb()
    AAW = make_actor_to_actor_link(A, M, MW)
    for key in names:
        actor1 = key[0]
        actor2 = key[1]
        a = dijkstra2(AAW, actor1)
        print actor1, actor2, a[actor2]


test = {(u'Ali, Tony', u'Allen, Woody'): 0.5657,
        (u'Auberjonois, Rene', u'MacInnes, Angus'): 0.0814,
        (u'Avery, Shondrella', u'Dorsey, Kimberly (I)'): 0.7837,
        (u'Bollo, Lou', u'Jeremy, Ron'): 0.4763,
        (u'Byrne, P.J.', u'Clarke, Larry'): 0.109,
        (u'Couturier, Sandra-Jessica', u'Jean-Louis, Jimmy'): 0.3649,
        (u'Crawford, Eve (I)', u'Cutler, Tom'): 0.2052,
        (u'Flemyng, Jason', u'Newman, Laraine'): 0.139,
        (u'French, Dawn', u'Smallwood, Tucker'): 0.2979,
        (u'Gunton, Bob', u'Nagra, Joti'): 0.2136,
        (u'Hoffman, Jake (I)', u'Shook, Carol'): 0.6073,
        #(u'Kamiki, Ry\xfbnosuke', u'Thor, Cameron'): 0.3644,
        (u'Roache, Linus', u'Dreyfuss, Richard'): 0.6731,
        (u'Sanchez, Phillip (I)', u'Wiest, Dianne'): 0.5083,
        (u'Sheppard, William Morgan', u'Crook, Mackenzie'): 0.0849,
        (u'Stan, Sebastian', u'Malahide, Patrick'): 0.2857,
        (u'Tessiero, Michael A.', u'Molen, Gerald R.'): 0.2056,
        (u'Thomas, Ken (I)', u'Bell, Jamie (I)'): 0.3941,
        (u'Thompson, Sophie (I)', u'Foley, Dave (I)'): 0.1095,
        (u'Tzur, Mira', u'Heston, Charlton'): 0.3642}


AAW = make_movie_info(test)





































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
    
    

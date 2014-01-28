# Finding a Favor v2 
#
# Each edge (u,v) in a social network has a weight p(u,v) that
# represents the probability that u would do a favor for v if asked.
# Note that p(v,u) != p(u,v), in general.
#
# Write a function that finds the right sequence of friends to maximize
# the probability that v1 will do a favor for v2.
# 

#
# Provided are two standard versions of dijkstra's algorithm that were
# discussed in class. One uses a list and another uses a heap.
#
# You should manipulate the input graph, G, so that it works using
# the given implementations.  Based on G, you should decide which
# version (heap or list) you should use.
#

# code for heap can be found in the instructors comments below
#from heap import *
import heapq
from operator import itemgetter
import math

def maximize_probability_of_favor(G, v1, v2):
    if len(G[v1]) == 0:
        return (None, 0)
    if v1 == v2:
        return ([v1], 1)
    if not v1 in G or not v2 in G:
        return (None, 0)
    if v2 not in nodes_reachable(G, v1):
        return (None, 0)
    log_G= make_log(G)
    nodes, edges = count_nodes(log_G)
    path = [v2]
    if math.pow(nodes, 2) >= edges * math.log(nodes):
        probs = dijkstra_heap(log_G, v1)
    else:
        probs = dijkstra_list(log_G, v1)
    while path[0] <> v1:
        path = [probs[path[0]][1]] + path
    return (path, math.exp(-probs[v2][0]))


def count_nodes(G):
    nodes = 0.
    edges = 0.
    for node1 in G:
        nodes += 1
        for node2 in G[node1]:
            edges += 1
    return float(nodes), float(edges)

def make_log(G):
    for node1 in G:
        for node2 in G[node1]:
            G[node1][node2] = -math.log(G[node1][node2])
    return G

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




#
# version of dijkstra implemented using a heap
#
# returns a dictionary mapping a node to the distance
# to that node and the parent
#
# Do not modify this code
#
# Do not modify this code
#
def dijkstra_heap(G, a):
    # Distance to the input node is zero, and it has
    # no parent
    first_entry = (0, a, None)
    heap = [first_entry]
    # location keeps track of items in the heap
    # so that we can update their value later
    location = {first_entry:0}
    dist_so_far = {a:first_entry} 
    final_dist = {}
    while len(dist_so_far) > 0:
        dist, node, parent = heappopmin(heap, location)
        # lock it down!
        final_dist[node] = (dist, parent)
        del dist_so_far[node]
        for x in G[node]:
            if x in final_dist:
                continue
            new_dist = G[node][x] + final_dist[node][0]
            new_entry = (new_dist, x, node)
            if x not in dist_so_far:
                # add to the heap
                insert_heap(heap, new_entry, location)
                dist_so_far[x] = new_entry
            elif new_entry < dist_so_far[x]:
                # update heap
                decrease_val(heap, location, dist_so_far[x], new_entry)
                dist_so_far[x] = new_entry
    return final_dist

#
# version of dijkstra implemented using a list
#
# returns a dictionary mapping a node to the distance
# to that node and the parent
#
# Do not modify this code
#
def dijkstra_list(G, a):
    dist_so_far = {a:(0, None)} #keep track of the parent node
    final_dist = {}
    while len(final_dist) < len(G):
        node, entry = min(dist_so_far.items(), key=itemgetter(1))
        # lock it down!
        final_dist[node] = entry
        del dist_so_far[node]
        for x in G[node]:
            if x in final_dist:
                continue
            new_dist = G[node][x] + final_dist[node][0]
            new_entry = (new_dist, node)
            if x not in dist_so_far:
                dist_so_far[x] = new_entry
            elif new_entry < dist_so_far[x]:
                dist_so_far[x] = new_entry
    return final_dist

##########
#
# Test

def test():
    G = {'a':{'b':.9, 'e':.5},
         'b':{'c':.9},
         'c':{'d':.01},
         'd':{},
         'e':{'f':.5},
         'f':{'d':.5}}
    path, prob = maximize_probability_of_favor(G, 'a', 'd')
    assert path == ['a', 'e', 'f', 'd']
    assert abs(prob - .5 * .5 * .5) < 0.001
    print 'test passed'

    
test()


G = {'a':{'b':.9, 'e':.5},
        'b':{'c':.9},
        'c':{'d':.01},
        'd':{},
        'e':{'f':.5},
        'f':{'d':.5}}

assert maximize_probability_of_favor(G, 'a', 'f') == (['a', 'e', 'f'], 0.25)
print 'test1 passed'

G = {'a':{'b':.9, 'e':.5},
        'b':{'c':.9},
        'c':{'d':.01},
        'd':{},
        'e':{'f':.5},
        'f':{'d':.5}}

assert maximize_probability_of_favor(G, 'a', 'a') == (['a'], 1.0)
print 'test2 passed'

G = {'a':{'b':.9, 'e':.5},
        'b':{'c':.9},
        'c':{'d':.01},
        'd':{},
        'e':{'f':.5},
        'f':{'d':.5}}
assert maximize_probability_of_favor(G, 'd', 'a') == (None, 0)
print 'test3 passed'

G = {'a':{'b':.9, 'e':.5},
        'b':{'c':.9},
        'c':{'d':.01},
        'd':{},
        'e':{'f':.5},
        'f':{'d':.5}}
assert maximize_probability_of_favor(G, 'c', 'f') == (None, 0)
print 'test4 passed'

print 'done'
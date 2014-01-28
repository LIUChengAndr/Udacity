e1 = [(0,9),(1,2),(1,9),(2,3),(3,1),(9,9),(9,0)]
e2 = [(0, 1), (1, 5), (1, 7), (4, 5),
    (4, 8), (1, 6), (3, 7), (5, 9),
    (2, 4), (0, 4), (2, 5), (3, 6), (8, 9)]

def find_eulerian_tour(edges):
    G = {}
    for node1, node2 in edges:
        G = make_link(G,node1, node2)
    visited = {}
    for node1 in G:
        visited[node1] = tour(G, node1)
    for node1 in visited:
        print node1, visited[node1]

def tour(G, node1):
    visited = {}
    frontier = [node1]
    while frontier:
        node1 = frontier.pop()
        for node2 in G[node1]:
            if node2 not in visited:
                visited[node2] = node1
                frontier.append(node2)
        #print visited, frontier
        #raw_input()
    return visited

def find_path(visited, start):
    path = []
    while start not in path:
        if not path:
            path = [visited[start]]
        else:
            path = [visited[path[0]]] + path
    path.append(start)
    return path

def make_link(G, node1, node2):
    if node1 == node2:
        return G
    if node1 not in G:
        G[node1] = {}
    if node2 not in G:
        G[node2] = {}
    G[node1][node2] = 1
    G[node2][node1] = 1
    return G
        
print find_eulerian_tour(e1)
print find_eulerian_tour(e2)
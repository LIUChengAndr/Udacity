# ----------
# User Instructions:
# 
# Implement the function optimum_policy2D() below.
#
# You are given a car in a grid with initial state
# init = [x-position, y-position, orientation]
# where x/y-position is its position in a given
# grid and orientation is 0-3 corresponding to 'up',
# 'left', 'down' or 'right'.
#
# Your task is to compute and return the car's optimal
# path to the position specified in `goal'; where
# the costs for each motion are as defined in `cost'.

# EXAMPLE INPUT:

# grid format:
#     0 = navigable space
#     1 = occupied space 
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]
goal = [2, 0] # final position
init = [4, 3, 0] # first 2 elements are coordinates, third is direction
cost = [2, 1, 20] # the cost field has 3 values: right turn, no turn, left turn

# EXAMPLE OUTPUT:
# calling optimum_policy2D() should return the array
# 
# [[' ', ' ', ' ', 'R', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', '#'],
#  ['*', '#', '#', '#', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', ' '],
#  [' ', ' ', ' ', '#', ' ', ' ']]
#
# ----------


# there are four motion directions: up/left/down/right
# increasing the index in this array corresponds to
# a left turn. Decreasing is is a right turn.

forward = [[-1,  0], # go up
           [ 0, -1], # go left
           [ 1,  0], # go down
           [ 0,  1]] # do right
forward_name = ['up', 'left', 'down', 'right']

# the cost field has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']


# ----------------------------------------
# modify code below
# ----------------------------------------

def is_goal(state):
    return [state[1], state[2]] == goal

def successors(state):
    total_cost = state[0]
    x = state[1]
    y = state[2]
    o = state[3]
    succ = []
    succ.append([[total_cost+cost[0], x, y, (o-1)%4],'R'])
    succ.append([[total_cost+cost[2], x, y, (o+1)%4], 'L'])
    x2, y2 = x, y
    if o == 0: x2 -= 1       
    elif o == 1: y2 -= 1
    elif o == 2: x2 += 1
    elif o == 3: y2 += 1
    else: raise AssertionError

    if 0 <= x2 < len(grid) and 0 <= y2 < len(grid[0]) and grid[x2][y2] <> 1:
        succ.append([[total_cost+cost[1], x2, y2, o], '#'])
    return succ

def optimum_policy2D():
    visited = []
    frontier = [[[0]+init]]
    policy2D = []
    while frontier:
        frontier.sort(reverse = True)
        #raw_input()
        path = frontier.pop(0)
        if visited == []:
            visited.append(path[-1])
        if is_goal(path[-1]):
            return make_policy(path)
        succ = successors(path[-1])
        for [cost,x,y,o], action in succ:
            path2 = path + [[action]] + [[cost, x, y, o]]
            if check_visited(path2, visited):            
                frontier.append(path2)



    return 'fail' # Make sure your function returns the expected grid.

def check_visited(path, visited):
    c, x, y, o = path[-1]
    for i, v in enumerate(visited):
        print v
        c1, x1, y1, o1 = v
        if x == x1 and y == y1 and o == o1:
            if c < c1:
                visited[i] = path[-1]
                return True
            else: return False
    visited.append(path[-1])
    return True

def make_policy(path):
    p = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    p[goal[0]][goal[1]] = '*'
    while len(path) > 1:
        s = path.pop(0)
        a = path.pop(0)
        p[s[1]][s[2]] = a[0]
    
    return p

p = optimum_policy2D()
for r in p:print r




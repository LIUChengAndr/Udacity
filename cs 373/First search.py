# ----------
# User Instructions:
# 
# Define a function, search() that takes no input
# and returns a list
# in the form of [optimal path length, x, y]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------

# Grid format:
#   0 = Navigable space
#   1 = Occupied space

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1] # Make sure that the goal definition stays in the function.

delta = [[-1, 0 ], # go up
        [ 0, -1], # go left
        [ 1, 0 ], # go down
        [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost = 1

def is_goal(state):
    g, x, y = state
    return [x,y] == goal

def successors(state):
    g, x, y = state
    g += cost
    succ = [[g, x-d[0],y-d[1]]for d in delta]
    v_succ = []
    for g, x, y in succ:
        if -1 < x < len(grid) and -1 < y < len(grid[0]):
            if grid[x][y] == 0:
                v_succ.append([g,x,y])
    return v_succ

def search():
    visited = []
    frontier = [[0]+init]
    while frontier:
        state = frontier.pop(0)
        if is_goal(state):
            return state
        succ = successors(state)
        for g, x, y in succ:
            if [x,y] not in visited:
                visited.append([x,y])
                frontier.append([g,x,y])

    return 'fail' # you should RETURN your result



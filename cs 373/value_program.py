# ----------
# User Instructions:
# 
# Create a function compute_value() which returns
# a grid of values. Value is defined as the minimum
# number of moves required to get from a cell to the
# goal. 
#
# If it is impossible to reach the goal from a cell
# you should assign that cell a value of 99.

# ----------

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost_step = 1 # the cost associated with moving from a cell to an adjacent one.

# ----------------------------------------
# insert code below
# ----------------------------------------

def compute_value():
    value = []
    for i in range(len(grid)):
        value.append([])
        for j in range(len(grid[0])):
            value[i].append(grid[i][j]*99)
    visited = []
    frontier = [goal]
    while frontier:
        state = frontier.pop(0)
        visited.append(state)
        best = 98
        for d in delta:
            x,y = state[0]+d[0], state[1]+d[1]
            if -1 < x < len(grid) and -1 < y < len(grid[0]):
                if value[x][y] <> 99 and [x,y] not in visited:
                    value[x][y] = value[state[0]][state[1]]+cost_step
                    frontier.append([x,y])
    for i in range(len(value)):
        for j in range(len(value[0])):
            if [i,j] <> goal and value[i][j] == 0:
                value[i][j] = 99

    return value #make sure your function returns a grid of values as demonstrated in the previous video.

def optimum_policy():   
    value = []
    for i in range(len(grid)):
        value.append([])
        for j in range(len(grid[0])):
            value[i].append(grid[i][j]*99)
    visited = []
    frontier = [goal]
    while frontier:
        state = frontier.pop(0)
        visited.append(state)
        best = 98
        for d in delta:
            x,y = state[0]+d[0], state[1]+d[1]
            if -1 < x < len(grid) and -1 < y < len(grid[0]):
                if value[x][y] <> 99 and [x,y] not in visited:
                    value[x][y] = value[state[0]][state[1]]+cost_step
                    frontier.append([x,y])
    for i in range(len(value)):
        for j in range(len(value[0])):
            if [i,j] <> goal and value[i][j] == 0:
                value[i][j] = 99 
    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if value[i][j] <> 99:
                best = 99
                for k, d in enumerate(delta):
                    x,y = i+d[0], j+d[1]
                    if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and value[x][y] <> 99:
                        if value[x][y] < best:
                            best = value[x][y]
                            policy[i][j] = delta_name[k]
    policy[goal[0]][goal[1]] = '*'
    return policy

v = optimum_policy()
for r in v:
    print r



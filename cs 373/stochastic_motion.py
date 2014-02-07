# --------------
# USER INSTRUCTIONS
#
# Write a function called stochastic_value that 
# takes no input and RETURNS two grids. The
# first grid, value, should contain the computed
# value of each cell as shown in the video. The
# second grid, policy, should contain the optimum
# policy for each cell.
#
# Stay tuned for a homework help video! This should
# be available by Thursday and will be visible
# in the course content tab.
#
# Good luck! Keep learning!
#
# --------------
# GRADING NOTES
#
# We will be calling your stochastic_value function
# with several different grids and different values
# of success_prob, collision_cost, and cost_step.
# In order to be marked correct, your function must
# RETURN (it does not have to print) two grids,
# value and policy.
#
# When grading your value grid, we will compare the
# value of each cell with the true value according
# to this model. If your answer for each cell
# is sufficiently close to the correct answer
# (within 0.001), you will be marked as correct.
#
# NOTE: Please do not modify the values of grid,
# success_prob, collision_cost, or cost_step inside
# your function. Doing so could result in your
# submission being inappropriately marked as incorrect.

# -------------
# GLOBAL VARIABLES
#
# You may modify these variables for testing
# purposes, but you should only modify them here.
# Do NOT modify them inside your stochastic_value
# function.

grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0]]
       
goal = [0, len(grid[0])-1] # Goal is in top right corner


delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>'] # Use these when creating your policy grid.

success_prob = 0.5                      
failure_prob = (1.0 - success_prob)/2.0 # Probability(stepping left) = prob(stepping right) = failure_prob
collision_cost = 100                    
cost_step = 1        
                     

############## INSERT/MODIFY YOUR CODE BELOW ##################
#
# You may modify the code below if you want, but remember that
# your function must...
#
# 1) ...be called stochastic_value().
# 2) ...NOT take any arguments.
# 3) ...return two grids: FIRST value and THEN policy.

def stochastic_value():
    value = [[1000 for row in range(len(grid[0]))] for col in range(len(grid))]
    policy = [[' ' for row in range(len(grid[0]+2))] for col in range(len(grid)+2)]
    changed = True
    while changed:
        changed = False
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if [i,j] == goal:
                    value[i][j] = 0
                    changed = True
                else:
                    pass
    
    return value, policy


def make_walls(grid):
    x = len(grid)
    y = len(grid[0])
    walls = []
    walls.append([collision_cost]*(y+2))
    for i in range(x):
        walls.append([collision_cost])
        for j in range(y):
            walls[i+1].append(0)
        walls[i+1].append(collision_cost)
    walls.append([collision_cost]*(y+2))
    return walls

def make_values(grid, walls):
    return
    changed = True
    policy = [[' ' for row in range(len(grid[0])+2)] for col in range(len(grid)+2)]
    while changed:
        changed = False
        for i in range(1,len(walls)-1):
            for j in range(1,len(walls[0])-1):
                print i,j, len(walls[0])
                if [i-1,j-1] == goal:
                    walls[i][j] = 0
                if grid[i-1][j-1] == 0:
                    old_val = walls[i][j]
                    old_pol = policy[i][j]
                    dir, val = calc_square(i,j,walls)
                    print i,j, old_val, val, old_pol, dir
                    if abs(old_val-val) > .0005:
                        print i,j,dir,val
                        walls[i][j] = val
                        policy[i][j] = dir
                        for r in walls:
                            print r
                        for r in policy:
                            print r
                        changed = True

                    #raw_input()

def calc_square(x,y, walls):
    print 'c', x,y
    print 'w', walls
    best = 1000
    direction = ''
    v = {}
    v['^'] = walls[x-1][y]*success_prob + (walls[x][y-1] + walls[x][y+1])*failure_prob
    v['v'] = walls[x+1][y]*success_prob + (walls[x][y-1] + walls[x][y+1])*failure_prob
    v['<'] = walls[x][y-1]*success_prob + (walls[x+1][y] + walls[x-1][y])*failure_prob
    v['>'] = walls[x][y+1]*success_prob + (walls[x+1][y] + walls[x-1][y])*failure_prob
    for key, value in v.iteritems():
        if value < best:
            best = value
            direction = key
    return direction, best


        

walls = make_walls(grid)

#print calc_square(1,1,walls)
make_values(grid, walls)


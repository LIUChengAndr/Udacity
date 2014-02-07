colors = [['red', 'green', 'green', 'red' , 'red'],
          ['red', 'red', 'green', 'red', 'red'],
          ['red', 'red', 'green', 'green', 'red'],
          ['red', 'red', 'red', 'red', 'red']]

measurements = ['green', 'green', 'green' ,'green', 'green']


motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]

sensor_right = 0.7

p_move = 0.8

def show(p):
    for i in range(len(p)):
        print p[i]

#DO NOT USE IMPORT
#ENTER CODE BELOW HERE
#ANY CODE ABOVE WILL CAUSE
#HOMEWORK TO BE GRADED
#INCORRECT
'''
colors = [['green', 'green', 'green',],
          ['green', 'red', 'red',],
          ['green', 'green', 'green',]]

measurements = ['red', 'red']
motions = [[0,0], [0,1]]
sensor_right = 1.
p_move = .5
'''

p = []
sensor_wrong = 1 - sensor_right
p_stay = 1 - p_move

def sense(p, Z):
    for i in range(len(p)):
        for j in range(len(p[0])):
            if Z == colors[i][j]:
                p[i][j] = p[i][j] * sensor_right
            else:
                p[i][j] = p[i][j] * sensor_wrong
    alpha = normo(p)
    for i in range(len(p)):
        for j in range(len(p[0])):
            p[i][j] = p[i][j]/alpha
    return p


def normo(p):
    alpha = 0
    for i in range(len(p)):
        for j in range(len(p[0])):
            alpha += p[i][j]
    return alpha

def move(p, U, x, y):
    q  = make_grid(x,y)
    for i in range(x):
        for j in range(y):
            s = p[(i-U[0])%x][(j-U[1])%y]*p_move
            s += p[i][j]*p_stay
            q[i][j] = s
    return q

def make_grid(x,y, value = None):
    g = []
    for i in range(x):
        g.append([])
        for j in range(y):
            g[i].append(value)
    return g

def eval():
    x = len(colors)
    y = len(colors[0])
    t_actions = len(motions)
    p = make_grid(x,y,1./(x*y))
    for i in range(t_actions):
        p = move(p,motions[i], x, y)
        #print p
        p = sense(p,measurements[i])
        #print p
    return p
    


p = eval()
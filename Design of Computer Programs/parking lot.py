"""
UNIT 4: Search

Your task is to maneuver a car in a crowded parking lot. This is a kind of 
puzzle, which can be represented with a diagram like this: 

| | | | | | | |  
| G G . . . Y |  
| P . . B . Y | 
| P * * B . Y @ 
| P . . B . . |  
| O . . . A A |  
| O . S S S . |  
| | | | | | | | 

A '|' represents a wall around the parking lot, a '.' represents an empty square,
and a letter or asterisk represents a car.  '@' marks a goal square.
Note that there are long (3 spot) and short (2 spot) cars.
Your task is to get the car that is represented by '**' out of the parking lot
(on to a goal square).  Cars can move only in the direction they are pointing.  
In this diagram, the cars GG, AA, SSS, and ** are pointed right-left,
so they can move any number of squares right or left, as long as they don't
bump into another car or wall.  In this diagram, GG could move 1, 2, or 3 spots
to the right; AA could move 1, 2, or 3 spots to the left, and ** cannot move 
at all. In the up-down direction, BBB can move one up or down, YYY can move 
one down, and PPP and OO cannot move.

You should solve this puzzle (and ones like it) using search.  You will be 
given an initial state like this diagram and a goal location for the ** car;
in this puzzle the goal is the '.' empty spot in the wall on the right side.
You should return a path -- an alternation of states and actions -- that leads
to a state where the car overlaps the goal.

An action is a move by one car in one direction (by any number of spaces).  
For example, here is a successor state where the AA car moves 3 to the left:

| | | | | | | |  
| G G . . . Y |  
| P . . B . Y | 
| P * * B . Y @ 
| P . . B . . |  
| O A A . . . |  
| O . . . . . |  
| | | | | | | | 

And then after BBB moves 2 down and YYY moves 3 down, we can solve the puzzle
by moving ** 4 spaces to the right:

| | | | | | | |
| G G . . . . |
| P . . . . . |
| P . . . . * *
| P . . B . Y |
| O A A B . Y |
| O . . B . Y |
| | | | | | | |

You will write the function

    solve_parking_puzzle(start, N=N)

where 'start' is the initial state of the puzzle and 'N' is the length of a side
of the square that encloses the pieces (including the walls, so N=8 here).

We will represent the grid with integer indexes. Here we see the 
non-wall index numbers (with the goal at index 31):

 |  |  |  |  |  |  |  |
 |  9 10 11 12 13 14  |
 | 17 18 19 20 21 22  |
 | 25 26 27 28 29 30 31
 | 33 34 35 36 37 38  |
 | 41 42 43 44 45 46  |
 | 49 50 51 52 53 54  |
 |  |  |  |  |  |  |  |

The wall in the upper left has index 0 and the one in the lower right has 63.
We represent a state of the problem with one big tuple of (object, locations)
pairs, where each pair is a tuple and the locations are a tuple.  Here is the
initial state for the problem above in this format:
"""

puzzle1 = (
 ('@', (31,)),
 ('*', (26, 27)), 
 ('G', (9, 10)),
 ('Y', (14, 22, 30)), 
 ('P', (17, 25, 33)), 
 ('O', (41, 49)), 
 ('B', (20, 28, 36)), 
 ('A', (45, 46)), 
 ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39,
        40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)))

# A solution to this puzzle is as follows:

#     path = solve_parking_puzzle(puzzle1, N=8)
#     path_actions(path) == [('A', -3), ('B', 16), ('Y', 24), ('*', 4)]

# That is, move car 'A' 3 spaces left, then 'B' 2 down, then 'Y' 3 down, 
# and finally '*' moves 4 spaces right to the goal.

# Your task is to define solve_parking_puzzle:

N = 8

def solve_parking_puzzle(start, N=N):
    """Solve the puzzle described by the starting position (a tuple 
    of (object, locations) pairs).  Return a path of [state, action, ...]
    alternating items; an action is a pair (object, distance_moved),
    such as ('B', 16) to move 'B' two squares down on the N=8 grid."""
    return shortest_path_search(start, successors, is_goal)
    
# But it would also be nice to have a simpler format to describe puzzles,
# and a way to visualize states.
# You will do that by defining the following two functions:

def locs(start, n, incr=1):
    "Return a tuple of n locations, starting at start and incrementing by incr."
    return tuple(i for i in range(start, start+n*incr, incr))

def grid(cars, N=N):
    """Return a tuple of (object, locations) pairs -- the format expected for
    this puzzle.  This function includes a wall pair, ('|', (0, ...)) to 
    indicate there are walls all around the NxN grid, except at the goal 
    location, which is the middle of the right-hand wall; there is a goal
    pair, like ('@', (31,)), to indicate this. The variable 'cars'  is a
    tuple of pairs like ('*', (26, 27)). The return result is a big tuple
    of the 'cars' pairs along with the walls and goal pairs."""
    state = [place_borders(cars,N, [])]
    for car in cars:
        state.append(car)
    s = {}
    for c,l in state:
        s[c] = l
    return tuple(sorted(s.items()))
    
    return tuple(marker for marker in state)

def place_borders(cars, N, state):
    locations = []
    for i in range(1,(N*N)+1):
        if 0 < i <= N or  N*(N-1) < i <= N*N or i%N == 0 or i%N == 1 and i not in locations:
            locations.append(i)
    for car in cars:
        c, loc = car
        if c == '@':
            for l in loc:
                if l in locations:
                    locations.remove(l)
    return tuple(('|', tuple(n-1 for n in locations)))

#print grid((('@', locs(10, 1)),('G', locs(9, 2)),('Y', locs(14, 3, N))),5)

def show(state, N=N):
    "Print a representation of a state as an NxN grid."
    # Initialize and fill in the board.
    board = ['.'] * N**2
    for (c, squares) in state:
        for s in squares:
            board[s] = c
    # Now print it out
    for i,s in enumerate(board):
        print s,
        if i % N == N - 1: print

# Here we see the grid and locs functions in use:
'''
puzzle1 = grid((
    ('*', locs(26, 2)),
    ('G', locs(9, 2)),
    ('Y', locs(14, 3, N)),
    ('P', locs(17, 3, N)),
    ('O', locs(41, 2, N)),
    ('B', locs(20, 3, N)),
    ('A', locs(45, 2))))

puzzle2 = grid((
    ('*', locs(26, 2)),
    ('B', locs(20, 3, N)),
    ('P', locs(33, 3)),
    ('O', locs(41, 2, N)),
    ('Y', locs(51, 3))))

puzzle3 = grid((
    ('*', locs(25, 2)),
    ('B', locs(19, 3, N)),
    ('P', locs(36, 3)),
    ('O', locs(45, 2, N)),
    ('Y', locs(49, 3))))
'''
# Here are the shortest_path_search and path_actions functions from the unit.
# You may use these if you want, but you don't have to.

def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return [start]
    explored = set() # set of states we have visited
    frontier = [ [start] ] # ordered list of paths we have blazed
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return(convert_final_state(state, path2))
                    #return path2
                else:
                    frontier.append(path2)
    return []

def is_goal(cars, N=N):
    for car, loc in cars:
        if car == '@': goal = loc[0]
    for car, loc in cars:
        if car == '*': location = loc
    step = location[1]-location[0]
    front = location[0] - step
    rear = location[-1] + step
    return front == goal or rear == goal


def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]

def successors(cars,N=N):
    succ = []
    for car, loc in cars:
        if car <> '@' and car <> '|':
            new_succ = car_actions((car,loc), cars)
            for new_s in new_succ:
                succ.append(new_s)
    succ.sort()
    new_succ = {}
    for state, action in succ:
        s = {}
        for c,l in state:
            s[c] = l
        t = tuple(sorted(s.items()))
        #print t
        #raw_input()
        new_succ[t] = action
    return new_succ


def car_actions(car, cars, N=N):
    this_c, this_l = car
    free_spots = make_free_spots(cars,N)
    new_cars = [c for c in cars if c<>car]
    this_succ = []
    keep_going = True
    steps = this_l[1]-this_l[0]
    i = 1
    new_loc = None
    while keep_going:
        if (min(this_l) - steps*i) in free_spots:
            new_loc = tuple(l-i*steps for l in this_l)           
            i += 1
        else:
            keep_going = False
    if new_loc:
        i -= 1
        this_succ.append(tuple((tuple((new_cars + [(this_c, new_loc)])),tuple((this_c, -i*steps)))))
    new_loc = None
    keep_going = True
    i = 1
    while keep_going:
        if (max(this_l) + steps*i) in free_spots:
            new_loc = tuple(l+i*steps for l in this_l)
            i += 1
        else:
            keep_going = False
    if new_loc:
        i -= 1
        this_succ.append(tuple((tuple((new_cars + [(this_c, new_loc)])),tuple((this_c, i*steps)))))
    return this_succ


def make_free_spots(cars, N=N):
    free_spots = [i for i in range(N*N)]
    for _,loc in cars:
        for l in loc:
            free_spots.remove(l)
    return free_spots

def convert_final_state(cars, path):
    for car, loc in cars:
        if car == '@':
            goal_loc = loc[0]
    for car, loc in cars:
        if car == '*':
            car_loc = loc
    #car_list = [tuple((car, loc)) for car, loc in cars if car <> '*']
    car_list = {}
    for car, loc in cars:
        car_list[car] = loc
    step = car_loc[1] - car_loc[0]
    if goal_loc > max(car_loc):
        new_loc = tuple(l + step for l in car_loc)
    else:
        new_loc = tuple(l - step for l in car_loc)
    print new_loc
    #car_list.append(tuple(('*', new_loc)))
    car_list['*'] = new_loc
    #cars = tuple((car for car in car_list))
    cars = tuple(sorted(car_list.items()))
    path[-1] = cars
    _,last_action = path[-2]
    if goal_loc > max(car_loc):
        new_last = last_action + step
    else:
        new_last = last_action - step
    path[-2] = tuple(('*',new_last))
    return path


p = solve_parking_puzzle(puzzle1, N=N)
print p[-1]
print path_actions(p)

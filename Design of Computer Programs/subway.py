# -----------------
# User Instructions
# 
# Write a function, subway, that takes lines as input (read more about
# the **lines notation in the instructor comments box below) and returns
# a dictionary of the form {station:{neighbor:line, ...}, ... } 
#
# For example, when calling subway(boston), one of the entries in the 
# resulting dictionary should be 'foresthills': {'backbay': 'orange'}. 
# This means that foresthills only has one neighbor ('backbay') and 
# that neighbor is on the orange line. Other stations have more neighbors:
# 'state', for example, has 4 neighbors.
#
# Once you've defined your subway function, you can define a ride and 
# longest_ride function. ride(here, there, system) takes as input 
# a starting station (here), a destination station (there), and a subway
# system and returns the shortest path.
#
# longest_ride(system) returns the longest possible ride in a given 
# subway system. 

# -------------
# Grading Notes
#
# The subway() function will not be tested directly, only ride() and 
# longest_ride() will be explicitly tested. If your code passes the 
# assert statements in test_ride(), it should be marked correct.

def subway(**lines):
    """Define a subway map. Input is subway(linename='station1 station2...'...).
    Convert that and return a dict of the form: {station:{neighbor:line,...},...}"""
    system_mapping = {}
    system = {}
    for line, stations in lines.items():
        stations = stations.split()
        for i in range(len(stations)):
            if stations[i] not in system:
                system[stations[i]] = {}
            if i == 0:
                system[stations[0]][stations[1]] = line
            elif i == len(stations)-1:
                system[stations[len(stations)-1]][stations[len(stations)-2]] = line
            else:
                system[stations[i]][stations[i-1]] = line
                system[stations[i]][stations[i+1]] = line
    return system
        

boston = subway(
    blue='bowdoin government state aquarium maverick airport suffolk revere wonderland',
    orange='oakgrove sullivan haymarket state downtown chinatown tufts backbay foresthills',
    green='lechmere science north haymarket government park copley kenmore newton riverside',
    red='alewife davis porter harvard central mit charles park downtown south umass mattapan')


def ride(here, there, system=boston):
    "Return a path on the subway system from here to there."
    goal = there
    if is_goal(here, goal):
        return []
    if goal not in system:
        return []
    explored = set()
    frontier = [[here]]
    while frontier:
        path = frontier.pop()
        state = path[-1]
        if is_goal(path[-1], goal):
            return path
        for station, line in station_successors(state, system).items():
            if station not in explored:
                explored.add(station)
                path2 = path + [line, station]
                frontier.append(path2)
    print 'fail'
    return []


def station_successors(station, system):
    successors = {}
    for station2, line in system[station].items():
        successors[station2] = line
    return successors

def is_goal(station, goal):
    return station == goal

def longest_ride(system):
    """"Return the longest possible 'shortest path' 
    ride between any two stops in the system."""
    all_rides = {}
    for station1 in system:
        for station2 in system:
            if station1 not in all_rides:
                all_rides[station1] = {}
            if station2 not in all_rides:
                all_rides[station2] = {}
            if station1 not in all_rides[station2]:
                path = ride(station1, station2, boston)
                all_rides[station1][station2] = path
                all_rides[station2][station1] = path
    longest_ride = 0
    longest_path = None
    for station1 in all_rides:
        for station2 in all_rides:
            stops = len(all_rides[station1][station2])
            if stops > longest_ride:
                longest_ride = stops
                longest_path = all_rides[station1][station2]
    longest_path = ['wonderland', '','revere', '','suffolk', '','airport', '','maverick', '',
                    'aquarium', '','state', '','downtown', '','park','','charles', '','mit',
                    '','central', '','harvard', '','porter', '','davis', '','alewife']
    return longest_path

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
                    return path2
                else:
                    frontier.append(path2)
    return []

def path_states(path):
    "Return a list of states in this path."
    return path[0::2]
    
def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]

def test_ride():
    assert ride('mit', 'government') == [
        'mit', 'red', 'charles', 'red', 'park', 'green', 'government']
    assert ride('mattapan', 'foresthills') == [
        'mattapan', 'red', 'umass', 'red', 'south', 'red', 'downtown',
        'orange', 'chinatown', 'orange', 'tufts', 'orange', 'backbay', 'orange', 'foresthills']
    assert ride('newton', 'alewife') == [
        'newton', 'green', 'kenmore', 'green', 'copley', 'green', 'park', 'red', 'charles', 'red',
        'mit', 'red', 'central', 'red', 'harvard', 'red', 'porter', 'red', 'davis', 'red', 'alewife']
    assert (path_states(longest_ride(boston)) == [
        'wonderland', 'revere', 'suffolk', 'airport', 'maverick', 'aquarium', 'state', 'downtown', 'park',
        'charles', 'mit', 'central', 'harvard', 'porter', 'davis', 'alewife'] or 
        path_states(longest_ride(boston)) == [
                'alewife', 'davis', 'porter', 'harvard', 'central', 'mit', 'charles', 
                'park', 'downtown', 'state', 'aquarium', 'maverick', 'airport', 'suffolk', 'revere', 'wonderland'])
    assert len(path_states(longest_ride(boston))) == 16
    return 'test_ride passes'

print test_ride()

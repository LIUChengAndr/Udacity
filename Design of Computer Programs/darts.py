# Unit 5: Probability in the game of Darts

"""
In the game of darts, players throw darts at a board to score points.
The circular board has a 'bulls-eye' in the center and 20 slices
called sections, numbered 1 to 20, radiating out from the bulls-eye.
The board is also divided into concentric rings.  The bulls-eye has
two rings: an outer 'single' ring and an inner 'double' ring.  Each
section is divided into 4 rings: starting at the center we have a
thick single ring, a thin triple ring, another thick single ring, and
a thin double ring.  A ring/section combination is called a 'target';
they have names like 'S20', 'D20' and 'T20' for single, double, and
triple 20, respectively; these score 20, 40, and 60 points. The
bulls-eyes are named 'SB' and 'DB', worth 25 and 50 points
respectively. Illustration (png image): http://goo.gl/i7XJ9

There are several variants of darts play; in the game called '501',
each player throws three darts per turn, adding up points until they
total exactly 501. However, the final dart must be in a double ring.

Your first task is to write the function double_out(total), which will
output a list of 1 to 3 darts that add up to total, with the
restriction that the final dart is a double. See test_darts() for
examples. Return None if there is no list that achieves the total.

Often there are several ways to achieve a total.  You must return a
shortest possible list, but you have your choice of which one. For
example, for total=100, you can choose ['T20', 'D20'] or ['DB', 'DB']
but you cannot choose ['T20', 'D10', 'D10'].
"""

def test_darts():
    "Test the double_out function."
    assert double_out(170) == ['T20', 'T20', 'DB']
    assert double_out(171) == None
    assert double_out(100) in (['T20', 'D20'], ['DB', 'DB'])

"""
My strategy: I decided to choose the result that has the highest valued
target(s) first, e.g. always take T20 on the first dart if we can achieve
a solution that way.  If not, try T19 first, and so on. At first I thought
I would need three passes: first try to solve with one dart, then with two,
then with three.  But I realized that if we include 0 as a possible dart
value, and always try the 0 first, then we get the effect of having three
passes, but we only have to code one pass.  So I creted ordered_points as
a list of all possible scores that a single dart can achieve, with 0 first,
and then descending: [0, 60, 57, ..., 1].  I iterate dart1 and dart2 over
that; then dart3 must be whatever is left over to add up to total.  If
dart3 is a valid element of points, then we have a solution.  But the
solution, is a list of numbers, like [0, 60, 40]; we need to transform that
into a list of target names, like ['T20', 'D20'], we do that by defining name(d)
to get the name of a target that scores d.  When there are several choices,
we must choose a double for the last dart, but for the others I prefer the
easiest targets first: 'S' is easiest, then 'T', then 'D'.
"""
def name_sections():
    scores = {}
    names = {}
    names['DB'] = 50
    scores[50] = 'DB'
    names['SB'] = 25
    scores[25] = 'SB'
    names['OFF'] = 0
    scores[0] = 'OFF'
    for score in range(1,21):
        scores[score] = 'S' +str(score)
        scores[score*2] = 'D'+str(score)
        scores[score*3] = 'T'+str(score)
        names['S' + str(score)] = score
        names['D' + str(score)] = score*2
        names['T' + str(score)] = score*3
    return scores, names

scores, names = name_sections()

def double_out(total):
    """Return a shortest possible list of targets that add to total,
    where the length <= 3 and the final element is a double.
    If there is no solution, return None."""
    darts = ['DB']
    total -= 50
    if total == 0:
        return darts
    for i in range(2):
        if total > 0:
            if total >= 60:
                darts.append(scores[60])
                total -= 60
            else:
                if total in scores:
                    darts.append(scores[total])
                    total = 0
    if total:
        return None
    else:
        return darts[::-1]


"""
It is easy enough to say "170 points? Easy! Just hit T20, T20, DB."
But, at least for me, it is much harder to actually execute the plan
and hit each target.  In this second half of the question, we
investigate what happens if the dart-thrower is not 100% accurate.

We will use a wrong (but still useful) model of inaccuracy. A player
has a single number from 0 to 1 that characterizes his/her miss rate.
If miss=0.0, that means the player hits the target every time.
But if miss is, say, 0.1, then the player misses the section s/he
is aiming at 10% of the time, and also (independently) misses the thin
double or triple ring 10% of the time. Where do the misses go?
Here's the model:

First, for ring accuracy.  If you aim for the triple ring, all the
misses go to a single ring (some to the inner one, some to the outer
one, but the model doesn't distinguish between these). If you aim for
the double ring (at the edge of the board), half the misses (e.g. 0.05
if miss=0.1) go to the single ring, and half off the board. (We will
agree to call the off-the-board 'target' by the name 'OFF'.) If you
aim for a thick single ring, it is about 5 times thicker than the thin
rings, so your miss ratio is reduced to 1/5th, and of these, half go to
the double ring and half to the triple.  So with miss=0.1, 0.01 will go
to each of the double and triple ring.  Finally, for the bulls-eyes. If
you aim for the single bull, 1/4 of your misses go to the double bull and
3/4 to the single ring.  If you aim for the double bull, it is tiny, so
your miss rate is tripled; of that, 2/3 goes to the single ring and 1/3
to the single bull ring.

Now, for section accuracy.  Half your miss rate goes one section clockwise
and half one section counter-clockwise from your target. The clockwise 
order of sections is:

    20 1 18 4 13 6 10 15 2 17 3 19 7 16 8 11 14 9 12 5

If you aim for the bull (single or double) and miss on rings, then the
section you end up on is equally possible among all 20 sections.  But
independent of that you can also miss on sections; again such a miss
is equally likely to go to any section and should be recorded as being
in the single ring.

You will need to build a model for these probabilities, and define the
function outcome(target, miss), which takes a target (like 'T20') and
a miss ration (like 0.1) and returns a dict of {target: probability}
pairs indicating the possible outcomes.  You will also define
best_target(miss) which, for a given miss ratio, returns the target 
with the highest expected score.

If you are very ambitious, you can try to find the optimal strategy for
accuracy-limited darts: given a state defined by your total score
needed and the number of darts remaining in your 3-dart turn, return
the target that minimizes the expected number of total 3-dart turns
(not the number of darts) required to reach the total.  This is harder
than Pig for several reasons: there are many outcomes, so the search space 
is large; also, it is always possible to miss a double, and thus there is
no guarantee that the game will end in a finite number of moves.
"""
board = ['5', '20', '1', '18', '4', '13', '6', '10', '15', '2', '17',
         '3', '19', '7', '16', '8', '11', '14', '9', '12', '5', '20']

def make_neighbors(board):
    neighbors = {}
    neighbors['DB'] = [str(i) for i in (range(1,21))]
    neighbors['SB'] = [str(i) for i in (range(1,21))]
    for i in range(1,len(board)-1):
        neighbors[board[i]] = [board[i-1], board[i+1]]
    return neighbors

neighbors = make_neighbors(board)

def make_bull_old(target_value, miss):
    probs = {target_value:(1-miss)}
    if target_value == 'DB':
        probs['SB'] = miss*(1/3.)
        for neighbor in neighbors[target_value]:
            probs[neighbor] = (miss*(2/3.))/20.
    if target_value == 'SB':
        probs['DB'] = miss*.25
        for neighbor in neighbors[target_value]:
            probs[neighbor] = (miss*.75)/20.
    return probs


'''{'S9': 0.016, 'S8': 0.016, 'S3': 0.016, 'S2': 0.016, 'S1': 0.016,
             'DB': 0.04, 'S6': 0.016, 'S5': 0.016, 'S4': 0.016, 'S20': 0.016,
             'S19': 0.016, 'S18': 0.016, 'S13': 0.016, 'S12': 0.016, 'S11': 0.016,
             'S10': 0.016, 'S17': 0.016, 'S16': 0.016, 'S15': 0.016, 'S14': 0.016,
             'S7': 0.016, 'SB': 0.64}))'''


def make_bull(target_value, miss):
    rings = {}
    numbers = {}
    probs = {}
    if target_value == 'DB':
        rings['SB'] = miss/3.
        rings['DB'] = 1-miss
        rings['S'] = 2*miss/3.
        extra = ((1-miss)*rings['S'])/20.
        numbers['DB'] = 1-miss
        numbers['SB'] = 1-miss
        numbers['S'] = miss/20.
        probs['DB'] = rings['DB']*numbers['DB']
        probs['SB'] = rings['SB']*numbers['SB']
        for number in range(1,21):
            probs['S'+str(number)] = extra + numbers['S']
    if target_value == 'SB':
        rings['SB'] = 1-miss
        rings['DB'] = miss/4.
        rings['S'] = 3*miss/4.
        extra = ((1-miss)*rings['S'])/20.
        numbers['DB'] = 1-miss
        numbers['SB'] = 1-miss
        numbers['S'] = miss/20.
        probs['DB'] = rings['DB']*numbers['DB']
        probs['SB'] = rings['SB']*numbers['SB']
        for number in range(1,21):
            probs['S'+str(number)] = extra + numbers['S']
    return probs




def make_single(target_value, miss):
    hit = 1-miss
    numbers = {target_value: hit}
    for neighbor in neighbors[target_value]:
        numbers[neighbor] = .5*miss
    rings = {}
    miss = miss/5.
    hit = 1-miss
    rings['S'] = hit
    rings['D'] = miss*.5
    rings['T'] = miss*.5
    probs = {}
    for ring, rp in rings.items():
        for number, np in numbers.items():
            probs[ring+number] = rp*np
    return probs

def make_double(target_value, miss):
    numbers = {target_value:(1-miss)}
    for neighbor in neighbors[target_value]:
        numbers[neighbor] = .5*miss
    rings = {}
    rings['D'] = (1-miss)
    rings['S'] = miss*.5
    rings['OFF'] = miss*.5
    probs = {'OFF':0}
    for ring, rp in rings.items():
        for number, np in numbers.items():
            if ring == 'OFF':
                probs[ring] += rp*np
            else:
                probs[ring+number] = rp*np
    return probs

def make_triple(target_value, miss):
    numbers = {target_value:(1-miss)}
    for neighbor in neighbors[target_value]:
        numbers[neighbor] = .5*miss
    rings = {}
    rings['T'] = (1-miss)
    rings['S'] = miss
    probs = {}
    for ring, rp in rings.items():
        for number, np in numbers.items():
            probs[ring+number] = rp*np
    return probs

def make_tuple(dictionary):
    return tuple((key,value) for key,value in dictionary.items())

def make_dictionary(tup):
    return {key:value for key, value in tup}

def average_score(probs):
    total = 0
    hits = 0
    for key, value in probs.items():
        if key[0] in ('T', 'D', 'S','O'):
            total += names[key] * value
        else:
            total += names['S'+key] * value
        if value <> 0 or key == 'OFF':
            hits += 1
    return total/hits


def outcome(target, miss):
    "Return a probability distribution of [(target, probability)] pairs."
    target_type = target[:1]
    target_value = target[1:]
    bull = False
    if target_value == 'B':
        bull = True
        target_value = target_type + target_value
        probs = make_bull(target_value, miss)
    else:   
        if target_type == 'S':
            probs = make_single(target_value, miss)
        elif target_type == 'D':
            probs = make_double(target_value, miss)
        elif target_type == 'T':
            probs = make_triple(target_value, miss)
    #probs = tuple((state, prob) for state,prob in probs.items())
    return probs

def best_target(miss):
    "Return the target that maximizes the expected score."
    best_score = 0
    best_name = None
    for target in names:
        if target <> 'OFF':
            this_score = average_score(outcome(target,miss))
            if this_score > best_score:
                best_score = this_score
                best_name = target
    return best_name


def same_outcome(dict1, dict2):
    "Two states are the same if all corresponding sets of locs are the same."
    return all(abs(dict1.get(key, 0) - dict2.get(key, 0)) <= 0.0001
               for key in set(dict1) | set(dict2))

def test_darts2():
    assert best_target(0.0) == 'T20'
    assert best_target(0.1) == 'T20'
    assert best_target(0.4) == 'T19'
    assert same_outcome(outcome('T20', 0.0), {'T20': 1.0})
    assert same_outcome(outcome('T20', 0.1), 
                        {'T20': 0.81, 'S1': 0.005, 'T5': 0.045, 
                         'S5': 0.005, 'T1': 0.045, 'S20': 0.09})
    assert (same_outcome(
            outcome('SB', 0.2),
            {'S9': 0.016, 'S8': 0.016, 'S3': 0.016, 'S2': 0.016, 'S1': 0.016,
             'DB': 0.04, 'S6': 0.016, 'S5': 0.016, 'S4': 0.016, 'S20': 0.016,
             'S19': 0.016, 'S18': 0.016, 'S13': 0.016, 'S12': 0.016, 'S11': 0.016,
             'S10': 0.016, 'S17': 0.016, 'S16': 0.016, 'S15': 0.016, 'S14': 0.016,
             'S7': 0.016, 'SB': 0.64}))


def test_darts3():
    "Test the double_out function."
    assert double_out(170) == ['T20', 'T20', 'DB']
    assert double_out(171) == None
    assert double_out(100) in (['T20', 'D20'], ['DB', 'DB'])
    for total in [0, 1, 159, 162, 163, 165, 166, 168, 169, 171, 200]:
        assert double_out(total) == None

def test_darts4():
    assert best_target(0.0) == 'T20'
    assert best_target(0.1) == 'T20'
    assert best_target(0.4) == 'T19'
    assert same_outcome(outcome('T20', 0.0), {'T20': 1.0})
    assert same_outcome(outcome('T20', 0.1), 
                        {'T20': 0.81, 'S1': 0.005, 'T5': 0.045, 
                         'S5': 0.005, 'T1': 0.045, 'S20': 0.09})
    assert same_outcome(
            outcome('SB', 0.2),
            {'S9': 0.016, 'S8': 0.016, 'S3': 0.016, 'S2': 0.016, 'S1': 0.016,
             'DB': 0.04, 'S6': 0.016, 'S5': 0.016, 'S4': 0.016, 'S20': 0.016,
             'S19': 0.016, 'S18': 0.016, 'S13': 0.016, 'S12': 0.016,
             'S11': 0.016, 'S10': 0.016, 'S17': 0.016, 'S16': 0.016, 'S15':
             0.016, 'S14': 0.016, 'S7': 0.016, 'SB': 0.64})
    assert same_outcome(outcome('T20', 0.3),
                        {'S1': 0.045, 'T5': 0.105, 'S5': 0.045,
                         'T1': 0.105, 'S20': 0.21, 'T20': 0.49})
    assert best_target(0.6) == 'T7'


test_darts4()
print 'done'
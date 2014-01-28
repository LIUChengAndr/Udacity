"""
UNIT 2: Logic Puzzle

You will write code to solve the following logic puzzle:

1. The person who arrived on Wednesday bought the laptop.
2. The programmer is not Wilkes.
3. Of the programmer and the person who bought the droid,
   one is Wilkes and the other is Hamming. 
4. The writer is not Minsky.
5. Neither Knuth nor the person who bought the tablet is the manager.
6. Knuth arrived the day after Simon.
7. The person who arrived on Thursday is not the designer.
8. The person who arrived on Friday didn't buy the tablet.
9. The designer didn't buy the droid.
10. Knuth arrived the day after the manager.
11. Of the person who bought the laptop and Wilkes,
    one arrived on Monday and the other is the writer.
12. Either the person who bought the iphone or the person who bought the tablet
    arrived on Tuesday.

You will write the function logic_puzzle(), which should return a list of the
names of the people in the order in which they arrive. For example, if they
happen to arrive in alphabetical order, Hamming on Monday, Knuth on Tuesday, etc.,
then you would return:

['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']

(You can assume that the days mentioned are all in the same week.)
"""

import itertools


def logic_puzzle():
    "Return a list of the names of the people, in the order they arrive."
    ## your code here; you are free to define additional functions if needed
    days = (mon, tues, wed, thurs, fri) = (1,2,3,4,5)
    possible_days = list(itertools.permutations(days))
    return next(sorter(Wilkes = Wilkes, Hamming = Hamming, Minsky = Minsky, 
                       Knuth = Knuth, Simon = Simon)
                for (Wilkes, Hamming, Minsky, Knuth, Simon) in possible_days
                for  (laptop, droid, tablet, iphone,_) in possible_days
                for (programmer,writer, designer,manager,_) in possible_days
                if laptop == wed
                if programmer <> Wilkes
                if set([programmer, droid]) == set([Wilkes, Hamming])
                if writer <> Minsky
                if manager <> tablet
                if Knuth <> manager
                if Knuth <> tablet
                if Knuth == Simon + 1
                if thurs <> designer
                if fri <> tablet
                if designer <> droid
                if Knuth == manager + 1
                if set([laptop, Wilkes]) == set([mon, writer])
                if tues in set([iphone, tablet])
                )


def sorter(**names):
    return sorted(names, key= lambda name: names[name])


assert 'Minsky' in logic_puzzle()
assert logic_puzzle() == ['Wilkes', 'Simon', 'Knuth', 'Hamming', 'Minsky']
print 'done'
  


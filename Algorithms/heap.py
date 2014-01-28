import random


class Heap:
    def __init__(self):
        self.l = []

    def parent(self, i):
        return(i-1)/2

    def left_child(self,i):
        return 2*i+1

    def right_child(self,i):
        return 2*i+2

    def is_leaf(self, i):
        return (self.left_child(i) >= len(self.l)) and (self.right_child(i) >= len(self.l))

    def one_child(self, i):
        return (self.left_child(i) < len(self.l)) and (self.right_child(i) >= len(self.l))

    def check_valid(self):
        for i in xrange(len(self.l)):
            if not self.is_leaf(i):
                if self.one_child(i):
                    if self.l[i] > self.l[self.left_child(i)]:
                        return False
                else:
                    if self.l[i] > min(self.l[self.left_child(i)], self.l[self.right_child(i)]):
                        return False
        return True

    def down_heapify(self, i):
        if self.is_leaf(i):
            return
        if self.one_child(i):
            if self.l[i] > self.l[self.left_child(i)]:
                (self.l[i], self.l[self.left_child(i)]) = (self.l[self.left_child(i)], self.l[i])
            return
        if min(self.l[self.left_child(i)], self.l[self.right_child(i)]) >= self.l[i]:
            return
        if self.l[self.left_child(i)] < self.l[self.right_child(i)]:
            (self.l[i], self.l[self.left_child(i)]) = (self.l[self.left_child(i)], self.l[i])
            self.down_heapify(self.left_child(i))
            return
        else:
            (self.l[i], self.l[self.right_child(i)]) = (self.l[self.right_child(i)], self.l[i])
            self.down_heapify(self.right_child(i))

    def up_heapify(self, i):
        if i < 1:
            return
        if self.l[i] > self.l[self.parent(i)]:
            return
        (self.l[i], self.l[self.parent(i)]) = (self.l[self.parent(i)], self.l[i])
        self.up_heapify(self.parent(i))

    def build_heap(self, L):
        self.l = L
        for i in range(len(self.l)-1, -1, -1):
            self.down_heapify(i)

    def add_to_heap(self, number):
        self.l.append(number)
        self.up_heapify(len(self.l)-1)

    def remove_minimum(self):
        if len(self.l) > 0:
            minimum = self.l[0]
            self.l[0] = self.l.pop()
            self.down_heapify(0)
            return minimum

    def minimum(self):
        if len(self.l) == 0:
            return None
        return self.l[0]

    def remove_maximum(self):
        if len(self.l) == 0:
            return None
        if len(self.l) == 1:
            maximum = self.l[0]
            self.l.pop()
            return maximum
        maximum = -10**30
        location = 0
        for i in range(len(self.l)-1,self.parent(len(self.l)-1),-1):
            if maximum < self.l[i]:
                maximum = self.l[i]
                location = i
        if location == len(self.l)-1:
            self.l.pop()
        else:
            self.l[location] = self.l.pop()
            self.up_heapify(location)
        return maximum

    def maximum(self):
        if len(self.l) == 0:
            return None
        if len(self.l) == 1:
            return self.l[0]
        maximum = -10**30
        for i in range(len(self.l)-1,self.parent(len(self.l)-1),-1):
            if maximum < self.l[i]:
                maximum = self.l[i]
        return maximum
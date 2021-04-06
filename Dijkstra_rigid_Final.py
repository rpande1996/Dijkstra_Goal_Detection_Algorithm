import numpy as np
import cv2

radius = 10
clearance = 5
cl = radius + clearance

# Map creation with edges as '1' in order to provide a void border of the map

obs_map = np.zeros((302, 402), dtype=int)
obs_map[0, :] = 1
obs_map[301, :] = 1
obs_map[:, 0] = 1
obs_map[:, 401] = 1

class Queue:

    # Creating a class to convert a list into a queue

    def __init__(self):
        self.queue = []

    def add(self, node):
        self.queue.append(node)

    def pop(self):
        ind = self.queue.index(min(self.queue))
        node = self.queue.pop(ind)
        return node

    def __len__(self):
        return len(self.queue)

# Creating a class to determine the node of the iteration. Node is the puzzle state.

class Node:

    # Defining the __init__ function

    def __init__(self, data, parent, act, cost):
        self.data = data
        self.parent = parent
        self.act = act
        self.id = self.get_id()
        self.cost = cost

    def __eq__(self, other):
        if hasattr(other, 'cost'):
            return self.cost == other.cost
        else:
            raise NotImplementedError('Not supported between given types')

    def __ne__(self, other):
        if hasattr(other, 'cost'):
            return self.cost != other.cost
        else:
            raise NotImplementedError('Not supported between given types')

    def __lt__(self, other):
        if hasattr(other, 'cost'):
            return self.cost < other.cost
        else:
            raise NotImplementedError('Not supported between given types')

    def __gt__(self, other):
        if hasattr(other, 'cost'):
            return self.cost > other.cost
        else:
            raise NotImplementedError('Not supported between given types')

    def __le__(self, other):
        if hasattr(other, 'cost'):
            return self.cost <= other.cost
        else:
            raise NotImplementedError('Not supported between given types')

    def __ge__(self, other):
        if hasattr(other, 'cost'):
            return self.cost >= other.cost
        else:
            raise NotImplementedError('Not supported between given types')

    # Defining a function to generate a unique id of the state of the puzzle.

    def get_id(self):
        _id = np.ravel(self.data).tolist()
        _id = [str(item) for item in _id]
        _id = "-".join(_id)
        self.id = _id
        return self.id

    # Defining the __repr__ function

    def __repr__(self):
    def __repr__(self):
        return str(self.data)
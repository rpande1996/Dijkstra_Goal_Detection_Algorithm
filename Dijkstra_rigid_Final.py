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

# Creating a function to define the circle obstacle's area on the map

def getCircleObstacle(i, j):
    global cl
    cond = ((j - 90) ** 2) + ((i - 70) ** 2) <= ((35 + cl) ** 2)
    return cond

# Creating a function to define the C shape obstacle's area on the map

def getCShapeObstacle(i, j):
    global cl
    cond1 = i <= 270 - cl
    cond2 = i <= 280 + cl
    cond3 = j >= 200 - cl
    cond4 = j >= 210 + cl
    cond5 = i >= 240 + cl
    cond6 = i >= 230 - cl
    cond7 = j <= 230 + cl
    ret_val = ((cond2 and cond3 and cond6 and cond7) and not (cond1 and cond4 and cond5 and cond7))
    return ret_val

# Creating a function to define the slanted rectangle obstacle's area on the map

def getSlantedRectObstacle(i, j):
    global cl
    s1 = 0.7
    s2 = -1.42814
    x1 = np.arctan(s1)
    x2 = np.arctan(s2)
    d1 = np.cos(np.pi - x1)
    d2 = np.cos(np.pi - x2)
    a = -(cl / d1)
    b = -(cl / d2)
    cond1 = (i) + (1.42814 * j) >= (176.5511 - b)
    cond2 = (i) - (0.7 * j) >= (74.39 - a)
    cond3 = (i) + (1.42814 * j) <= (428.06815 + b)
    cond4 = (i) - (0.7 * j) <= (98.80545 + a)
    ret_val = (cond1 and cond2 and cond3 and cond4)
    return ret_val

# Creating a function to define the ellipse obstacle's area on the map

def getEllipseObstacle(i, j):
    global cl
    cond = (((j - 246) / (60 + cl)) ** 2) + (((i - 145) / (30 + cl)) ** 2) <= 1
    return cond


def getBorderClearance(i, j):
    global cl
    cond1 = j >= 402 - cl
    cond2 = j <= cl
    cond3 = i >= 302 - cl
    cond4 = i <= cl
    ret_val = cond1 or cond2 or cond3 or cond4
    return ret_val

# Creating an if-condition to change value of the element in area under all obstacles to '1' in order to create a void in the map

for i in range(obs_map.shape[0]):
    for j in range(obs_map.shape[1]):
        if getCircleObstacle(obs_map.shape[0] - i, j) or getCShapeObstacle(obs_map.shape[0] - i,
                                                                           j) or getSlantedRectObstacle(
            obs_map.shape[0] - i, j) or getEllipseObstacle(obs_map.shape[0] - i, j) or getBorderClearance(
            obs_map.shape[0] - i, j):
            obs_map[i, j] = 1

# Defining the move functions
# Defining the move up function where if the element above does not have '1' value, i.e. if there isn't a void in the element above, the object moves up

def move_up(i, j):
    if obs_map[i - 1, j] != 1:
        return (i - 1, j)


# Defining the move down function where if the element below does not have '1' value, i.e. if there isn't a void in the element below, the object moves down

def move_down(i, j):
    if obs_map[i + 1, j] != 1:
        return (i + 1, j)


# Defining the move left function where if the element on the left does not have '1' value, i.e. if there isn't a void in the element on the left, the object moves left

def move_left(i, j):
    if obs_map[i, j - 1] != 1:
        return (i, j - 1)


# Defining the move right function where if the element on the right does not have '1' value, i.e. if there isn't a void in the element on the right, the object moves right

def move_right(i, j):
    if obs_map[i, j + 1] != 1:
        return (i, j + 1)


# Defining the move up left function where if the element above and left does not have '1' value, i.e. if there isn't a void in the element above and left , the object moves up left

def move_up_left(i, j):
    if obs_map[i - 1, j - 1] != 1:
        return (i - 1, j - 1)


# Defining the move up right function where if the element above and right does not have '1' value, i.e. if there isn't a void in the element above and right, the object moves up right

def move_up_right(i, j):
    if obs_map[i - 1, j + 1] != 1:
        return (i - 1, j + 1)


# Defining the move down left function where if the element below and left does not have '1' value, i.e. if there isn't a void in the element below and left, the object moves down left

def move_down_left(i, j):
    if obs_map[i + 1, j - 1] != 1:
        return (i + 1, j - 1)


# Defining the move down right function where if the element below and right does not have '1' value, i.e. if there isn't a void in the element below and right, the object moves down right

def move_down_right(i, j):
    if obs_map[i + 1, j + 1] != 1:
        return (i + 1, j + 1)

# Defining a function to generate new legal moves as per the state

def generate_new_moves(state):
    list_states = []
    for func in [move_left, move_right, move_down, move_up]:
        cost = state.cost + 1
        dum_state = state.data
        out_state = func(dum_state[0], dum_state[1])
        if out_state is not None:
            list_states.append((out_state, cost))
    for func in [move_up_left, move_up_right, move_down_left,
                 move_down_right]:
        cost = state.cost + 1.414
        dum_state = state.data
        out_state = func(dum_state[0], dum_state[1])
        if out_state is not None:
            list_states.append((out_state, cost))
    return list_states

# Inputting values from the user and checking if the values are valid by checking the outbound values and in-obstacle values

try:
    start_node_x = int(input('Enter start node x postion: '))
    if start_node_x < 0:
        print("Invalid start node x position, setting x postion to 0")
        start_node_x = 0
    elif start_node_x > 402:
        print("Invalid start node x position, setting x postion to 403")
        start_node_x = 402

    start_node_y = int(input('Enter start node y postion: '))
    if start_node_y < 0:
        print("Invalid start node y position, setting y postion to 0")
        start_node_y = 0
    elif start_node_y > 302:
        print("Invalid start node y position, setting y postion to 300")
        start_node_y = 302

    goal_node_x = int(input('Enter goal node x postion: '))
    if goal_node_x < 0:
        print("Invalid goal node x position, setting x postion to 0")
        goal_node_x = 0
    elif goal_node_x > 402:
        print("Invalid goal node x position, setting x postion to 403")
        start_node_x = 402

    goal_node_y = int(input('Enter goal node y postion: '))
    if goal_node_y < 0:
        print("Invalid goal node y position, setting y postion to 0")
        goal_node_y = 0
    elif goal_node_y > 302:
        print("Invalid goal node y position, setting y postion to 300")
        start_node_y = 302

    if obs_map[obs_map.shape[0] - start_node_y, start_node_x] == 1:
        print("Error: Start position is in void space. Exiting program")
        exit(1)

    if obs_map[obs_map.shape[0] - goal_node_y, goal_node_x] == 1:
        print("Error: Goal position is in void space. Exiting program")
        exit(1)
except:
    print("Error: Invalid Input. Exiting program")
    exit(2)
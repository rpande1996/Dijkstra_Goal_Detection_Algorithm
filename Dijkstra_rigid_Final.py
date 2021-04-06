import numpy as np
import cv2

radius = 10
clearance = 5
cl = radius + clearance

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
import numpy as np
import math
from sheep import Sheep
from numpy import random

class Flock:

    # flock = []
    # flock_positions = [[]]

    separation_weight = 0.7
    alignment_weight = 0.5
    cohesion_weight = 0.5

    def __init__(self, n, e):
        self.num_of_sheep = n    
        self.env = e

        self.dists = np.zeros([self.num_of_sheep, self.num_of_sheep])
        
        # get flock of n sheep on init
        # log positions at t=0
        sheep = []
        sheep_posX = []
        sheep_posY = []
        for s in range(self.num_of_sheep):
            sheep.append(Sheep(s, self.env.height, self.env.width))
            sheep[s].set_pos(self.random_start_pos(25, 25, self.env.width-25, self.env.height-25))
            sheep_posX.append(sheep[s].pos[0])
            sheep_posY.append(sheep[s].pos[1])

        self.flock = np.array(sheep)
        self.flock_positionsX = np.array(sheep_posX)
        self.flock_positionsY = np.array(sheep_posY)

    # random start position within starting area
    # xMin, yMin, xMax, yMax bounds of start area
    def random_start_pos(self, xMin, yMin, xMax, yMax):
        xDiff = xMax-xMin
        yDiff = yMax-yMin
        p = np.array([random.rand()*xDiff + xMin, random.rand()*yDiff + yMin])
        # check if p is valid when obstacles added
        return p

    def calc_distances_sheep(self):
        # create matrix of distances between sheep
        # this is a 2D array of floats, and None value if same agent
        for sheep in self.flock:
            for other in self.flock:
                if sheep.id == other.id:
                    self.dists[sheep.id][other.id] = 0  # zero distance from self, remember to account for this later
                else:
                    self.dists[sheep.id][other.id] = np.linalg.norm(other.pos - sheep.pos)
        # print(self.dists)


    def calc_distances_sheepdogs(self):
        # create matrix of distances from sheepdogs
        pass

    # calc flock centre of mass
    def calc_flock_centre(self):
        # avg x pos
        flock_avg_x = np.average(self.flock_positionsX)
        # avg y pos
        flock_avg_y = np.average(self.flock_positionsY)
        return np.array([flock_avg_x, flock_avg_y])

    # calc flock density
    def calc_flock_density(self, threshold):
        # if all distances between sheep are below threshold
        # apply np.all() to flock dist matrix
        pass

    def calc_flocking(self):        
        # loop through flock
        for sheep in self.flock:
            # call separation, alignment & cohesion calcs
            sheep.apply_flocking(self.flock, self.dists, self.separation_weight, self.alignment_weight, self.cohesion_weight)

    def update_flock(self):
        self.calc_distances_sheep()
        self.calc_flocking()
        for sheep in self.flock:
            # update pos
            sheep.update_agent()
            # log position change
            np.put(self.flock_positionsX, sheep.id, sheep.pos[0])
            np.put(self.flock_positionsY, sheep.id, sheep.pos[1])
            # self.flock_positionsX[sheep.id] = sheep.pos[0]
            # self.flock_positionsY[sheep.id] = sheep.pos[1]
            

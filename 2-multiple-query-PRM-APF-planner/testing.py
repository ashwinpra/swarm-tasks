import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.patches import Polygon
from matplotlib.path import Path



def check_point(Q,obstacles):
    checks = np.full(len(Q),1)
    # check if point lies within the obstacle 
    for obstacle in obstacles:
        p = Path(obstacle)  
        bool = p.contains_point(Q)
        for i in range(len(bool)):
            if bool[i] == True:
                checks[i] = 0
    return checks



obstacles = []

with open("obstacles.txt") as f:
    for line in f:
        coord_arr = []
        vertices_arr = line.split()
        # join each 2 consecutive values and form an array of coordinates
        for i in range(0, len(vertices_arr), 2):
            coord_arr.append((int(vertices_arr[i]), int(vertices_arr[i+1])))
        obstacles.append(coord_arr)

# A list of coordinates that are chosen randomly 
N_nodes = 1000
Q = [(np.random.rand()*60, np.random.rand()*40) for _ in range(N_nodes)]


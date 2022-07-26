import numpy as np 
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# The map is 60 x 40
map = np.zeros((60, 40))
# Nodes can be denoted by 1s and obstacles (all the cells in the area) by 0s

#! Utility functions

def dist(q1,q2):
    return (q1[0]-q2[0])**2 + (q1[1]-q2[1])**2

def knn(q,Q,k):
    dists = [dist(q,p) for p in Q if p != q]
    return [Q[i] for i in np.argsort(dists)[:k]]

def astar(start,goal,nodes):
    pass

def apf(q1,q2):
    pass


plt.rcParams['figure.figsize'] = (12, 8)
x = np.linspace(0, 60, 10)
y = np.linspace(0, 40, 10)
fig,ax = plt.subplots()

ax.set_title('Probabilistic Road Map')

with open("obstacles.txt") as f:
    for line in f:
        coord_arr = []
        vertices_arr = line.split()
        # join each 2 consecutive values and form an array of coordinates
        for i in range(0, len(vertices_arr), 2):
            coord_arr.append((int(vertices_arr[i]), int(vertices_arr[i+1])))
        p = Polygon(coord_arr, facecolor = 'blue', edgecolor = 'black')
        ax.add_patch(p)
        ax.set_xlim([0, 60])
        ax.set_ylim([0, 40])
        #plt.fill(vertices_arr[::2], vertices_arr[1::2])


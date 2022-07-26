import numpy as np 
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.path import Path

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

def check_points(Q,obstacles):
    checks = np.full(len(Q),1)
    # check if point lies within the obstacle 
    for obstacle in obstacles:
        p = Path(obstacle)  
        print(p)
        bool = p.contains_points(Q)
        for i in range(len(bool)):
            if bool[i] == True:
                checks[i] = 0
    return checks

plt.rcParams['figure.figsize'] = (12, 8)

fig,ax = plt.subplots()

ax.set_title('Probabilistic Road Map')

obstacles = []
with open("2-multiple-query-PRM-APF-planner/obstacles.txt") as f:
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
        obstacles.append(coord_arr)

# A list of coordinates that are chosen randomly 
N_nodes = 100
Q = [(np.random.randint(0,60), np.random.randint(0,40)) for _ in range(N_nodes)]

check = check_points(Q,obstacles)

for point in Q:
    if check[Q.index(point)] == 1:
        plt.scatter(point[0], point[1], color = 'green', marker = 'o', s = 25)
    else:
        plt.scatter(point[0], point[1], color = 'red', marker = 'o', s = 25)

# Now use APF to join the green nodes 


plt.show()



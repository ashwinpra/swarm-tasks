import numpy as np 
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.path import Path

N_nodes = 100
N_knn = 3
# The map is 60 x 40
# map = np.zeros((60, 40))
# Nodes can be denoted by 1s and obstacles (all the cells in the area) by 0s

#! Utility functions

def dist(q1,q2):
    return (q1[0]-q2[0])**2 + (q1[1]-q2[1])**2

def knn(q,Q,k):
    dists = [dist(q,p) for p in Q if p != q]
    return [Q[i] for i in np.argsort(dists)[:k]]

def apf(q1,q2):
    pass

def check_points(Q,obs):
    checks = np.full(len(Q),1)
    # check if point lies within the obstacle 
    for obstacle in obs:
        p = Path(obstacle)  
        bool = p.contains_points(Q)
        for i in range(len(bool)):
            if bool[i] == True:
                checks[i] = 0
    return checks

def check_collision(q1, q2, obs):
    sx, sy = q1[0], q1[1]
    ex, ey = q2[0], q2[1]

    for obstacle in obs:
        p = Path(obstacle)
        for i in range(100):
            u = i / 100
            x = sx * u + ex * (1 - u)
            y = sy * u + ey * (1 - u)
            if p.contains_point((x, y)):
                return True
    return False

def a_star(q_start,q_goal,Q_v,obstacles):    # Height and Width of the maze
        parent = np.zeros(len(Q_v)) # Keeping track of the parent pixels
        visited = []    # Keepinig a list of visited pixels so that we dont visit the same pixel again
        current = q_start
        visited.append(current)
        distance = np.full(len(Q_v),np.inf)
        pixel_distance = np.full(len(Q_v), np.inf)
        distance[0] = 0
        pixel_distance[0] = 0
         # Loop runs until we reach the target 
        while True:
            if current != q_goal:
                for q_n in knn(current,Q_v,N_knn):
                    if (not check_collision(current, q_n, obstacles)):
                        pixel_distance[Q_v.index(q_n)] = pixel_distance[current] + dist(q_n, current)
                        if distance[Q_v.index(q_n)] > pixel_distance[Q_v.index(q_n)]+ dist(q_n, current) + dist(q_n, q_goal):
                            distance[Q_v.index(q_n)] = pixel_distance[Q_v.index(q_n)] + dist(q_n, current)+ dist(q_n, q_goal)
                            parent[q_n] =  current
                            visited.append(q_n)
                    # Choosing the pixel with the least current distance for analysis in the next cycle
                        min = np.inf
                    for point in visited:
                        if distance[point] < min:
                            min = distance[point]
                            current = point
                    if not len(visited):
                        return None, None
                    else:
                        visited.remove(current)
                else:
                    distance[q_goal] = distance[current] +dist(q_goal, current)
                    return distance[q_goal], parent

def trackaStar(q_start,q_goal,dist,parent):
        #img = np.copy(self.inimg)       # Making a copy of the maze for the algorithm to work on
        #dist, parent = a_star(img)   # Running the algorithm
        # Tracking the final path
        current = tuple(list(map(int, parent[q_goal])))
        dist = 1
        while current != q_start:
            dist += 1
            #img[current] = GREEN
            current = tuple(list(map(int, parent[current])))
            # Scaling the right maze
            #if img.shape[0] < 100:
               # showImg = cv2.resize(img, (500,500), interpolation=cv2.INTER_AREA)
                #cv2.imshow("A*", showImg)
                #cv2.waitKey(1)
            #else:
                #cv2.imshow("A*", img)
        # Printing the final
        print("Distance: " + str(dist) + " pixels")

plt.rcParams['figure.figsize'] = (12, 8)

fig,ax = plt.subplots()

ax.set_title('Probabilistic Road Map')


#! Checkpoint 1
#! ----------------------------------------------------------------------------------------------------------------------

obstacles = []
with open("obstacles.txt") as f:
    for line in f:
        coord_arr = []
        vertices_arr = line.split()
        # join each 2 consecutive values and form an array of coordinates
        for i in range(0, len(vertices_arr), 2):
            coord_arr.append((int(vertices_arr[i]), int(vertices_arr[i+1])))
        p = Polygon(coord_arr, facecolor = 'blue', edgecolor = 'black')
        ax.add_patch(p)
        ax.set_xlim([-5, 65])
        ax.set_ylim([-5, 45])
        obstacles.append(coord_arr)

# A list of coordinates that are chosen randomly 
Q = [(np.random.randint(0,60), np.random.randint(0,40)) for _ in range(N_nodes)]

check = check_points(Q,obstacles)

Q_valid = []
for point in Q:
    if check[Q.index(point)] == 1:
        Q_valid.append(point)
        ax.scatter(point[0], point[1], color = 'green', marker = 'o', s = 25)
    else:
        ax.scatter(point[0], point[1], color = 'red', marker = 'o', s = 25)



connections = []
for q in Q_valid:
    for q_n in knn(q,Q_valid,N_knn):
        if (not check_collision(q, q_n, obstacles) and ((q,q_n) or (q_n,q) not in connections)):
            connections.append((q, q_n))
            ax.plot([q[0], q_n[0]], [q[1], q_n[1]], color = 'green')

#!----------------------------------------------------------------------------------------------------------------------

#! Checkpoint 2
#! --------------------------------------------------------------------------------------------------------------------

# Now we start the work with queries
starts = []
goals = []
with open("queries.txt") as f:
    for line in f:
        # first 2 numbers represent coordinate of start, last 2 numbers represent coordinate of goals
        coords = line.split()
        # join each 2 consecutive values and form an array of coordinates
        starts.append((coords[0], coords[1]))
        goals.append((coords[2], coords[3]))

for start, goal in zip(starts, goals):
    ax.scatter(int(start[0]), int(start[1]), color = 'orange',marker='x',  s = 50)
    ax.scatter(int(goal[0]), int(goal[1]), color = 'cyan',marker='x', s = 50)

    q_n_start = knn(start, Q_valid, N_knn)
    q_n_goal = knn(goal, Q_valid, N_knn)



plt.show()



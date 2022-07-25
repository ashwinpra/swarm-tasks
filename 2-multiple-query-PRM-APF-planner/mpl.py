import numpy as np
import matplotlib.pyplot as plt 

with open("obstacles.txt") as f:
    for line in f:
        vertices_arr = line.split()
        print(vertices_arr[::2], vertices_arr[1::2])
    
# def dist(q1,q2):
#     return (q1[0]-q2[0])**2 + (q1[1]-q2[1])**2
    
# def knn(q,Q,k):
#     dists = [dist(q,p) for p in Q if p != q]
#     return [Q[i] for i in np.argsort(dists)[:k]]

# N_nodes = 100
# Q = [(np.random.randint(0, 60), np.random.randint(0, 40)) for _ in range(N_nodes)]

# knn_q = knn(Q[0],Q,10)

# dists = [dist(Q[0],p) for p in Q]
# #print(dists)

# print(Q)
# print(knn_q)
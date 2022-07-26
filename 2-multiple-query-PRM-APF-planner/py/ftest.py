import numpy as np
import matplotlib.pyplot as plt

# with open("text.txt") as f:
#     for line in f:
#         vertices_arr = line.split()
#         #ax.fill(vertices_arr[::2], vertices_arr[1::2], 'b')
        

plt.rcParams['figure.figsize'] = (12, 8)
x = np.linspace(0, 60, 10)
y = np.linspace(0, 40, 10)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(0, 60)
ax.set_ylim(0, 40)
#!Make the scales equal 
ax.set_title('Probabilistic Road Map')


with open("text.txt") as f:
    for line in f:
        vertices_arr = line.split()
        print(vertices_arr)
        print(vertices_arr[::2])
        print(vertices_arr[1::2])
        ax.fill(vertices_arr[::2], vertices_arr[1::2], 'b')

plt.show()


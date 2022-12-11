from gridsolver import GridSolver
from gridvisualiser import GridVisualiser
import numpy as np

pathfinder = GridSolver(1,0.9,10000)

ql_q_table = pathfinder.q_learning()    

N_trials = 1000 

rewards = []
paths = []
for _ in range(N_trials):
    ql_path,ql_reward = pathfinder.get_path(ql_q_table)
    rewards.append(ql_reward)
    paths.append(ql_path)
avg_reward = np.mean(rewards)
highest_reward = np.max(rewards)
ql_path = paths[rewards.index(highest_reward)]
print("-------------------------------")
print("Average reward:", avg_reward)
print("Highest reward: ", highest_reward)

gridvisualiser = GridVisualiser()
grid = gridvisualiser.draw_grid()
gridvisualiser.show_path(grid,ql_path)

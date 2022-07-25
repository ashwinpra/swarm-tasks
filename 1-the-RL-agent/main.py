from gridsolver import GridSolver
from gridvisualiser import GridVisualiser
import numpy as np

pathfinder = GridSolver(1,0.9,0.01,1000)

ql_q_table = pathfinder.q_learning()

ql_path,ql_reward = pathfinder.get_path(ql_q_table)


print(f"QL reward: {ql_reward}")
gridvisualiser = GridVisualiser()
grid = gridvisualiser.draw_grid()
print("-------------------------------")
print("QL path:")
print(ql_path)
print("-------------------------------")
gridvisualiser.show_path(grid,ql_path)



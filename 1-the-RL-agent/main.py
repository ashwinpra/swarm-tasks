from gridsolver import GridSolver
#from gridvisualiser import GridVisualiser
import numpy as np

pathfinder = GridSolver(1,0.9,0.01,10000)

ql_q_table = pathfinder.q_learning()
#sarsa_q_table = pathfinder.sarsa()
ql_path,ql_reward = pathfinder.get_path(ql_q_table)
#sarsa_reward,sarsa_path = pathfinder.get_path(sarsa_q_table)

print(f"QL reward: {ql_reward}")
#print(f"SARSA reward: {sarsa_reward}")


#gridvisualiser = gv()



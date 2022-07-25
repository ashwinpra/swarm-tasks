from pathfinder import PathFinder as pf
from gridvisualiser import GridVisualiser as gv
import numpy as np

pathfinder = pf(1,0.1,0.1,1)

#ql_q_table = pathfinder.q_learning()
sarsa_q_table = pathfinder.sarsa()
print("sarsa table", sarsa_q_table)
#ql_reward,ql_path = pathfinder.get_path(ql_q_table)
sarsa_reward,sarsa_path = pathfinder.get_path(sarsa_q_table)

#print(f"QL reward: {ql_reward}")
print(f"SARSA reward: {sarsa_reward}")


#gridvisualiser = gv()



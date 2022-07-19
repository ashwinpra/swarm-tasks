import gridworld
import numpy as np 
import cv2 

#! Instructions 
# It starts at the start state and ends at the goal state.
# Start state: [6, 1] , Goal state: [8, 11]
# Reward -1 for each step
# Reward 0 if it leads to the goal
# Cannot move into an obstacle
# There is a wind that acts at a probability 0.8 and has a strength of 1 for rows 4 and 6 and strength 2 for row 5 
# Discount factor is 1

world = gridworld.GridWorld()

gamma = 1 # Discount rate 

alpha = 0.5 # Learning factor 

def choose_action(state, q_table, epsilon):
    # choosing the action based on epsilon-greedy approach
    if(np.random.binomial(1, epsilon) == 1):
        action = np.random.choice(world.ACTIONS)
    else:
        action = np.argmax(q_table[state[0],state[1],:])
    return action

def q_learning():
    def sarsa(alpha,epsilon,gamma): 
    #q-table storing q-values for each state and action pairs - state being coordinate, action being LEFT, RIGHT, UP, DOWN
    q_table = np.zeros((world.WORLD_HEIGHT,world.WORLD_WIDTH, len(world.ACTIONS)))

    q_table[world.START[0],world.START[1],world.ACTIONS] = 1.0
    q_table[world.GOAL[0],world.GOAL[1],world.ACTIONS] = 1.0

    N = 1000 # Number of episodes

    for i in range(N):
        s = world.START
        a = choose_action(s, q_table, epsilon)


        while(s !=world.GOAL):
        #for i in range(100):
            # taking the action and getting the next state and reward
            s_prime, r = world.step(s, a)

            a_prime = choose_action(s_prime, q_table, epsilon)

            # updating the q-table with q(s,a)
            q_table[s[0],s[1],a] = q_table[s[0],s[1],a] + alpha*(r + gamma*q_table[s_prime[0],s_prime[1],a_prime] - q_table[s[0],s[1],a])
            
            #print(f"s={s}, a={a}, s_prime={s_prime}, a_prime={a_prime}, q_table[s[0],s[1],a]={q_table[s[0],s[1],a]}")
            #print(f"s={s}, a={a}")
            # updating the state and action
            s = s_prime
            a = a_prime
        
    return q_table

# Takes Learning factor, epsilon and discount rate as parameters
def sarsa(alpha,epsilon,gamma): 
    #q-table storing q-values for each state and action pairs - state being coordinate, action being LEFT, RIGHT, UP, DOWN
    q_table = np.zeros((world.WORLD_HEIGHT,world.WORLD_WIDTH, len(world.ACTIONS)))

    q_table[world.START[0],world.START[1],world.ACTIONS] = 1.0
    q_table[world.GOAL[0],world.GOAL[1],world.ACTIONS] = 1.0

    N = 1000 # Number of episodes

    for i in range(N):
        s = world.START
        a = choose_action(s, q_table, epsilon)


        while(s !=world.GOAL):
        #for i in range(100):
            # taking the action and getting the next state and reward
            s_prime, r = world.step(s, a)

            a_prime = choose_action(s_prime, q_table, epsilon)

            # updating the q-table with q(s,a)
            q_table[s[0],s[1],a] = q_table[s[0],s[1],a] + alpha*(r + gamma*q_table[s_prime[0],s_prime[1],a_prime] - q_table[s[0],s[1],a])
            
            #print(f"s={s}, a={a}, s_prime={s_prime}, a_prime={a_prime}, q_table[s[0],s[1],a]={q_table[s[0],s[1],a]}")
            #print(f"s={s}, a={a}")
            # updating the state and action
            s = s_prime
            a = a_prime
        
    return q_table

qt = sarsa(0.5,0.1,1)

enhanced_array = np.zeros((world.WORLD_HEIGHT,world.WORLD_WIDTH)).astype(np.float32)

for i in range(world.WORLD_HEIGHT):
    for j in range(world.WORLD_WIDTH):
        enhanced_array[i,j] = np.argmax(qt[i,j,:])

print(qt)
print(enhanced_array)

# once we get the policy, we go greedily 
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

def choose_action(state, q_table, epsilon):
    # choosing the action based on epsilon-greedy approach
    if(np.random.binomial(1, epsilon) == 1):
        action = np.random.choice(world.ACTIONS)
    else:
        action = np.argmax(q_table[state[0],state[1],:])
    return action

def q_learning(alpha,epsilon,gamma):
#q-table storing q-values for each state and action pairs - state being coordinate, action being LEFT, RIGHT, UP, DOWN
    q_table = np.zeros(( world.WORLD_HEIGHT, world.WORLD_WIDTH, len( world.ACTIONS)))

    q_table[ world.START[0], world.START[1], world.ACTIONS] = 1.0
    q_table[ world.GOAL[0], world.GOAL[1], world.ACTIONS] = 1.0

    N = 1 # Number of episodes

    for i in range(N):
        s =  world.START

    while(s !=  world.GOAL):
    #for i in range(100):
        a =  choose_action(s, q_table,  epsilon)

        # taking the action and getting the next state and reward
        s_prime, r =  world.step(s, a)

        # get maximum of the next state's q-values
        a_max = np.argmax(q_table[s_prime[0],s_prime[1],:])

        # updating the q-table with q(s,a)
        q_table[s[0],s[1],a] = q_table[s[0],s[1],a] +  alpha*(r +  gamma*q_table[s_prime[0],s_prime[1],a_max] - q_table[s[0],s[1],a])
        
        #print(f"s={s}, a={a}, s_prime={s_prime}, a_prime={a_prime}, q_table[s[0],s[1],a]={q_table[s[0],s[1],a]}")
        #print(f"s={s}, a={a}")
        # updating the state and action
        s = s_prime
    
    return q_table

# Takes Learning factor, epsilon and discount rate as parameters
def sarsa(alpha,epsilon,gamma): 
    #q-table storing q-values for each state and action pairs - state being coordinate, action being LEFT, RIGHT, UP, DOWN
    q_table = np.zeros((world.WORLD_HEIGHT,world.WORLD_WIDTH, len(world.ACTIONS)))

    q_table[world.START[0],world.START[1],world.ACTIONS] = 1.0
    q_table[world.GOAL[0],world.GOAL[1],world.ACTIONS] = 1.0

    N = 10000 # Number of episodes

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

def get_path(q_table):
    s = world.START
    path = []
    total_reward = 0
    while(s != world.GOAL):
        path.append(s)
        a_max = np.argmax(q_table[s[0],s[1],:])
        s, r = world.step(s, a_max)
        total_reward += r

    return total_reward,path

sarsa_reward, sarsa_path = get_path(sarsa(0.5,0.1,1))
ql_reward, ql_path = get_path(q_learning(0.5,0.1,1))
print(f"Sarsa reward: {sarsa_reward}")
print(f"Sarsa path: {sarsa_path}")
print(f"Q-learning reward: {ql_reward}")
print(f"Q-learning path: {ql_path}")



# once we get the policy, we go greedily 
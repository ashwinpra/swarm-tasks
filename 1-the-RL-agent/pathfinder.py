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

class PathFinder():
    def __init__(self,gamma,alpha,epsilon,N):
        self.world = gridworld.GridWorld()
        self.gamma = gamma
        self.alpha = alpha
        self.epsilon = epsilon
        self.N = N
    
    def choose_action(self, state, q_table):
        if(np.random.binomial(1, self.epsilon) == 1):
            action = np.random.choice(self.world.ACTIONS)
        else:
            action = np.argmax(q_table[state[0],state[1],:])
        return action

    def q_learning(self):
        #q-table storing q-values for each state and action pairs - state being coordinate, action being LEFT, RIGHT, UP, DOWN
        q_table = np.zeros((self.world.WORLD_HEIGHT,self.world.WORLD_WIDTH, len(self.world.ACTIONS)))

        q_table[self.world.START[0],self.world.START[1],self.world.ACTIONS] = 1.0
        q_table[self.world.GOAL[0],self.world.GOAL[1],self.world.ACTIONS] = 1.0


        for i in range(self.N):
            s = self.world.START

        while(s != self.world.GOAL):
        #for i in range(100):
            a = self.choose_action(s, q_table, self.epsilon)

            # taking the action and getting the next state and reward
            s_prime, r = self.world.step(s, a)

            # get maximum of the next state's q-values
            a_max = np.argmax(q_table[s_prime[0],s_prime[1],:])

            # updating the q-table with q(s,a)
            q_table[s[0],s[1],a] = q_table[s[0],s[1],a] + self.alpha*(r + self.gamma*q_table[s_prime[0],s_prime[1],a_max] - q_table[s[0],s[1],a])
            
            #print(f"s={s}, a={a}, s_prime={s_prime}, a_prime={a_prime}, q_table[s[0],s[1],a]={q_table[s[0],s[1],a]}")
            #print(f"s={s}, a={a}")
            # updating the state and action
            s = s_prime
        
        return q_table
    
    def sarsa(self):
        #q-table storing q-values for each state and action pairs - state being coordinate, action being LEFT, RIGHT, UP, DOWN
        q_table = np.zeros((self.world.WORLD_HEIGHT,self.world.WORLD_WIDTH, len(self.world.ACTIONS)))

        q_table[self.world.START[0],self.world.START[1],self.world.ACTIONS] = 1.0
        q_table[self.world.GOAL[0],self.world.GOAL[1],self.world.ACTIONS] = 1.0


        for i in range(self.N):
            s = self.world.START
            a = self.choose_action(s, q_table, self.epsilon)


        while(s != self.world.GOAL):
        #for i in range(100):
            # taking the action and getting the next state and reward
            s_prime, r = self.world.step(s, a)          
            a_prime = self.choose_action(s_prime, q_table, self.epsilon)

            # updating the q-table with q(s,a)
            q_table[s[0],s[1],a] = q_table[s[0],s[1],a] + self.alpha*(r + self.gamma*q_table[s_prime[0],s_prime[1],a_prime] - q_table[s[0],s[1],a])
            
            #print(f"s={s}, a={a}, s_prime={s_prime}, a_prime={a_prime}, q_table[s[0],s[1],a]={q_table[s[0],s[1],a]}")
            #print(f"s={s}, a={a}")
            # updating the state and action
            s = s_prime
            a = a_prime
        
        return q_table

    # once the q-table is generated, we can use it to find the optimal path
    def greedy_movement(self, q_table):
        s = self.world.START
        path = []
        total_reward = 0
        while(s != self.world.GOAL):
            path.append(s)
            a_max = np.argmax(q_table[s[0],s[1],:])
            s, r = self.world.step(s, a_max)
            total_reward += r

        return total_reward


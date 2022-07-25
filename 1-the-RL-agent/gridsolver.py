import numpy as np 
from gridworld import GridWorld

'''
Instructions 
It starts at the start state and ends at the goal state.
Start state: [6, 1] , Goal state: [8, 11]
Reward -1 for each step
Reward 0 if it leads to the goal
Cannot move into an obstacle
There is a wind that acts at a probability 0.8 and has a strength of 1 for rows 4 and 6 and strength 2 for row 5 
Discount factor is 1
'''

class GridSolver():
    def __init__(self,gamma,alpha,epsilon,N):
        self.world = GridWorld()
        self.gamma = gamma
        self.alpha = alpha
        self.epsilon = epsilon
        self.N = N
    
    # Function to choose an action following epsilon-greedy policy
    def choose_action(self, state, q_table):
        if(np.random.binomial(1, self.epsilon) == 1):
            action = np.random.choice(self.world.ACTIONS)
        else:
            action = np.argmax(q_table[state[0],state[1],:])
        return action
    
    # Q -learning implementation
    # Pseudocode used has been provided in documentation
    def q_learning(self):
        '''
        Q table storing action values for every state, action pair 
        First two dimensions correspond to coordinate (state) and last corresponds to action
        Initial action value for each state is 0 except start and goal states, which are 10
        '''
        q_table = np.zeros((self.world.WORLD_HEIGHT,self.world.WORLD_WIDTH, len(self.world.ACTIONS)))
        q_table[self.world.START[0],self.world.START[1],self.world.ACTIONS] = 10.0
        q_table[self.world.GOAL[0],self.world.GOAL[1],self.world.ACTIONS] = 10.0

        # Iterate for N episodes
        for _ in range(self.N):
            s = self.world.START
            # For each episode, keep going until we reach goal state
            while(s != self.world.GOAL):
                a = self.choose_action(s, q_table) # Choose action using above-defined function
                s_prime, r = self.world.step(s,a) # Take action and get next state and reward
                a_max = np.argmax(q_table[s_prime[0],s_prime[1],:]) # Get action with maximum value in next state
                # Update Q table based on the Q-learning formula (see documentation)
                q_table[s[0],s[1],a] = q_table[s[0],s[1],a] + self.alpha*(r + self.gamma*q_table[s_prime[0],s_prime[1],a_max] - q_table[s[0],s[1],a])
                # Next state becomes current state for next iteration
                s = s_prime
        # Finally, the Q table is returned
        return q_table
    
    # SARSA implementation
    # Pseudocode used has been provided in documentation
    def sarsa(self):
        '''
        The implementation is very similar to Q learning, except the updation of Q table
        '''
        q_table = np.zeros((self.world.WORLD_HEIGHT,self.world.WORLD_WIDTH, len(self.world.ACTIONS)))
        q_table[self.world.START[0],self.world.START[1],self.world.ACTIONS] = 10.0
        q_table[self.world.GOAL[0],self.world.GOAL[1],self.world.ACTIONS] = 10.0

        for _ in range(self.N):
            s = self.world.START

            while(s != self.world.GOAL):
                a = self.choose_action(s, q_table)
                s_prime, r = self.world.step(s,a)
                a_prime = self.choose_action(s_prime, q_table) # Next action is chosen in the same way (rather than maximum)
                # Update Q table based on the SARSA formula (see documentation)
                q_table[s[0],s[1],a] = q_table[s[0],s[1],a] + self.alpha*(r + self.gamma*q_table[s_prime[0],s_prime[1],a_prime] - q_table[s[0],s[1],a])

                # Next state and action becomes current state and action for next iteration
                s = s_prime
                a = a_prime
                
        return q_table

    # A path is found to the goal following greedy policy based on the Q table that has been generatedmm
    def get_path(self, q_table):
        path = []
        total_reward=0
        s = self.world.START
        while(s != self.world.GOAL):
            a = self.choose_action(s, q_table)
            s_prime, r = self.world.step(s,a)
            #print(s)
            path.append(s)
            s = s_prime
            total_reward+=r
        return path,total_reward


# if __name__ == '__main__':
#     pf = GridSolver(gamma=1, alpha=0.9, epsilon=0.01, N=10000)

#     ql_qt = pf.q_learning()

#     rewards = []
#     for _ in range(1000):
#         ql_path,ql_reward = pf.get_path(ql_qt)
#         rewards.append(ql_reward)
#     avg_reward = np.mean(rewards)
#     highest_reward = np.max(rewards)
#     print("-------------------------------")
#     print("Average reward for Q-learning:", avg_reward)
#     print("Highest reward for Q-learning: ", highest_reward)

#     pf = GridSolver(gamma=1, alpha=0.9, epsilon=0.01, N=10000)

#     sarsa_qt = pf.sarsa()

#     rewards = []
#     for _ in range(1000):
#         sarsa_path,sarsa_reward = pf.get_path(sarsa_qt)
#         rewards.append(ql_reward)
#     avg_reward = np.mean(rewards)
#     highest_reward = np.max(rewards)
#     print("-------------------------------")
#     print("Average reward for SARSA:", avg_reward)
#     print("Lowest reward for SARSA: ", highest_reward)

import numpy as np 
import gridworld

class GridSolver():
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
        q_table = np.zeros((self.world.WORLD_HEIGHT,self.world.WORLD_WIDTH, len(self.world.ACTIONS)))

        q_table[self.world.START[0],self.world.START[1],self.world.ACTIONS] = 10.0
        q_table[self.world.GOAL[0],self.world.GOAL[1],self.world.ACTIONS] = 10.0

        for _ in range(self.N):
            s = self.world.START

            while(s != self.world.GOAL):
                a = self.choose_action(s, q_table)
                s_prime, r = self.world.step(s,a)

                a_max = np.argmax(q_table[s_prime[0],s_prime[1],:])

                q_table[s[0],s[1],a] = q_table[s[0],s[1],a] + self.alpha*(r + self.gamma*q_table[s_prime[0],s_prime[1],a_max] - q_table[s[0],s[1],a])

                s = s_prime

        return q_table
    
    def sarsa(self):
        q_table = np.zeros((self.world.WORLD_HEIGHT,self.world.WORLD_WIDTH, len(self.world.ACTIONS)))

        q_table[self.world.START[0],self.world.START[1],self.world.ACTIONS] = 10.0
        q_table[self.world.GOAL[0],self.world.GOAL[1],self.world.ACTIONS] = 10.0

        for _ in range(self.N):
            s = self.world.START

            while(s != self.world.GOAL):
                a = self.choose_action(s, q_table)
                s_prime, r = self.world.step(s,a)

                a_prime = self.choose_action(s_prime, q_table)

                q_table[s[0],s[1],a] = q_table[s[0],s[1],a] + self.alpha*(r + self.gamma*q_table[s_prime[0],s_prime[1],a_prime] - q_table[s[0],s[1],a])

                s = s_prime
                a = a_prime
                
        return q_table

    def get_path(self, q_table):
        path = []
        total_reward=0
        s = self.world.START
        while(s != self.world.GOAL):
            a = self.choose_action(s, q_table)
            s_prime, r = self.world.step(s,a)
            #print(s_prime)
            path.append(s)
            s = s_prime
            total_reward+=r
        return path,total_reward


if __name__ == '__main__':
    pf = GridSolver(gamma=1, alpha=0.9, epsilon=0.01, N=10000)

    ql_qt = pf.q_learning()

    avg_reward = 0
    for _ in range(1000):
        ql_path,ql_reward = pf.get_path(ql_qt)
        #print("reward",ql_reward)
        avg_reward+=ql_reward
    avg_reward/=1000
    print("-------------------------------")
    print("Average reward for ql:", avg_reward)

    pf = GridSolver(gamma=1, alpha=0.9, epsilon=0.01, N=10000)

    sarsa_qt = pf.sarsa()

    avg_reward = 0
    for _ in range(1000):
        sarsa_path,sarsa_reward = pf.get_path(sarsa_qt)
        #print("reward",sarsa_reward)
        avg_reward+=sarsa_reward
    avg_reward/=1000
    print("-------------------------------")
    print("Average reward for sarsa:", avg_reward)


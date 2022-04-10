#!/usr/bin/env python3

import gym

import numpy as np

import random

# from myenv import MyEnv

class Agent:
    # agent parameters
    def __init__(self, env, epsilon=0.1, alpha=0.5, gamma=0.9):
        self._env = env
        self._epsilon = epsilon
        self._alpha = alpha
        self._gamma = gamma

    # agent uses epsilon greedy algorithm to select an action
    # epsilon decreases with each random action to reduce exploration in later episodes
    def epsilon_greedy_action(self, q_sapair):
        # q_sapair is all state action values for a given state
        if random.random() < self._epsilon:
            action = self._env.action_space.sample()
            # epsilon scheduling
            self._epsilon = 0.95 * self._epsilon
        else:
            # choose one action randomly from a set of greedy actions
            max_sa = np.max(q_sapair)
            greedy_actions = np.argwhere(q_sapair == max_sa).flatten() 
            action = np.random.choice(greedy_actions)
        
        return action
    
    # Q-learning algorithm for Reinforcement learning
    def Q_learning_update(self, q_sa, reward, q_snextall):
        # Q learning
        
        Q_snexta = np.max(q_snextall)
        target = reward + self._gamma * Q_snexta - q_sa
        
        Q_sa = q_sa + self._alpha * target
        return Q_sa
        
    
# if __name__ == "__main__":
#     print("Testing agent")
    
#     grid_map = np.array([[0, 1, 1], [0, 0, 0]])
#     rows, cols = grid_map.shape
    
#     e = MyEnv(rows, cols, grid_map)
#     a = Agent(e, epsilon=0.9)
    
#     n_actions = e.num_actions()
    
#     Q_sa = np.zeros((n_actions, rows, cols))
    
#     print(Q_sa)

    
#     for j in range(30):
#         S = []
#         R = []     
#         A = []
    
#         S.append(e.reset())
#         print("episode reset")
#         R.append(0)
    
#         done = False
#         i = 0
#         while done == False:
#             Scurr = S[i]
#             act_i = a.epsilon_greedy_action(Q_sa[:, Scurr[0], Scurr[1]]) 
#             A.append(act_i)
#             # print("action ", A[i])
#             (Snext, Rnext, done, _) = e.step(A[i])
#             Q_sa[act_i, Scurr[0], Scurr[1]] = a.Q_learning_update(Q_sa[act_i, Scurr[0], Scurr[1]], Rnext,
#                             Q_sa[:, Snext[0], Snext[1]])
        
#             S.append(Snext)
#             R.append(Rnext)
#             # print("reward: ", R[i+1])
#             # print("next state: ", S[i+1])
#             # print("done: ", done)
#             i = i + 1
#         print("goal in %d steps"%(i))
#         print(S)
#         print(a._epsilon)
#     print(Q_sa)

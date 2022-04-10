#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt


# my libraries/helpers/utilities
import myinputs
import mygraphics

from myenv import MyEnv
from myRL import Agent as MyAgent

if __name__ == "__main__":
    # read input grid
    layout_path = "layout.yaml"
    params = myinputs.read_yaml_file(layout_path)
    
    grid_map = np.array(params["map"])
    rows, cols = grid_map.shape
    
    assert rows > 0
    assert cols > 0
    
    # create environment and agent
    e = MyEnv(rows, cols, grid_map)
    a = MyAgent(e, epsilon=0.9)
    
    n_actions = e.num_actions()
    
    Q_sa = np.zeros((n_actions, rows, cols))
    
    np.set_printoptions(suppress=True, linewidth=120)
    #np.get_printoptions()
    print("State Action value matrix")
    print(Q_sa)

    # runs 31 epsiodes, each episode ends when agent reaches goal
    for j in range(31):
        S = []
        R = []     
        A = []
    
        S.append(e.reset())
        R.append(0)
    
        done = False
        i = 0
        while done == False:
            Scurr = S[i]
            # choose an action
            act_i = a.epsilon_greedy_action(Q_sa[:, Scurr[0], Scurr[1]]) 
            A.append(act_i)
            (Snext, Rnext, done, _) = e.step(A[i])
            # update corresponding state action value
            Q_sa[act_i, Scurr[0], Scurr[1]] = a.Q_learning_update(Q_sa[act_i, Scurr[0], Scurr[1]], Rnext,
                            Q_sa[:, Snext[0], Snext[1]])
        
            S.append(Snext)
            R.append(Rnext)
            i = i + 1
        print("Episode %d: goal in %d steps"%(j, i))
        
        if j%5 == 0:
            # plot steps in an episode
            # print(S)
            mygraphics.draw_one_episode(grid_map, rows, cols, S, j)
    print("State Action value matrix")
    print(Q_sa)

    np.set_printoptions()
    plt.show()    

# For TESTING    
#     for j in range(3):
#         states = []
#         curr_pos = tuple(np.random.randint(1, [rows, cols]))
#         states.append(curr_pos)
    
#         for i in range(10):
#             new_pos = np.array(curr_pos) + np.random.choice(3, 2) - np.array([1, 1])
#             curr_pos = new_pos
#             states.append(curr_pos)
                              
#         mygraphics.draw_one_episode(grid_map, rows, cols, states, j)
     
#     plt.show()
#!/usr/bin/env python3

import gym
from gym.envs.registration import EnvSpec
import numpy as np
import enum

# this is a custom environment

class Actions(enum.Enum):
    Up = 0
    Right = 1
    Down = 2
    Left = 3


# environment class has following members and methods
# action_space, observation_space, reset(), step()

class MyEnv(gym.Env):
    spec = EnvSpec('MyFirstEnv-v0', max_episode_steps=100);
    
    def __init__(self, rows, cols, grid_map):
        # rows and cols are from layout yaml file
        # error checking
        assert isinstance(rows, int);
        assert isinstance(cols, int);
        
        # up down right left
        self.action_space = gym.spaces.Discrete(n=len(Actions))
    
        # (row, col) - row from bottom to top and col is from left to right
        self.observation_space = gym.spaces.Tuple(
            spaces=(gym.spaces.Discrete(n=rows),
                    gym.spaces.Discrete(n=cols)))
        
        self._goal = (rows -1, cols - 1)
        self._start = (0, 0)
        self.form_blocked_list(grid_map)
        self._current = self._start
        
    # reset() resets and returns initial observation
    def reset(self):
        self._current = self._start
        return self._current  # starts at start position
    
    # step() takes action as input and outputs (observation, reward, 
    # done, info) info is optional and can be empty
    # SARSA - observation ~ state,
    #         action ~ action,
    #         reward ~ reward   
    def step(self, action_index):
        assert self.action_space.contains(action_index)
        
        new_state = False
        
        action = Actions(action_index)
        
        # up
        if action == Actions.Up:
            # 1) update state
            # 2) reward mechanism
            # 3) done
            new_pos = (self._current[0] + 1, self._current[1])
            # print("up :", new_pos)
        # right
        elif action == Actions.Right:
            new_pos = (self._current[0], self._current[1] + 1)
            # print("right :", new_pos)
        # down
        elif action == Actions.Down:
            new_pos = (self._current[0] - 1, self._current[1])
            # print("down :", new_pos)
        # left
        elif action == Actions.Left:
            new_pos = (self._current[0], self._current[1] - 1)
            # print("left :", new_pos)
        else:
            new_pos = self._current
        
        # update state
        if self.observation_space.contains(new_pos) and \
            not self.is_position_blocked(new_pos):
            self._current = new_pos
            new_state = True
        # else: dont change self._current 
        
        # Reward - 100 on goal, -5 on hitting a block/wall
        # and -1 elsewhere
        # return Reward and end of episode
        if self._current == self._goal:
            done = True
            reward = 100
        elif new_state == True:
            done = False
            reward = -1
        else:
            done = False
            reward = -10
        
        # extra information
        info = {"new_state": new_state}
        
        return self._current, reward, done, info
    
    # helper functions
    # number of available actions
    def num_actions(self):
        return len(Actions)
    
    # get a list of blocked cells
    def form_blocked_list(self, grid_map):
        b_indxs = np.where(grid_map)
        self._blocked = [(b_indxs[0][i], b_indxs[1][i]) 
                         for i in range(len(b_indxs[0]))]
        
    # check if cell at input position is blocked
    def is_position_blocked(self, pos):
        blocked = pos in self._blocked
        return blocked
        
        
                
# for TESTING        
# if __name__ == "__main__":
#     print("Testing environment\n")
    
    
#     grid_map = np.array([[0,1, 1], [0,0,0]])
#     rows, cols = grid_map.shape
#     e = MyEnv(rows, cols, grid_map)
    
#     print (e.action_space)
    
#     print(e.observation_space)
    
#     S = []
#     R = []
#     A = []
    
#     S.append(e.reset())
#     print("initial state: ", S[0])
#     R.append(0)
    
#     for i in range(20):
#         A.append(e.action_space.sample())
#         print("action ", A[i])
#         (Snext, Rnext, done, _) = e.step(A[i]) 
#         S.append(Snext)
#         R.append(Rnext)
#         print("reward: ", R[i+1])
#         print("next state: ", S[i+1])
#         print("done: ", done)
import numpy as np
import matplotlib.pyplot as plt
from time import sleep

# draws a grid of input rows and columns
# (0,0) is start position
# (row-1, cols-1) is goal position
def draw_map_grid(rows, cols):
    fig, ax = plt.subplots()
    
    for i in range(1, rows):
        ax.plot([0,cols], [i,i], color='black')
        
    for i in range(1, cols):
        ax.plot([i, i], [0,rows], color='black')

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    ax.set_aspect('equal')

    ax.fill_between([0, 1], [0, 0], [1, 1], color="green")
    ax.fill_between([cols-1, cols], [rows-1, rows-1], [rows, rows], color="red")

    return fig, ax

# reads obstacle locations from the map and marks them on the grid 
def draw_occupancy_map(fig, ax, occupancy_map):
    occ_indices = np.where(occupancy_map)
    for cell_idx in range(len(occ_indices[0])):
        r = occ_indices[0][cell_idx]
        c = occ_indices[1][cell_idx]
        ax.fill_between([c, c+1], [r, r], [r+1, r+1], color="blue")

    return fig, ax

# draws a step taken by the agent
# arrow indicates direction
# dot idicates agent did't change position
def draw_path(fig, ax, curr_pos, new_pos):
    dy = new_pos[0] - curr_pos[0] # rows move along y
    dx = new_pos[1] - curr_pos[1] # cols move along x
    
    if dx == 0 and dy == 0:
        ax.scatter(curr_pos[1] + 0.5, curr_pos[0] + 0.5, 
                   marker='o', color='orangered')
    else:
        ax.arrow(curr_pos[1] + 0.5, curr_pos[0] + 0.5, dx, dy,
             color='saddlebrown', head_length=0.1, head_width=0.1,
                length_includes_head=True)
            
# draws the path taken by the agent in one episode    
def draw_one_episode(grid_map, rows, cols, states, episode_num):
    assert isinstance(states, list)
    
    fig, ax = draw_map_grid(rows, cols)
    fig, ax = draw_occupancy_map(fig, ax,grid_map)
    
    for i in range(1, len(states)):
        draw_path(fig, ax, states[i-1], states[i])
    
    ax.set_title("Episode %d: %d steps"%(episode_num, i))

    plt.show(block=False)
    
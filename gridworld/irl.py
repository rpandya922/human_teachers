from __future__ import division
import numpy as np
from grid import GridWorld

# number indicates color: (1: green, 2: blue, 3: yellow, 10: goal)
grid = np.array(
    [[0, 0, 3, 3,  0],
     [0, 1, 1, 3,  0],
     [0, 2, 1, 0, 10],
     [0, 2, 1, 0,  0],
     [0, 2, 2, 2,  0]
    ])
gridworld = GridWorld(grid)

trajectory = []
goal_reached = False
while not goal_reached:
    gridworld.print_grid()
    a = raw_input("Enter next move: ")
    while a not in ['l', 'r', 'u', 'd']:
        a = raw_input("Enter next move: ")
    t, goal_reached = gridworld.transition(a)
    trajectory.append(t)
    


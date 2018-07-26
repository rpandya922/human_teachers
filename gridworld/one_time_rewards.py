from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import itertools
import networkx as nx
import random
from environment import Environment
from utils import *
import pickle

grid = np.array([[0,  0,  0,  0],
                 [0,  0,  0,  0],
                 [0, -1, -1,  0],
                 [0, -1, -1,  0]])

# each state will have current position (x, y) and indicator for each reward square
all_states = []
for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
        for b in ["".join(seq) for seq in itertools.product("01", repeat=4)]:
            all_states.append((i, j, b))

N_STATES = len(all_states)
N_ACTIONS = 4
transitions = np.zeros((N_STATES, N_STATES, N_ACTIONS))

for s0 in range(N_STATES):
    for s1 in range(N_STATES):
        for a in range(N_ACTIONS):
            i, j, b = all_states[s0]
            i1, j1, b1 = all_states[s1]
            # very unfinished function

def compute_trajectory_set_nx(grid, start, goal):
    G = nx.Graph()
    G.add_node(start)
    G.add_node(goal)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            G.add_node((i, j))
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            neighbors = get_valid_neighbors(i, j, grid)
            for n in neighbors:
                G.add_edge((i, j), n)
    # in 10x10 grid, there are over 1 million simple paths of length < 20
    return nx.all_simple_paths(G, start, goal, 20)

start, goal = (5, 0), (5, 9)
traj_generator = compute_trajectory_set_nx(grid, start, goal)
env = Environment(grid, start, goal, living_reward=0)

fig, ax = plt.subplots()
env.show_all_paths(ax)
plt.show()

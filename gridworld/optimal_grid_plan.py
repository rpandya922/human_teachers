from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import pickle
import networkx as nx
from utils import *
from environment import Environment
np.set_printoptions(precision=2)

# construct directed, weighted graph from grid + rewards
# env_26
file_name = "./data/environments.pkl"
f = open(file_name, "rb")
envs = pickle.load(f)
f.close()
env = envs['env_19']
grid = np.array(env.grid)
# start = (9,2)
# env.start = start
start = tuple(env.start)
goal = tuple(env.goal)
living_reward = -1.1
# add rewards based on style
# for now, use -alpha * avg(reward * dist) for all rewards

all_reward_locs = []
for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
        if grid[(i, j)] != 0:
            all_reward_locs.append((i, j))
alpha = 1

style_grid = np.zeros(grid.shape)
for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
        r = np.average([grid[r] * (np.sqrt((i - r[0])**2 + (j - r[1])**2)) for r in all_reward_locs])
        style_grid[i,j] = -alpha * r
print grid
print style_grid
# env.grid = style_grid
# grid = env.grid
fig, ax = plt.subplots()
env.show_grid(ax, np.min(env.grid), np.max(env.grid))
living_reward = -np.max(style_grid) - 0.1
G = nx.DiGraph()
for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
        G.add_node((i, j))
for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
        neighbors = get_valid_neighbors(i, j, grid)
        for n in neighbors:
            G.add_edge((i, j), n, weight=-(grid[n] + living_reward))
pred, dist = nx.bellman_ford(G, start, weight="weight")
print dist[goal]
prev = pred[goal][0]
path = [goal]
while prev != start:
    path.append(prev)
    prev = pred[prev][0]
path.append(start)

env.paths['path_0'] = path
env.show_path(ax, 0)
plt.show()

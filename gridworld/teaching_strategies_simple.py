from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from environment import Environment
from utils import *
np.set_printoptions(precision=2)
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
    return list(nx.all_simple_paths(G, start, goal))
def dist_to_squares(i, j, squares):
    """
    (i, j): grid location
    black_squares: list of (i, j) locations of black squares
    """
    return np.average([np.sqrt((i - i1)**2 + (j - j1)**2) for i1, j1 in squares])
def partition_function(trajectory_set, trajectory_lens, theta, distances=0, alpha=1, beta=1):
    """
    trajectory_set -DxN_FEAT - all featurized trajectories which are optimal for 
                                some theta
    trajectory_lens: Dx1 - actual length of each trajectory for living cost
    theta: N_FEATx1 - current reward parameters to reason over
    alpha: scalar - "exaggeration coeffiecient"
    beta: scalar - rationality coefficient
    """
    return np.sum(np.exp(beta * (trajectory_set.dot(theta) - 0.6*trajectory_lens) - (alpha * (theta * distances))))
def prob_trajectory_given_theta(trajectory, trajectory_set, traj_len, trajectory_lens, theta, dist=0, distances=0, alpha=1, beta=1):
    """
    trajectory: N_FEATx1 - featurized trajectory to reason about, sum of state feature counts
    theta: N_FEATx1 - current reward parameters to reason over
    trajectory_set: DxN_FEAT - all featurized trajectories
    traj_len: scalar - actual length of demonstration for living cost
    trajectory_lens: Dx1 - actual length of each trajectory for living cost
    alpha: scalar - "exaggeration coeffiecient"
    beta: scalar - rationality coefficient
    returns P(xi | theta)
    """
    return np.exp(beta * (np.dot(trajectory, theta) - 0.6*traj_len) - (alpha * (theta * dist))) / \
           partition_function(trajectory_set, trajectory_lens, theta, distances, alpha, beta)
def update_distribution(prior, thetas, demonstration, trajectory_set, traj_len, trajectory_lens, dist=0, distances=0, alpha=1, beta=1):
    """
    prior: Nx1 - list of probabilities for each theta
    thetas: NxN_FEAT - list of reward parameters to reason over
    demonstration: N_FEATx1 - featurized trajectory to reason about, sum of state feature counts
    trajectory_set - DxN_FEAT - all featurized trajectories which are optimal for 
                                some theta
    traj_len: scalar - actual length of demonstration for living cost
    trajectory_lens: Dx1 - actual length of each trajectory for living cost
    alpha: scalar - "exaggeration coeffiecient"
    beta: scalar - rationality coefficient
    returns P(theta | xi)
    """
    numerators = []
    for i, theta in enumerate(thetas):
        numerators.append(prob_trajectory_given_theta(demonstration, trajectory_set, traj_len, trajectory_lens, theta, dist, distances, alpha, beta) * prior[i])
    numerators = np.array(numerators)
    return numerators / np.sum(numerators)

# colors as usual: -1=black, 0=gray, 1=white
# start with single black square for 1D belief space
# grid = np.array([[0, -1,  0],
#                  [0,  0,  0],
#                  [0,  0,  0]])
# grid = np.array([[0, -1,  0,  0],
#                  [0,  0,  0,  0],
#                  [0,  0,  0,  0],
#                  [0,  0,  0,  0]])
grid = np.array([[0,  0,  0,  0,  0],
                 [0,  0,  0,  0,  0],
                 [0,  0,  0,  0,  0],
                 [0,  0,  0,  0,  0],
                 [0,  0, -1,  0,  0]])
dimension = 1

# start = (0, 2)
# goal = (0, 0)
start = (2, 0)
goal = (2, 4)
goal_reward = 2
env = Environment(grid=grid, start=start, goal=goal, living_reward=0)

start = ij_to_idx(start[0], start[1], grid.shape[1])
goal = ij_to_idx(goal[0], goal[1], grid.shape[1])

if dimension == 1:
    feature_map = featurize(grid, {-1: 0})
elif dimension == 2:
    feature_map = featurize(grid, {-1:0, 0:1})

if dimension == 1:
    thetas = np.linspace(-1, 1, 11)
    print thetas
elif dimension == 2:
    thetas = []
    for i in np.linspace(-1, 1, 10):
        for j in np.linspace(-1, 1, 10):
            thetas.append((i, j))

    xx, yy = np.mgrid[-1:1:10j, -1:1:10j]
    thetas = np.vstack([xx.ravel(), yy.ravel()]).T

trajectory_set = compute_trajectory_set_nx(grid, state_idx_to_ij(start, grid), state_idx_to_ij(goal, grid))
traj_set_featurized = np.array([sum([feature_map[ij_to_idx(s[0], s[1], grid.shape[0])] for s in traj]) \
                                                                          for traj in trajectory_set])
prior = np.ones(len(thetas)) / len(thetas)

demo1 = [(0, 2), (0, 1), (0, 0)]
demo2 = [(0, 2), (1, 2), (1, 1), (1, 0), (0, 0)]
demo3 = [(0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0), (0, 0)]

demo4 = [(0, 2), (0, 3), (1, 3), (2, 3), (3, 3), (3, 2), (3, 1), (3, 0), (2, 0), (1, 0), (0, 0)]
demo5 = [(0, 3), (1, 3), (2, 3), (2, 2), (2, 1), (2, 0), (1, 0), (0, 0)]
demo6 = [(0, 3), (1, 3), (1, 2), (1, 1), (1, 0), (0, 0)]

demo7 = [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4)]
demo8 = [(2, 0), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 4)]
demo9 = [(2, 0), (1, 0), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4)]
demo = demo9

alphas = np.linspace(0, 10, 12)
fig, axes = plt.subplots(nrows=4, ncols=3)
axes = np.array(axes).flatten()

demo_featurized = sum([feature_map[ij_to_idx(s[0], s[1], grid.shape[0])] for s in demo])
dist = np.average([dist_to_squares(i, j, [(4, 2)]) for i, j in demo])
print dist
distances_to_black = np.array([np.average([dist_to_squares(i, j, [(4, 2)]) for i, j in traj]) for traj in trajectory_set])
print distances_to_black

traj_len = len(demo)
trajectory_lens = np.array([len(traj) for traj in trajectory_set])

# shows final belief over theta for different values of alpha
for axes_idx, alpha in enumerate(alphas):
    posterior = update_distribution(prior, thetas, demo_featurized, traj_set_featurized, traj_len, trajectory_lens, dist, distances_to_black, alpha)
    
    ax = axes[axes_idx]
    if dimension == 1:
        entropy = -sum([p * np.log2(p) for p in posterior])

        ax.bar(thetas, posterior, 0.2)
        ax.set_ylim((0,1))
        ax.set_title(entropy)
    elif dimension == 2:
        f = np.reshape(posterior, xx.shape)
        cfset = ax.contourf(xx, yy, f, cmap='Greys')
        cset = ax.contour(xx, yy, f, colors='k')
        ax.clabel(cset, inline=1, fontsize=10)
        ax.set_xlabel("weight of black")
        ax.set_ylabel("living reward")
        plt.pause(0.1)

fig, ax = plt.subplots()
env.paths['path_0'] = demo
env.show_all_paths(ax)
plt.show()
1/0

# find probability of each trajctory given ground truth
theta = -1

fig, axes = plt.subplots(nrows=4, ncols=3)
axes = np.array(axes).flatten()

for i, traj in enumerate(traj_set_featurized):
    ax = axes[i]
    env.show_grid(ax)
    env.paths['path_' + str(i)] = trajectory_set[i]
    env.show_path(ax, i)
    traj_len = trajectory_lens[i]
    dist = distances_to_black[i]
    trajectory_reward = (np.dot(traj, theta) - 0.6*(traj_len-1))
    # def prob_trajectory_given_theta(trajectory, trajectory_set, traj_len, trajectory_lens, theta, dist=0, distances=0, alpha=1, beta=1):
    prob = prob_trajectory_given_theta(traj, traj_set_featurized, traj_len, trajectory_lens, theta, dist, distances_to_black, alpha=0)
    ax.set_title("Reward: " + str(trajectory_reward) + " Likelihood: " + str(prob))
plt.show()
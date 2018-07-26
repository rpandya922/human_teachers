from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pickle
import argparse
from environment import Environment
from utils import *

##########################################################################################################################################
# reasoning over optimal vs exaggerated trajectories in 1d belief, see if it results in better learning than assuming 
# either one individually
##########################################################################################################################################

parser = argparse.ArgumentParser()
parser.add_argument('--entropy', action='store_true')
args = parser.parse_args()

living_reward = -0.1
reason_over_entropy = args.entropy
alpha = 5
beta = 1
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
    return np.sum(np.exp(beta * (trajectory_set.dot(theta) + living_reward*trajectory_lens) - (alpha * (theta * distances))))
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
    return np.exp(beta * (np.dot(trajectory, theta) + living_reward*traj_len) - (alpha * (theta * dist))) / \
           partition_function(trajectory_set, trajectory_lens, theta, distances, alpha, beta)

# colors as usual: -1=black, 0=gray, 1=white
# start with single black square for 1D belief space
grid = np.array([[0,  0,  0,  0,  0],
                 [0,  0,  0,  0,  0],
                 [0,  0,  0,  0,  0],
                 [0,  0, -1,  0,  0],
                 [0,  0, -1,  0,  0]])
dimension = 1

start = (2, 0)
goal = (2, 4)
goal_reward = 2
env = Environment(grid=grid, start=start, goal=goal, living_reward=living_reward)

start = ij_to_idx(start[0], start[1], grid.shape[1])
goal = ij_to_idx(goal[0], goal[1], grid.shape[1])

if dimension == 1:
    feature_map = featurize(grid, {-1: 0})
if dimension == 1:
    thetas = np.linspace(-1, 1, 11)

trajectory_set = compute_trajectory_set_nx(grid, state_idx_to_ij(start, grid), state_idx_to_ij(goal, grid))
traj_set_featurized = np.array([sum([feature_map[ij_to_idx(s[0], s[1], grid.shape[0])] for s in traj]) \
                                                                          for traj in trajectory_set])
prior = np.ones(len(thetas)) / len(thetas)

demo1 = [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4)]
demo2 = [(2, 0), (1, 0), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4)]
demos = [demo1, demo2]
possible_strategies = ["exaggerate", "optimal"]

if reason_over_entropy:
    prior = np.ones(len(thetas)) / len(thetas)

    for demo_idx, demo in enumerate(demos):
        demo_featurized = sum([feature_map[ij_to_idx(s[0], s[1], grid.shape[0])] for s in demo])
        dist = np.average([dist_to_squares(i, j, [(4, 2)]) for i, j in demo])
        distances_to_black = np.array([np.average([dist_to_squares(i, j, [(4, 2)]) for i, j in traj]) for traj in trajectory_set])

        traj_len = len(demo)
        trajectory_lens = np.array([len(traj) for traj in trajectory_set])

        numerators = [[] for _ in possible_strategies]
        for i, theta in enumerate(thetas):
            for s_idx, strategy in enumerate(possible_strategies):
                if strategy == "optimal":
                    numerators[s_idx].append(prob_trajectory_given_theta(demo_featurized, traj_set_featurized, traj_len, trajectory_lens, theta, 0, 0, alpha, beta) * prior[i])
                elif strategy == "exaggerate":
                    numerators[s_idx].append(prob_trajectory_given_theta(demo_featurized, traj_set_featurized, traj_len, trajectory_lens, theta, dist, distances_to_black, alpha, beta) * prior[i])
        denominators = np.sum(numerators, axis=1)
        numerators = np.array(numerators)[:,:,0]
        posteriors = np.array(numerators) / denominators

        entropies = [-sum([p * np.log2(p) for p in posterior]) for posterior in posteriors]        
        prior = posteriors[np.argmin(entropies)]
else:
    # given/assumed strategies for the two demonstrations
    strategies = ["optimal", "exaggerate"]
    prior = np.ones(len(thetas)) / len(thetas)

    for demo_idx, demo in enumerate(demos):
        strategy = strategies[demo_idx]

        demo_featurized = sum([feature_map[ij_to_idx(s[0], s[1], grid.shape[0])] for s in demo])
        dist = np.average([dist_to_squares(i, j, [(4, 2)]) for i, j in demo])
        distances_to_black = np.array([np.average([dist_to_squares(i, j, [(4, 2)]) for i, j in traj]) for traj in trajectory_set])

        traj_len = len(demo)
        trajectory_lens = np.array([len(traj) for traj in trajectory_set])

        numerators = []
        for i, theta in enumerate(thetas):
            if strategy == "optimal":
                numerators.append(prob_trajectory_given_theta(demo_featurized, traj_set_featurized, traj_len, trajectory_lens, theta, 0, 0, alpha, beta) * prior[i])
            elif strategy == "exaggerate":
                numerators.append(prob_trajectory_given_theta(demo_featurized, traj_set_featurized, traj_len, trajectory_lens, theta, dist, distances_to_black, alpha, beta) * prior[i])
        numerators = np.array(numerators)
        prior = numerators / np.sum(numerators)

print prior

fig, ax = plt.subplots()
ax.bar(thetas, prior, width=0.2)
ax.set_ylim((0, 1))

fig, ax = plt.subplots()
env.paths['path_0'] = demo1
env.paths['path_1'] = demo2
env.show_all_paths(ax)
plt.show()

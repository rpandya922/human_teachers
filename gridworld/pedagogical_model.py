from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pickle
from tqdm import tqdm
from environment import Environment
from utils import *
from dummy_file import compute
np.random.seed(0)

def featurize(grid, feature_idxs):
    """
    grid: 10x10 color grid, colors are -1, -0.5, 0, 0.5, 1
    feature_idxs: dictionary, maps colors to feature index 
        {-1:0, -0.5:1,...}
    returns list of featurized states: last feature of each state is 1
        so that we can use dot product for learning living reward
    """
    feature_map = []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            color = grid[i, j]
            features = np.zeros(len(feature_idxs))
            if color in feature_idxs.keys():
                features[feature_idxs[color]] += 1
            feature_map.append(np.hstack((features, [1])))
    return np.array(feature_map)
def get_valid_neighbors(i, j, grid, row_idxs, col_idxs):
    i_idx = row_idxs.index(i)
    j_idx = col_idxs.index(j)

    neighbor_idxs = [(i_idx+1, j_idx), (i_idx-1,j_idx), (i_idx,j_idx+1), (i_idx,j_idx-1)]
    neighbors = []
    for i1, j1 in neighbor_idxs:
        if not (i1 >= 0 and i1 < len(row_idxs)):
            continue
        if not (j1 >= 0 and j1 < len(col_idxs)):
            continue
        neighbors.append((row_idxs[i1], col_idxs[j1]))
    return neighbors
def compute_trajectory_set_nx(grid, start, goal):
    G = nx.Graph()
    G.add_node(start)
    G.add_node(goal)

    # default
    col_idxs = list(range(grid.shape[0]))
    row_idxs = list(range(grid.shape[1]))

    # default 10x10
    # col_idxs = [0, 2, 4, 6, 8, 9]
    # row_idxs = [0, 2, 4, 5, 7, 9]

    # for grid 3 and grid 15
    # col_idxs = [0, 2, 3, 5, 6, 7]
    # row_idxs = [0, 2, 3, 4, 5, 6]

    for i in row_idxs:
        for j in col_idxs:
            G.add_node((i, j))
    for i in row_idxs:
        for j in col_idxs:
            neighbors = get_valid_neighbors(i, j, grid, row_idxs, col_idxs)
            for n in neighbors:
                G.add_edge((i, j), n)
    return list(nx.all_simple_paths(G, start, goal))
def partial_traj_to_features(partial, feature_map, grid, include_living_cost=False):
    features = np.zeros(feature_map.shape[1])

    i1, j1 = partial[0]
    traj_len = 0
    for (i2, j2) in partial[1:]:
        if abs(i1 - i2) == 2 and j1 - j2 == 0:
            # need to add feature for in between state
            features += feature_map[ij_to_idx(int((i1+i2)/2), j1, grid.shape[0])]
            traj_len += 1
        elif i1 - i2 == 0 and abs(j1 - j2) == 2:
            features += feature_map[ij_to_idx(i1, int((j1+j2)/2), grid.shape[0])]
            traj_len += 1
        features += feature_map[ij_to_idx(i2, j2, grid.shape[0])]
        traj_len += 1
        i1, j1 = i2, j2
    if include_living_cost:
        features = np.hstack((features, [0]))
        features[-1] = traj_len
    return features
def partition_function(trajectory_set, theta, beta=1):
    """
    trajectory_set -DxN_FEAT - all featurized trajectories which are optimal for 
                                some theta
    trajectory_lens: Dx1 - actual length of each trajectory for living cost
    theta: N_FEATx1 - current reward parameters to reason over
    beta: scalar - rationality coefficient
    """
    return np.sum(np.exp(beta * trajectory_set.dot(theta)))
def prob_trajectory_given_theta(trajectory, trajectory_set, theta, beta=1):
    """
    trajectory: N_FEATx1 - featurized trajectory to reason about, sum of state feature counts
    theta: N_FEATx1 - current reward parameters to reason over
    trajectory_set: DxN_FEAT - all featurized trajectories
    traj_len: scalar - actual length of demonstration for living cost
    trajectory_lens: Dx1 - actual length of each trajectory for living cost
    beta: scalar - rationality coefficient
    returns P(xi | theta)
    """
    return np.exp(beta * np.dot(trajectory, theta)) / partition_function(trajectory_set, theta, beta)

# features will be: [black, white, living_reward]
ground_truth = np.array([-1, 1, -1])
ground_truth = ground_truth / np.linalg.norm(ground_truth)

# file_name = "./data/mturk_6_21_18/parsed_envs.pkl"
# f = open(file_name, "rb")
# envs = pickle.load(f)['envs']
# f.close()

# env = envs[10]
# grid = np.array(env.grid)
# start = env.start
# goal = env.goal
# living_reward = env.living_reward
grid = np.array([[0,  0,  0,  0,  0],
                 [0, -1, -1,  0,  0],
                 [0,  1,  1,  0,  0],
                 [0,  1,  1,  0,  0],
                 [0,  0,  0,  0,  0]])
start = (0, 0)
goal = (0, 3)
living_reward = -1

trajectory_set = compute_trajectory_set_nx(grid, start, goal)
idxs_to_keep = np.random.choice(len(trajectory_set), size=1000)
trajectory_set = np.array(trajectory_set)[idxs_to_keep]
feature_map = featurize(grid, {-1:0, 1:1})
# traj_set_featurized = np.array([sum([feature_map[ij_to_idx(s[0], s[1], grid.shape[0])] for s in traj]) \
#                                                                           for traj in trajectory_set])
traj_set_featurized = np.array([partial_traj_to_features(traj, feature_map, grid) for traj in trajectory_set])
thetas = []
for i in np.linspace(-1, 1, 5):
    for j in np.linspace(-1, 1, 5):
        for k in np.linspace(-1, 1, 5):
            thetas.append((i, j, k))
thetas = np.array(thetas)
norms = np.linalg.norm(thetas, axis=1)[:,np.newaxis]
norms[norms == 0] = 1

thetas = thetas / norms
prior = np.ones(len(thetas)) / len(thetas)

#####################################################################################
# TIMING TESTING
# p_show = []
# for traj in tqdm(traj_set_featurized):
#     num, denom = compute(traj, traj_set_featurized, ground_truth, thetas)

#     # computes sum over all theta P(xi | theta)
#     p_obs_denom = np.sum(num / denom)
#     # computes P(xi | ground truth)
#     p_obs_num = prob_trajectory_given_theta(traj, traj_set_featurized, ground_truth)

#     # computes P(ground truth | xi)
#     p_obs = p_obs_num / p_obs_denom
#     p_show.append(p_obs)
# # computes P(xi | ground truth) for all xi
# p_show = p_show / np.sum(p_show)

# all_best = np.argwhere(p_show == np.amax(p_show)).flatten()
# FINDING: np.exp is the real culprit: not sure how to do any faster
#####################################################################################

# uncomment for real running
# ultimate goal: find most pedagogical example; highest P(xi|ground truth)
p_show = []
for traj in tqdm(traj_set_featurized):
    # xi = current traj, phi(xi) = featurized trajectory
    # computes exp(phi(xi)^T theta) for all thetas
    num = np.exp(thetas.dot(traj))

    # computes sum over all xi exp(phi(xi)^T theta) for all thetas
    denom = np.exp(traj_set_featurized.dot(thetas.T))
    denom = np.sum(denom, axis=0)

    # computes sum over all theta P(xi | theta)
    p_obs_denom = np.sum(num / denom)
    # computes P(xi | ground truth)
    p_obs_num = prob_trajectory_given_theta(traj, traj_set_featurized, ground_truth)

    # computes P(ground truth | xi)
    p_obs = p_obs_num / p_obs_denom
    p_show.append(p_obs)
# computes P(xi | ground truth) for all xi
p_show = p_show / np.sum(p_show)

all_best = np.argwhere(p_show == np.amax(p_show)).flatten()

env = Environment(grid, start, goal, living_reward=living_reward)
fig, ax = plt.subplots()
for i, idx in enumerate(all_best):
    path = trajectory_set[idx]
    env.paths['path_' + str(i)] = path
    print traj_set_featurized[idx]
env.show_all_paths(ax)
plt.show()
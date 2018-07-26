from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import pickle
import math
from environment import Environment

def ij_to_idx(i, j, n): return (i * n) + j
def idx_to_ij(idx, grid=np.zeros((10,10))):
    m = grid.shape[0]
    n = grid.shape[1]
    i = math.floor(idx / m)
    j = idx % n
    return (i, j)
def states_to_action(state1, state2):
    i1, j1 = idx_to_ij(state1)
    i2, j2 = idx_to_ij(state2)
    if i1 == i2 and j2 == j1 + 1:
        return 0
    elif j1 == j2 and i2 == i1 - 1:
        return 1
    elif i1 == i2 and j2 == j1 - 1:
        return 2
    elif j1 == j2 and i2 == i1 + 1:
        return 3
    return None
def create_transitions(grid):
    """
    grid: MxN grid of color indices
    """
    M = grid.shape[0]
    N = grid.shape[1]
    N_STATES = M * N
    N_ACTIONS = 4
    # transitions[s, s1, a] = prob of landing in s1 when taking action a from s
    transitions = np.zeros((N_STATES, N_STATES, N_ACTIONS))

    for s in range(N_STATES):
        for s1 in range(N_STATES):
            for a in range(N_ACTIONS):
                i, j = idx_to_ij(s, grid)
                i1, j1 = idx_to_ij(s1, grid)
                if a == 0:
                    # going right, not at right edge
                    if i == i1 and j < grid.shape[1] - 1 and j1 == j + 1:
                        transitions[s, s1, a] = 1
                elif a == 1:
                    # going up, not at top
                    if j == j1 and i > 0 and i1 == i - 1:
                        transitions[s, s1, a] = 1
                elif a == 2:
                    # going left, not at left edge
                    if i == i1 and j > 0 and j1 == j -1:
                        transitions[s, s1, a] = 1
                elif a == 3:
                    # going down, not at bottom
                    if j == j1 and i < grid.shape[0] - 1 and i1 == i + 1:
                        transitions[s, s1, a] = 1
    return transitions
def featurize(grid, feature_idxs):
    """
    grid: 10x10 color grid, example colors are -1, -0.5, 0, 0.5, 1
    feature_idxs: dictionary, maps colors to feature index 
        {-1:0, -0.5:1,...}
    returns list of featurized states
    """
    feature_map = []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            color = grid[i, j]
            features = np.zeros(len(feature_idxs))
            if color in feature_idxs.keys():
                features[feature_idxs[color]] += 1
            feature_map.append(features)
    return np.array(feature_map)
def value_iteration(transitions, rewards, gamma, threshold):
    """
    transition: NxNxN_ACTIONS - transition dynamics
    rewards: Nx1 - state rewards
    gamma: discount factor
    threshold: threshold for stopping
    returns stochastic optimal policy, all optimal actions listed at each state
    """
    N, _, N_ACTIONS = transitions.shape
    values = np.zeros((N))

    finished = False
    while not finished:
        values_copy = values.copy()
        for s in range(N):
            values[s] = max([sum([transitions[s, s1, a]*(rewards[s] + gamma*values_copy[s1]) 
                                for s1 in range(N)]) 
                                for a in range(N_ACTIONS)])
        if (np.abs(values - values_copy) < threshold).all():
            finished = True
    # stores all equally optimal actions in an array at each state
    stochastic_policy = [0 for _ in range(N)]
    for s in range(N):
        actions = [sum([transitions[s, s1, a]*(rewards[s] + gamma*values[s1])
                               for s1 in range(N)])
                               for a in range(N_ACTIONS)]
        best_actions = np.argwhere(actions == np.amax(actions)).flatten()
        stochastic_policy[s] = best_actions
    return stochastic_policy
def percent_suboptimal(policy, path):
    """
    policy: Nx1 - maps states to list of all optimal actions
    path: Nx1 - list of states by index
    returns percentage of time action on path doesn't match policy
    """
    times_suboptimal = 0
    for i in range(len(path) - 1):
        j = i + 1
        loc1 = int(path[i])
        loc2 = int(path[j])
        action_taken = states_to_action(loc1, loc2)
        if action_taken not in policy[loc1]:
            times_suboptimal += 1
    return times_suboptimal / (len(path) - 1)
file_name = './data/mturk_6_21_18/parsed_envs.pkl'
f = open(file_name, "rb")
envs = pickle.load(f)['envs']
f.close()

fig, axes = plt.subplots(nrows=4, ncols=4)
axes = np.array(axes).flatten()

all_suboptimality = [[] for _ in range(len(envs))]

for env_idx, env in enumerate(envs):
    ax = axes[env_idx]
    env.show_all_paths(ax)
    grid = np.array(env.grid)
    ground_truth = np.array(env.true_rewards)
    transitions = create_transitions(grid)
    feature_idxs_dict = {}
    for i, r in enumerate(ground_truth):
        feature_idxs_dict[r] = i
    feature_map = featurize(grid, feature_idxs_dict)
    goal = ij_to_idx(env.goal[0], env.goal[1], 10)

    rewards = feature_map.dot(ground_truth)
    rewards[goal] = 10
    gamma = 0.95
    threshold = 0.01

    optimal_policy = value_iteration(transitions, rewards, gamma, threshold)
    
    for i in range(len(env.paths)):
        env.show_path(ax, i)
        path = env.paths['path_' + str(i)]
        idx_path = [ij_to_idx(i,j,10) for (i, j) in path]
        subopt = percent_suboptimal(optimal_policy, idx_path)
        all_suboptimality[env_idx].append(subopt)
avg_subopt_per_env = np.average(np.array(all_suboptimality), axis=1)
avg_subopt_per_user = np.average(np.array(all_suboptimality), axis=0)
avg_subopt = np.average(np.array(all_suboptimality))
print avg_subopt_per_env
print avg_subopt_per_user
print avg_subopt
plt.show()
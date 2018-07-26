from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from grid import GridWorld
import math
from environment import Environment

def plot_cost_function(costs, grid, title=''):
    costs = np.array(costs) / np.linalg.norm(costs)
    grid_copy = np.copy(grid).astype(float)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] != 0:
                # colors are 1-indexed, 0 means white space
                grid_copy[i, j] = costs[grid[i, j] - 1]
    fig, ax = plt.subplots()
    # cmap = colors.ListedColormap(['xkcd:white', 'xkcd:light red', 'xkcd:red', 'xkcd:dark red'])
    # bounds = sorted(costs)
    # b1 = (bounds[0] - 1.1)
    # b2 = (bounds[0] - 1 + bounds[0]) / 2
    # b3 = (bounds[0] + bounds[1]) / 2
    # b4 = (bounds[1] + bounds[2]) / 2
    # b5 = bounds[2] + 0.1
    # bounds = [b1, b2, b3, b4, b5]
    # norm = colors.BoundaryNorm(bounds, cmap.N)
    ax.set_title(title)
    cax = ax.imshow(grid_copy, cmap='Greys')
    cbar = fig.colorbar(cax)
    ax.grid(axis='both', linestyle='-', color='k', linewidth=2)
    ax.set_xticks(np.arange(-0.5, 4.5, 1))
    ax.set_yticks(np.arange(-0.5, 4.5, 1))
def plot_demonstrations(demonstrations, grid, costs, goal_location):
    gridworld = GridWorld(grid, costs, goal_location)
    gridworld.plot_grid()
    ax = gridworld.ax
    ax.set_title('Demonstrations')
    for trajectory in demonstrations:
        points = []
        for t in trajectory:
            points.append(t[0])
        points.append(trajectory[-1][-1])
        points = np.array(points)
        ax.plot(points[:,1], points[:,0], c='k', linestyle='--')

def next_state_from_action_idx(state, a):
    i, j = state
    if a == 0:
       j += 1
    elif a == 1:
        i -= 1
    elif a == 2:
        j -= 1
    elif a == 3:
        i += 1
    return i, j
def is_valid(i, j, grid):
    if i < 0 or i >= grid.shape[0] or j < 0 or j >= grid.shape[1]:
        return False
    return True
def get_valid_neighbors(i, j, grid):
    all_neighbors = [(i+1, j), (i-1,j), (i,j+1), (i,j-1)]
    return [(i,j) for (i,j) in all_neighbors if is_valid(i,j,grid)]
def get_valid_actions(i, j, grid):
    valid = []
    if i != 0:
        valid.append(1)
    if i != grid.shape[0]:
        valid.append(3)
    if j != 0:
        valid.append(2)
    if j != grid.shape[1]:
        valid.append(0)
    return valid
def reward(state, action, s_prime, grid, living_reward):
    # state, s_prime: (i, j)
    # action: [0, 1, 2, 3] = [right, up, left, down]
    # if s_prime in get_valid_neighbors(state[0], state[1], grid):
    return grid[s_prime] + living_reward
def vi_optimal_trajectory(env, theta, style=None):
    grid = np.array(env.grid)
    start = tuple(env.start)
    goal = tuple(env.goal)
    threshold = 0.001
    gamma = 0.881111111111
    living_reward = env.living_reward
    goal_value = 7

    color_to_reward = {-1:theta[0], -0.5:theta[1], 0:theta[2], 0.5:theta[3], 1:theta[4]}

    if style is not None:
        all_reward_locs = []
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                if grid[(i, j)] != 0:
                    all_reward_locs.append((i, j))
        alpha = 1
        style_grid = np.zeros(grid.shape)
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                r = np.average([color_to_reward[grid[r]] * (np.sqrt((i - r[0])**2 + (j - r[1])**2)) for r in all_reward_locs])
                style_grid[i,j] = -alpha * r

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            grid[i,j] = color_to_reward[grid[i,j]]
    if style is not None:
        grid += style_grid
    grid[goal] = goal_value

    value_function_prev = np.zeros(grid.shape)
    value_function = np.zeros(grid.shape)
    finished = False

    while not finished:
        value_function_prev = np.copy(value_function)
        value_function = np.zeros(grid.shape)
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                s = (i, j)
                vals = []
                for a in list(range(4)):
                    # sums over all s', but deterministic so only one
                    n = next_state_from_action_idx(s, a)
                    if is_valid(n[0], n[1], grid):
                        vals.append(reward(s, a, n, grid, living_reward) + (gamma * value_function_prev[n]))
                    # else:
                    #     vals.append(reward(s, a, s) + (gamma * value_function_prev[s]))
                value_function[s] = max(vals)

        if (np.abs(value_function - value_function_prev) < threshold).all():
            finished = True
    policy = np.zeros(grid.shape)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            s = (i, j)
            vals = []
            for a in list(range(4)):
                # sums over all s', but deterministic so only one
                n = next_state_from_action_idx(s, a)
                if is_valid(n[0], n[1], grid):
                    vals.append(reward(s, a, n, grid, living_reward) + (gamma * value_function[n]))
                else:
                    vals.append(float('-inf'))
            action = np.argmax(vals)
            policy[i,j] = action

    path = [start]
    loc = start
    seen = set(start)
    while loc != goal:
        action = policy[loc]
        loc = next_state_from_action_idx(loc, action)
        if loc in seen:
            print "Optimal trajectory does not reach goal"
            break
        path.append(loc)
        seen.add(loc)
    return path

def ij_to_idx(i, j, n): return (i * n) + j
def path_to_ij(m, n, path):
    # path: list of indices in 2D array
    # n, m: dimensions of array
    ij_path = []
    for idx in path:
        i = math.floor(idx / m) + np.random.uniform(-0.1, 0.1)
        j = idx % n + np.random.uniform(-0.1, 0.1)
        ij_path.append([i, j])
    return np.array(ij_path)
def state_idx_to_ij(idx, grid):
    """
    idx: 0-MxN index of grid
    grid: MxN array
    """
    i = math.floor(idx / grid.shape[0])
    j = idx % grid.shape[1]
    return int(i), int(j)
def next_state_from_action(state, a, grid):
    i, j = state_idx_to_ij(state, grid)
    m, n = grid.shape
    if a == 0 and j != n-1:
       j += 1
    elif a == 1 and i != 0:
        i -= 1
    elif a == 2 and j != 0:
        j -= 1
    elif a == 3 and i != m-1:
        i += 1
    return (i * n) + j
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
                i, j = state_idx_to_ij(s, grid)
                i1, j1 = state_idx_to_ij(s1, grid)
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
    grid: 10x10 color grid, colors are -1, -0.5, 0, 0.5, 1
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
def value_iteration(transitions, rewards, goal, gamma, threshold):
    """
    transition: NxNxN_ACTIONS - transition dynamics
    rewards: Nx1 - state rewards
    goal: terminal state in MDP, set policy here as -1: no action
    gamma: discount factor
    threshold: threshold for stopping
    returns optimal policy
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
    policy = np.zeros([N])
    for s in range(N):
        policy[s] = np.argmax([sum([transitions[s, s1, a]*(rewards[s] + gamma*values[s1])
                               for s1 in range(N)])
                               for a in range(N_ACTIONS)])
    policy[goal] = -1 # goal is terminal state, don't take more actions from here
    return policy
def feature_counts(policy, feature_map, state, action=None, gamma=1):
    """
    policy: Nx1 - mapping of state to optimal action
    feature_map: NxN_FEATURES - list of features per state
    state: start state
    action: action to take from state 

    returns: feature counts from taking given action from given state
             to the goal state
    """
    N, N_FEATURES = feature_map.shape

    if action is None:
        action = policy[state]

    feature_counts = np.zeros(N_FEATURES)
    grid_size = (int(np.sqrt(N)), int(np.sqrt(N)))
    dummy_grid = np.zeros(grid_size)
    # while not at terminal state
    i = 0
    while policy[state] != -1:
        feature_counts += np.power(gamma, i) * feature_map[state]
        next_state = int(next_state_from_action(state, action, dummy_grid))
        state = next_state
        action = int(policy[state])
        i += 1
    return feature_counts

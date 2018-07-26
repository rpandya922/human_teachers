from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import pickle
from environment import Environment
import math
np.set_printoptions(precision=2)
file_name = "./data/environments.pkl"
f = open(file_name, "rb")
envs = pickle.load(f)
f.close()

env = envs['env_14']
env.grid = np.array(env.grid)
grid = env.grid

# defines color index based on current color values (-1, -0.5, 0, 0.5, 1)
color_idxs = {-1:0, -0.5:1, 0:2, 0.5:3, 1:4, 7:2}
GOAL_VALUE = 7
NUM_FEATURES = 5
N_STATES = grid.shape[0] * grid.shape[1]
gamma = 0.81
threshold = 0.001

def state_idx_to_ij(idx):
    i = math.floor(idx / grid.shape[0])
    j = idx % grid.shape[1]
    return (i, j)
def make_state(i, j): return (int(i), int(j), color_idxs[grid[int(i), int(j)]])
def get_neighboring_action_state_pairs(state):
    """
    state: (i, j, color), color: [0-4]
    """
    i, j = state[0], state[1]
    neighbors = []
    if i > 0:
        # up
        neighbors.append((1, make_state(i-1, j)))
    if i < grid.shape[0] - 1:
        # down
        neighbors.append((3, make_state(i+1, j)))
    if j > 0:
        # left
        neighbors.append((2, make_state(i, j-1)))
    if j < grid.shape[1] - 1:
        # right
        neighbors.append((0, make_state(i, j+1)))
    # return list of (action, s_prime)
    return neighbors
def get_neighboring_states(state):
    """
    state: (i, j, color), color: [0-4]
    """
    neighbors = []
    if i > 0:
        # up
        neighbors.append(make_state(i-1, j))
    if i < grid.shape[0] - 1:
        # down
        neighbors.append(make_state(i+1, j))
    if j > 0:
        # left
        neighbors.append(make_state(i, j-1))
    if j < grid.shape[1] - 1:
        # right
        neighbors.append(make_state(i, j+1))
    return neighbors
def is_valid(state, action):
    i, j = state[0], state[1]
    if i == 0 and action == 1:
        # top row, going up
        return False
    if i == grid.shape[0] - 1 and action == 3:
        # bottom row going down
        return False
    if j == 0 and action == 2:
        # left column going left
        return False
    if j == grid.shape[1] - 1 and action == 0:
        # right column, going right
        return False
    return True
def get_next_state(state, action):
    """
    state: (i, j, color), color: [0-4]
    action: [0-3]
    """
    if is_valid(state, action):
        if action == 0:
            return make_state(state[0], state[1] + 1)
        elif action == 1:
            return make_state(state[0] - 1, state[1])
        elif action == 2:
            return make_state(state[0], state[1] - 1)
        elif action == 3:
            return make_state(state[0] + 1, state[1])
    return state
def get_transition_prob(state, action, s_prime):
    """
    state, s_prime: (i, j, color), color: [0-4]
    action: [0-3] (right, up, left, down)
    """
    if (action, s_prime) in get_neighboring_action_state_pairs(state):
        return 1
    return 0
def featurized(state):
    """
    state: (i, j, color), color: [0-4]
    returns 1-hot color index
    """
    features = np.zeros(NUM_FEATURES)
    features[state[2]] = 1
    return features
def reward(state, theta):
    """
    state: (i, j, color), color: [0-4]
    theta: NUM_FEATURESx1, reward weights
    """
    features = featurized(state)
    return features.dot(theta)
def get_optimal_policy(theta, grid):
    """
    theta: NUM_FEATURESx1, reward weights
    """
    grid[env.goal] = GOAL_VALUE

    value_function_prev = np.zeros(grid.shape)
    value_function = np.zeros(grid.shape)
    finished = False

    while not finished:
        value_function_prev = np.copy(value_function)
        value_function = np.zeros(grid.shape)
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                s = make_state(i, j)
                vals = []
                for a in list(range(4)):
                    # sums over all s', but deterministic so only one
                    if is_valid(s, a):
                        n = get_next_state(s, a)
                        vals.append(reward(n, theta) + (gamma * value_function_prev[n[0], n[1]]))
                value_function[s[0], s[1]] = max(vals)
        if (np.abs(value_function - value_function_prev) < threshold).all():
            finished = True

    policy = np.zeros(grid.shape)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            s = make_state(i, j)
            vals = []
            for a in list(range(4)):
                # sums over all s', but deterministic so only one
                if is_valid(s, a):
                    n = get_next_state(s, a)
                    vals.append(reward(n, theta) + (gamma * value_function[n[0], n[1]]))
                else:
                    vals.append(float('-inf'))
            action = np.argmax(vals)
            policy[s[0], s[1]] = action
    return policy

demonstration = env.paths['path_2']
fig, ax = plt.subplots()
env.show_all_paths(ax)
plt.pause(0.01)
T = len(demonstration)
demo_features = sum([featurized(make_state(*s)) for s in demonstration])
#initialize
s = make_state(env.goal[0], env.goal[1])
z_s = 1
theta = [0, 0, 0, 0, 0]
alpha = 0.01
num_iters = 20
for iteration in range(num_iters):
    mu = np.zeros((N_STATES, T))
    i, j = demonstration[0]
    s_idx = (i * grid.shape[1]) + j
    mu[s_idx, 0] = 1
    current_policy = get_optimal_policy(theta, grid)
    for s in range(N_STATES):
        for t in range(T-1):
            probs = []
            for pre_s in range(N_STATES):
                pre_state = make_state(*state_idx_to_ij(pre_s))
                optimal_a = current_policy[pre_state[0], pre_state[1]]
                probs.append(mu[pre_s, t] * get_transition_prob(pre_state, optimal_a, make_state(*state_idx_to_ij(s))))
            mu[s, t+1] = sum(probs)
    # state visitation frequencies
    svf = np.sum(mu, 1) # N_STATESx1

    gradient = demo_features - sum([svf[s] * featurized(make_state(*state_idx_to_ij(s))) for s in range(N_STATES)])
    theta += alpha * gradient
    print theta
plt.show()
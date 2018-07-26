from __future__ import division
import numpy as np
import pickle
import math
from environment import Environment
np.set_printoptions(precision=2)
def value_iteration(transitions, rewards, gamma, threshold):
    """
    transition: NxNxN_ACTIONS - transition dynamics
    rewards: Nx1 - state rewards
    gamma: discount factor
    threshold: threshold for stopping
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
    return policy
def backward_pass(transitions, rewards, demos):
    """
    transitions: NxNxN_ACTIONS - transition dynamics
    rewards: Nx1 - state rewards
    demos: list of lists of states
    """
    N, _, N_ACTIONS = transitions.shape
    T = len(demos[0])
    partition = np.zeros((N, T))
    partition[:,0] = 1
    
    for t in range(1, T):
        for s in range(N):
            partials = []
            # sums over possible end states for action, but deterministic
            for a in range(N_ACTIONS):
                for s1 in range(N):
                    partials.append(transitions[s, s1, a] * np.exp(rewards[s]) * partition[s1, t-1])
            partition[s, t] = sum(partials)
    return partition
def forward_pass(transitions, rewards, demos):
    """
    transitions: NxNxN_ACTIONS - transition dynamics
    rewards: Nx1 - state rewards    
    demos: list of lists of states
    """
    N, _, N_ACTIONS = transitions.shape

    # partition: NxT, partition function approximation
    partition = backward_pass(transitions, rewards, demos)
    
    T = len(demos[0])
    svf = np.zeros((N, T))
    for demo in demos:
        svf[demos[0], 0] += 1
    svf[:,0] = svf[:,0] / len(demos)
    
    for t in range(1, T):
        for s in range(N):
            partials = []
            for a in range(N_ACTIONS):
                P_a = sum([transitions[s, s1, a] * np.exp(rewards[s]) * partition[s1, T-2] 
                           for s1 in range(N)]) / partition[s, T-1]
                for s1 in range(N_ACTIONS):
                    partials.append(svf[s1, t-1] * P_a * transitions[s, s1, a])
            svf[s, t] = sum(partials)
    return np.sum(svf, axis=1)
def compute_state_visitation_freq(transitions, demos, policy):
    """
    transitions: NxNxN_ACTIONS - transition dynamics
    demos: list of demonstrations (each is list of states)
    policy: Nx1 
    """
    N, _, N_ACTIONS = transitions.shape
    T = len(demos[0])
    expected_svf = np.zeros([N, T])

    for demo in demos:
        expected_svf[demo[0], 0] += 1
    expected_svf[:,0] = expected_svf[:,0] / len(demos)

    for s in range(N):
        for t in range(T-1):
            expected_svf[s, t+1] = sum([expected_svf[pre_s, t] * transitions[pre_s, s, int(policy[pre_s])] 
                                        for pre_s in range(N)])
    return np.sum(expected_svf, 1)
def maxent_irl(feature_map, transitions, gamma, demos, alpha, n_iters):
    """
    feature_map: NxD - features for each state
    transitions: NxNxN_ACTIONS - transitions[s0, s1, a] = prob of landing
                                 in state s1 from taking action a in s0
    gamma: discount factor
    demos: list of demonstrations
    alpha: learning rate
    n_iters: # iterations for learning
    """
    N, _, N_ACTIONS = transitions.shape
    theta = np.ones(feature_map.shape[1])/5

    feat_exp = np.zeros([feature_map.shape[1]])
    for demo in demos:
        for step in demo:
            feat_exp += feature_map[step,:]
    feat_exp = feat_exp / len(demos)

    # black_squares = get_color_squares(grid, -1)
    # distances = []
    # for s in range(N):
    #     i, j = state_idx_to_ij(s, grid)
    #     distances.append(dist_to_black(i, j, black_squares))
    # distances = np.array(distances)
    for iteration in range(n_iters):
        rewards = np.dot(feature_map, theta) - 1.1
        # rewards = np.dot(feature_map[:,:-1], theta[:-1])
        # rewards += -distances * theta[0]

        policy = value_iteration(transitions, rewards, gamma, 0.001)
        svf = compute_state_visitation_freq(transitions, demos, policy)
        print policy.reshape((10,10))
        # svf = forward_pass(transitions, rewards, demos)
        # print svf.reshape((10,10))
        gradient = feat_exp - feature_map.T.dot(svf)
        theta += alpha * gradient
        # print np.reshape(policy, (10,10))
        print theta
    rewards = np.dot(feature_map, theta)
    return theta
def get_color_squares(grid, color):
    """
    grid: MxN array, value at (i,j) specifies color
    color: -1, -0.5, 0, 0.5, 1 -> black, dark gray, gray, light gray, white
    """
    locations = []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == color:
                locations.append((i, j))
    return locations
def dist_to_black(i, j, black_squares):
    """
    (i, j): grid location
    black_squares: list of (i, j) locations of black squares
    """
    return np.average([np.sqrt((i - i1)**2 + (j - j1)**2) for i1, j1 in black_squares])
def featurize(grid, feature_idxs, black_squares):
    """
    grid: 10x10 color grid, colors are -1, -0.5, 0, 0.5, 1
    feature_idxs: dictionary, maps colors to feature index 
        {-1:0, -0.5:1,...}
    """
    feature_map = []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            color = grid[i, j]
            features = np.zeros(len(feature_idxs))
            if color in feature_idxs.keys():
                features[feature_idxs[color]] += 1
            # features[-1] = dist_to_black(i, j, black_squares)
            feature_map.append(features)
    return np.array(feature_map)
def state_idx_to_ij(idx, grid):
    i = math.floor(idx / grid.shape[0])
    j = idx % grid.shape[1]
    return (i, j)
file_name = "./data/environments.pkl"
f = open(file_name, "rb")
envs = pickle.load(f)
f.close()
env = envs['env_2']
grid = np.array(env.grid)

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
print grid
path = env.paths['path_2']
demo = []
for (i, j) in path: 
    demo.append((i * grid.shape[1]) + j)
demos = [demo]

# all_black_squares = get_color_squares(grid, -1)
feature_map = featurize(grid, {-1:0, -0.5:1, 0.5:2, 1:3}, None)
maxent_irl(feature_map, transitions, 0.81, demos, 0.01, 20)
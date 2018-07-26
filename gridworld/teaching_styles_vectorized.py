from __future__ import division
import numpy as np
import pickle
import math
import matplotlib.pyplot as plt
from environment import Environment
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--env', type=int, required=True)
parser.add_argument('-p', '--path', type=int, required=True)
parser.add_argument('-s', '--strategy', default='optimal')
parser.add_argument('--plot', type=bool, default=False)
args = parser.parse_args()
print args.plot
np.set_printoptions(precision=2)

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
    return i, j
def next_state_from_action_idx(state, a):
    i, j = state_idx_to_ij(state, grid)
    if a == 0 and j != 9:
       j += 1
    elif a == 1 and i != 0:
        i -= 1
    elif a == 2 and j != 0:
        j -= 1
    elif a == 3 and i != 9:
        i += 1
    return (i * grid.shape[1]) + j
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
def dist_to_squares(i, j, squares):
    """
    (i, j): grid location
    black_squares: list of (i, j) locations of black squares
    """
    return np.average([np.sqrt((i - i1)**2 + (j - j1)**2) for i1, j1 in squares])
def featurize(grid, feature_idxs, black_squares):
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
            features = np.zeros(len(feature_idxs) + 1)
            if color in feature_idxs.keys():
                features[feature_idxs[color]] += 1
            # feature for distance to black
            # features[-1] = dist_to_black(i, j, black_squares)
            # feature for living reward
            features[-1] = -1.0
            feature_map.append(features)
    return np.array(feature_map)
def value_iteration_optimal_trajectory(transitions, rewards, gamma, threshold):
    """
    transition: NxNxN_ACTIONS - transition dynamics
    rewards: Nx1 - state rewards
    gamma: discount factor
    threshold: threshold for stopping
    returns optimal trajectory for this grid and rewards
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
    path = [start]
    loc = start
    seen = set()
    seen.add(start)
    while loc != goal:
        action = policy[int(loc)]
        loc = int(next_state_from_action_idx(loc, action))
        if loc in seen:
            break
        path.append(loc)
        seen.add(loc)
    # print path
    return path
def partition_function(trajectory_set, theta, beta=1):
    """
    trajectory_set -DxN_FEAT - all featurized trajectories which are optimal for 
                                some theta
    theta: N_FEATx1 - current reward parameters to reason over
    beta: scalar - rationality coefficient
    """
    return np.sum(np.exp(beta * trajectory_set.dot(theta)))
def prob_trajectory_given_theta(trajectory, trajectory_set, theta, beta=1):
    """
    trajectory: N_FEATx1 - featurized trajectory to reason about, sum of state feature counts
    theta: N_FEATx1 - current reward parameters to reason over
    trajectory_set - DxN_FEAT - all featurized trajectories which are optimal for 
                                some theta
    beta: scalar - rationality coefficient
    returns P(xi | theta)
    """
    return np.exp(beta * np.dot(trajectory, theta)) / partition_function(trajectory_set, theta, beta)
def update_distribution(prior, thetas, demonstration, trajectory_set):
    """
    prior: Nx1 - list of probabilities for each theta
    thetas: NxN_FEAT - list of reward parameters to reason over
    demonstration: N_FEATx1 - featurized trajectory to reason about, sum of state feature counts
    trajectory_set - DxN_FEAT - all featurized trajectories which are optimal for 
                                some theta
    returns P(theta | xi)
    """
    numerators = []
    for i, theta in enumerate(thetas):
        numerators.append(prob_trajectory_given_theta(demonstration, trajectory_set, theta) * prior[i])
    numerators = np.array(numerators)
    return numerators / np.sum(numerators)

env_num = args.env
path_num = args.path
strategy = args.strategy

file_name ="./data/environments.pkl"
f = open(file_name, "rb")
envs = pickle.load(f)
f.close()
env = envs['env_' + str(env_num)]
grid = np.array(env.grid)
start = (env.start[0] * grid.shape[1]) + env.start[1]
goal = (env.goal[0] * grid.shape[1]) + env.goal[1]
demonstration = env.paths['path_' + str(path_num)]
demonstration = [(i * grid.shape[1]) + j for (i, j) in demonstration]

black_squares = get_color_squares(grid, -1)
feature_map = featurize(grid, {-1:0, -0.5:1, 0.5:2, 1:3}, black_squares)
demo_featurized = sum([feature_map[s] for s in demonstration])
transitions = create_transitions(grid)
thetas = []
for i in np.linspace(-1.0, 1.0, 5):
    for j in np.linspace(-1.0, 1.0, 5):
        for k in np.linspace(-1.0, 1.0, 5):
            for l in np.linspace(-1.0, 1.0, 5):
                for m in np.linspace(-1.0, 1.0, 2):
                    thetas.append((i, j, k, l, m))
ground_truth = (-1, -0.5, 0.5, 1, -1)
# thetas = [(-1.0, -0.5,  0.5,  1.0, -1.0),
#           (-0.5, -0.5,  0.5,  1.0, -1.0),
#           ( 1.0,  0.5, -0.5, -1.0,  1.0),
#           ( 1.0,  1.0,  1.0,  1.0,  1.0),
#           (-0.5, -1.0,  1.0,  0.5, -1.0),
#           ( 2.0,  0.5,  0.1,  2.0,  1.0)]
ground_truth_idx = thetas.index(ground_truth)

black_squares = get_color_squares(grid, -1)
distances = []
for s in range(100):
    i, j = state_idx_to_ij(s, grid)
    distances.append(dist_to_squares(i, j, black_squares))
distances = np.array(distances)

trajectory_set = []
for theta in tqdm(thetas):
    rewards = feature_map.dot(theta)
    if strategy == "avoid":
        # rewards += 0.5 * (-distances * theta[0])
        if theta[0] >= 0:
            rewards += 0.5 / distances 
        else:
            rewards += 0.5 * distances
    rewards[goal] = 7
    trajectory_set.append(value_iteration_optimal_trajectory(transitions, rewards, 0.81, 0.01))
if args.plot:
    for i, traj in enumerate(trajectory_set):
        ij_path = path_to_ij(10, 10, traj)
        env.paths['path_' + str(i)] = ij_path
    fig, ax = plt.subplots()
    env.show_all_paths(ax)
    plt.show()

trajectory_set = np.array([sum([feature_map[s] for s in traj]) for traj in trajectory_set])

prior = np.ones(len(thetas)) / len(thetas)
posterior = update_distribution(prior, thetas, demo_featurized, trajectory_set)

largest_idxs = np.argwhere(posterior == np.amax(posterior)).flatten()
best_thetas = np.array(thetas)[largest_idxs]
dist_to_gt = np.average([np.linalg.norm(ground_truth - theta) for theta in best_thetas])
prob_gt = posterior[ground_truth_idx]

file_name = "./data/env" + str(env_num) + "_path" + str(path_num) + "_" + strategy + ".pkl"
f = open(file_name, "wb")
data = {'env': env, 'thetas': thetas, 'prior': prior, 'posterior': posterior, 'demonstration': demonstration,
        'demo_featurized': demo_featurized, 'trajectory_set': trajectory_set, 'ground_truth': ground_truth,
        'mode_dist_to_gt': dist_to_gt, 'prob_gt': prob_gt}
pickle.dump(data, f)
f.close()

# optimal demonstration calculation
rewards = feature_map.dot(ground_truth)
print value_iteration_optimal_trajectory(transitions, rewards, 0.81, 0.01)

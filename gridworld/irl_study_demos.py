from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import pickle
import networkx as nx
from environment import Environment
from utils import *

np.set_printoptions(precision=3)
alpha = 0.01
threshold = 0.02
learn_living_reward = True
env_num = 3

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

    col_idxs = [0, 2, 4, 6, 8, 9]
    row_idxs = [0, 2, 4, 5, 7, 9]

    # for grid 3 and grid 15
    col_idxs = [0, 2, 3, 5, 6, 7]
    row_idxs = [0, 2, 3, 4, 5, 6]

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
file_name = "./data/mturk_6_21_18/parsed_envs.pkl"
f = open(file_name, "rb")
envs = pickle.load(f)['envs']
f.close()

env = envs[env_num]

trajectory_set = compute_trajectory_set_nx(np.zeros((10, 10)), env.start, env.goal)
grid = np.array(env.grid)
feature_map = featurize(grid, {-1:0, -0.5:1, 0.5:2, 1:3})
traj_set_featurized = np.array([partial_traj_to_features(traj, feature_map, grid, include_living_cost=True) for traj in trajectory_set])

env_copy = Environment(grid=np.array(env.grid), start=env.start, goal=env.goal, living_reward=env.living_reward, true_rewards=env.true_rewards)
fig, ax = plt.subplots()
env.show_grid(ax)

distances_from_gt = []
learned_weights = []
if learn_living_reward:
    ground_truth = np.array([-1, -0.5, 0.5, 1, env.living_reward])
else:
    ground_truth = np.array([-1, -0.5, 0.5, 1])
ground_truth = ground_truth / np.linalg.norm(ground_truth)

for i in range(10):
    demo = env.paths['path_' + str(i)]
    demo_featurized = sum([feature_map[int(ij_to_idx(s[0], s[1], grid.shape[0]))] for s in demo])
    if learn_living_reward:
        demo_featurized = np.hstack((demo_featurized, len(demo)-1))

    if learn_living_reward:
        w = np.ones(5) / np.linalg.norm(np.ones(5))
    else:
        w = np.ones(4) / np.linalg.norm(np.ones(4))

    iteration = 0
    while True:
        if learn_living_reward:
            optimal_features = traj_set_featurized[np.argmin(traj_set_featurized.dot(w))]
        else:
            optimal_features = traj_set_featurized[np.argmin(traj_set_featurized.dot(np.hstack((w, [-env.living_reward]))))][:-1]
        w_new = w * (1 - alpha) - alpha * (demo_featurized - optimal_features)
        if np.linalg.norm(w - w_new) <= threshold or iteration > 1000:
            break
        else:
            print np.linalg.norm(w - w_new)
        w = w_new
        # print w_new
        iteration += 1
    # learned w will be for cost function, want store as reward parameters
    w = -w / np.linalg.norm(w)
    print w
    learned_weights.append(w)
    distances_from_gt.append(np.linalg.norm(w - ground_truth))
    if learn_living_reward:
        learned_trajectory = trajectory_set[np.argmax(traj_set_featurized.dot(w))]
    else:
        learned_trajectory = trajectory_set[np.argmax(traj_set_featurized.dot(np.hstack((w, [env.living_reward]))))]

    env_copy.paths['path_0'] = demo
    env_copy.paths['path_1'] = learned_trajectory
    ax.clear()
    env_copy.show_grid(ax)
    env_copy.show_path(ax, 0, noisy=True)
    env_copy.show_path(ax, 1, noisy=True)
    plt.pause(0.01)
    raw_input()
plt.figure(2)
plt.bar(list(range(10)), distances_from_gt)
plt.title('Grid ' + str(env_num) + ' distances from GT')

fig, axes = plt.subplots(nrows=5, ncols=2)
axes = np.array(axes).flatten()
for i, ax in enumerate(axes):
    env.show_grid(ax)
    env.show_path(ax, i)
    ax.set_title("Demo " + str(i) + ", " + str(learned_weights[i]))
plt.show()
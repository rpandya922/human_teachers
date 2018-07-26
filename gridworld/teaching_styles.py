from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import pickle
from environment import Environment
import networkx as nx
from utils import *
# find out if knowledge of teaching style helps with prediction of true reward parameters

NUM_TRAJECTORIES = 1
DEFAULT_ACTION_LENGTH = 500

def compute_trajectory_from_actions(actions, grid, start, goal, allow_looping=False):
    traj = [start]
    state = start
    reached_states = set()
    goal_reached = False
    for a in actions:
        # 0: right, 1: up, 2: left, 3: down
        i, j = next_state_from_action_idx(state, a)
        if is_valid(i, j, grid):
            if all([(state[0], state[1], x) in reached_states for x in get_valid_actions(state[0], state[1], grid)]):
                # not allowing looping gets stuck easily, need a better fix for this, it's still a hack
                reached_states = set()
            if not allow_looping:
                if (state[0], state[1], a) in reached_states:
                    continue
            traj.append((i, j))
            reached_states.add((state[0], state[1], a))
            state = (i, j)
            if (i, j) == goal:
                goal_reached = True
                break
    print len(traj)
    while not goal_reached:
        a = np.random.randint(0, 4)
        i, j = next_state_from_action_idx(state, a)
        if is_valid(i, j, grid):
            if all([(state[0], state[1], x) in reached_states for x in get_valid_actions(state[0], state[1], grid)]):
                # allow_looping = True
                reached_states = set()
            if not allow_looping:
                if (state[0], state[1], a) in reached_states:
                    continue
            traj.append((i, j))
            reached_states.add((state[0], state[1], a))
            state = (i, j)
            if (i, j) == goal:
                goal_reached = True
                break
    return traj
def compute_trajectory_set_sampling(grid, start, goal):
    # randomly initialize a matrix: each row is a sequence of actions, number of 
    # rows is number of trajectories to sample
    actions_matrix = np.random.randint(0, 4, size=(NUM_TRAJECTORIES, DEFAULT_ACTION_LENGTH)) # actions: 0,1,2,3
    trajectories = []
    for actions in actions_matrix:
        trajectories.append(compute_trajectory_from_actions(actions, grid, start, goal))
    return trajectories
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
    print len(list(nx.all_simple_paths(G, start, goal, cutoff=19)))
def compute_trajectory_set(env, thetas):
    """
    env: Environment object (contains grid, start/goal, living reward, etc)
    thetas: list of possible parameter vectors
    returns set of trajectories optimal for some theta
    """
    return [vi_optimal_trajectory(env, theta, style='') for theta in thetas]
def featurize(trajectory, grid, reward_idxs):
    """
    reward_idxs: dictionary mapping reward value to feature index 
    returns list of color counts from grid in order
    """
    counts = np.zeros(len(reward_idxs))
    for state in trajectory:
        counts[reward_idxs[grid[state]]] += 1
    return counts
def partition_function(trajectories, theta, beta):
    """
    trajectories: 2D array of featurized trajectories (color counts)
    theta: reward parameters, weight for each color
    """
    return np.sum(np.exp(beta * trajectories.dot(theta)))
def prob_trajectory_given_theta(trajectory, trajectories, theta, beta=1):
    """
    trajectory: featurized trajectory
    trajectories: 2D array of featurized trajectories (color counts)
    theta: reward parameters, weight for each color
    """
    return np.exp(beta * np.dot(trajectory, theta)) / partition_function(trajectories, theta, beta)
def prob_theta_given_demonstration(demonstration, trajectories, theta, thetas, prior, beta=1):
    """
    demonstration: demonstrated trajectory
    trajetories: 2D array of featurized trajectories
    theta: potential reward parameters
    thetas: all possible reward parameters
    prior: dictionary, previous belief over theta: between 0-1 for each theta in thetas
    beta: rationality coefficient
    returns P(theta | xi) = P(xi | theta) P(theta) / sum(P(xi | theta') P(theta'))
    """
    numerator = prob_trajectory_given_theta(demonstration, trajectories, theta) * prior[theta]
    denominator = sum([prob_trajectory_given_theta(demonstration, trajectories, t) * prior[t] for t in thetas])
    return numerator / denominator

file_name = "./data/environments.pkl"
f = open(file_name, "rb")
envs = pickle.load(f)
f.close()
env = envs['env_2']
env.grid = np.array(env.grid)
reward_idxs = {-1:0, -0.5:1, 0:2, 0.5:3, 1:4}

paths = {'path_2': [(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9)], 'path_0': [(5, 0), (4, 0), (3, 0), (2, 0), (1, 0), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9)], 'path_1': [(5, 0), (4, 0), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (4, 9), (5, 9)]}
env.paths = paths
fig, ax = plt.subplots()
env.show_all_paths(ax)
# plt.show()
# 1/0
demonstration = env.paths['path_2']
# demonstration = [(5, 0), (4, 0), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (4, 9), (5, 9)]
demo_features = featurize(demonstration, env.grid, reward_idxs)

# thetas = [(-1.0, -0.5,  0.0,  0.5,  1.0),
#           ( 1.0,  0.5,  0.0, -0.5, -1.0),
#           ( 1.0,  1.0,  0.0,  1.0,  1.0),
#           (-0.5, -1.0,  0.0,  1.0,  0.5),
#           (2.0,  0.5,  0.0,  0.1,  2.0)]
thetas = []
for i in np.linspace(-1.0, 1.0, 5):
    for j in np.linspace(-1.0, 1.0, 5):
        for k in np.linspace(-1.0, 1.0, 5):
            for l in np.linspace(-1.0, 1.0, 5):
                thetas.append((i, j, 0, k, l))
prior = {theta: 1 / len(thetas) for theta in thetas}
trajectories = compute_trajectory_set(env, thetas)
featurized = np.array([featurize(traj, env.grid, reward_idxs) for traj in trajectories])

new_probs = [prob_theta_given_demonstration(demo_features, featurized, theta, thetas, prior) for theta in thetas]
largest_idxs = np.argwhere(new_probs == np.amax(new_probs)).flatten()
print np.array(thetas)[largest_idxs]
print np.amax(new_probs)
fig1, ax1 = plt.subplots()
ax1.hist(new_probs)

# fig2, ax2 = plt.subplots()
# env.show_grid(ax2)
# env.show_path(ax2, 0)
# plt.show()
# 1/0
for i, traj in enumerate(trajectories):
    env.paths['path_' + str(i)] = traj
fig, ax = plt.subplots()
env.show_all_paths(ax)
plt.show()

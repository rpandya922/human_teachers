from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from environment import Environment
# find out if knowledge of teaching style helps with prediction of true reward parameters

NUM_TRAJECTORIES = 1
DEFAULT_ACTION_LENGTH = 500
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
def compute_trajectory_set(grid, start, goal):
    # randomly initialize a matrix: each row is a sequence of actions, number of 
    # rows is number of trajectories to sample
    actions_matrix = np.random.randint(0, 4, size=(NUM_TRAJECTORIES, DEFAULT_ACTION_LENGTH)) # actions: 0,1,2,3
    trajectories = []
    for actions in actions_matrix:
        trajectories.append(compute_trajectory_from_actions(actions, grid, start, goal))
    return trajectories
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
    trajectories: 2D array of featurized trajectories (color counts)
    theta: reward parameters, weight for each color
    """
    return np.exp(beta * np.dot(trajectory, theta)) / partition_function(trajectories, theta, beta)
grid = np.zeros((10, 10))
start = (5, 0)
goal = (5, 9)
env = Environment(grid, start=start, goal=goal, living_reward=0)

# may need to change to not allow looping in trajectories
trajectories = compute_trajectory_set(grid, start, goal)
featurized = np.array([featurize(traj, grid, {0: 0}) for traj in trajectories])

for i, traj in enumerate(trajectories):
    env.paths['path_' + str(i)] = traj
fig, ax = plt.subplots()
env.show_all_paths(ax)
plt.show()

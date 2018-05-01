from __future__ import division
import numpy as np
from collections import deque
from grid import GridWorld
import matplotlib.pyplot as plt
from matplotlib import colors
from utils import *
##################################################################
# CONSTANTS/FUNCTIONS
# costs of colors [green, blue, yellow]
costs = np.array([1, 2, 0])
costs = costs / np.linalg.norm(costs)
# number indicates color: (1: green, 2: blue, 3: yellow, 10: goal)
grid = np.array(
    [[0, 0, 3, 3,  0],
     [0, 1, 1, 3,  0],
     [0, 2, 1, 0,  0],
     [0, 2, 1, 0,  0],
     [0, 2, 2, 2,  0]
    ])
goal_location = (4, 4)

def featurize(grid, trajectories):
    n, m = grid.shape
    green, blue, yellow = [], [], []
    for i in range(n):
        for j in range(m):
            r = grid[(i, j)]
            if r == 1:
                green.append((i, j))
            elif r == 2:
                blue.append((i, j))
            elif r == 3:
                yellow.append((i, j))
    featurized = []
    for trajectory in trajectories:
        features = [0, 0, 0]
        for t in trajectory:
            s = t[0]
            if s in green:
                features[0] += 1
            elif s in blue:
                features[1] += 1
            elif s in yellow:
                features[2] += 1
        featurized.append(features[:])
    return np.array(featurized)
def distance(state1, state2):
    return np.linalg.norm(np.subtract(state1, state2))
# trajectory: [(s, a, s'), (s, a, s'), ...]
def get_plausiable_trajectories(grid, start_loc, goal_loc):
    partial_traj_queue = deque([])
    all_trajectories = []
    actions = ['w', 'a', 's', 'd']
    def help(traj):
        last_state = traj[-1][2]
        dist = distance(last_state, goal_loc)
        for a in actions:
            new_loc = gridworld.sim_transition(last_state, a)
            if new_loc == goal_loc:
                new_traj = traj[:]
                new_traj.append((last_state, a, new_loc))
                all_trajectories.append(new_traj)
            elif distance(new_loc, goal_loc) < dist:
                new_traj = traj[:]
                new_traj.append((last_state, a, new_loc))
                partial_traj_queue.append(new_traj)
    for a in actions:
        new_loc = gridworld.sim_transition(start_loc, a)
        dist = distance(start_loc, goal_loc)
        if distance(new_loc, goal_loc) < dist:
            new_traj = []
            new_traj.append((start_loc, a, new_loc))
            partial_traj_queue.append(new_traj)
    while len(partial_traj_queue) > 0:
        trajectory = partial_traj_queue.popleft()
        help(trajectory)
    return all_trajectories
##################################################################

plot_cost_function(costs, grid, 'Ground Truth Cost')

gridworld = GridWorld(grid, costs, goal_location, show_grid=False)
all_trajectories = get_plausiable_trajectories(gridworld, (0, 0), goal_location)

all_demonstrations = []
for _ in range(1):
    grid = np.array(
    [[0, 0, 3, 3,  0],
     [0, 1, 1, 3,  0],
     [0, 2, 1, 0,  0],
     [0, 2, 1, 0,  0],
     [0, 2, 2, 2,  0]
    ])
    gridworld = GridWorld(grid, costs, goal_location)
    trajectory = []
    goal_reached = False
    while not goal_reached:
        gridworld.plot_grid()
        a = raw_input("Enter next move: ")
        while a not in ['w', 'a', 's', 'd']:
            a = raw_input("Enter next move: ")
        t, goal_reached = gridworld.transition(a)
        trajectory.append(t)
    all_demonstrations.append(trajectory)
    gridworld.close_figure()
all_featurized = featurize(gridworld.grid, all_trajectories)
demo_features = featurize(gridworld.grid, all_demonstrations)

w = np.ones(3) / 3
alpha = 0.1
for _ in range(100):
    optimal_features = all_featurized[np.argmin(all_featurized.dot(w.T))]
    w = w * (1 - alpha) - alpha * np.mean(demo_features - optimal_features, axis=0)
learned_trajectory = all_trajectories[np.argmin(all_featurized.dot(w.T))]

# if there is a negative weight, shift so min is at 0
w = w - min(min(w), 0)
print w
plot_cost_function(w, grid, 'Learned Cost Function')

plot_demonstrations(all_demonstrations, grid, costs, goal_location)
plt.show()
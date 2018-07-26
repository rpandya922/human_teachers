from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import math
from environment import Environment
from utils import *

# colors as usual: -1=black, 1=white
grid = np.array([[1, -1,  1],
                 [1,  1,  1],
                 [1,  1,  1]])
start = (0, 2)
goal = (0, 0)
goal_reward = 2
env = Environment(grid=grid, start=start, goal=goal)
start = ij_to_idx(start[0], start[1], grid.shape[1])
goal = ij_to_idx(goal[0], goal[1], grid.shape[1])

# true feature weights (reward for [black, white])
ground_truth = np.array([-1, 1])
feature_map = featurize(grid, {-1: 0, 1: 1})
rewards = feature_map.dot(ground_truth)
rewards[goal] = goal_reward
transitions = create_transitions(grid)
optimal_policy = value_iteration(transitions, rewards, goal, 0.95, 0.01)

print optimal_policy.reshape((3, 3))

# gives coefficients x for inequalities of form w^Tx >= 0
weight_constraints = []
for state in range(len(optimal_policy)):
    optimal_action = int(optimal_policy[state])
    if optimal_action == -1:
        continue
    feature_counts_opt = feature_counts(optimal_policy, feature_map, start, optimal_action)
    other_actions = [0, 1, 2, 3]
    other_actions.remove(optimal_action)

    for b in other_actions:
        # create inequality w^T(mu_sa - mu_sb) >= 0
        feature_counts_other = feature_counts(optimal_policy, feature_map, start, b)
        weight_constraints.append(feature_counts_opt - feature_counts_other)

fig, ax = plt.subplots()
ax.set_ylim(-1, 1)
ax.set_xlim(-1, 1)
xs = np.linspace(-1, 1, 10)
for constraint in weight_constraints:
    y = [-constraint[0] / constraint[1] * x for x in xs]

    if constraint.dot([-1, 1]) > 0:
        y2 = [1 for _ in xs]
    elif constraint.dot([1, -1]) > 0:
        y2 = [-1 for _ in xs]

    print constraint
    plt.fill_between(xs, y, y2, alpha=0.1, color='C0')
    plt.pause(0.1)
plt.show()
from __future__ import division
import numpy as np
from grid import GridWorld
from sklearn.svm import SVC
import matplotlib.pyplot as plt
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
def feature_vector(gridworld, location):
    # for each neighbor (up, down, left, right), one-hot encode as
    # [green, blue, yellow, wall]
    location = (int(location[0]), int(location[1]))
    left = (int(location[0]), int(max(location[1] - 1, 0)))
    right = (int(location[0]), int(min(location[1] + 1, gridworld.m - 1)))
    up = (int(max(location[0] - 1, 0)), int(location[1]))
    down = (int(min(location[0] + 1, gridworld.n - 1)), int(location[1]))
    neighbors = [left, right, up, down]
    data_point = []
    for n in neighbors:
        if n == location:
            data_point.extend([0, 0, 0, 1])
        elif gridworld.grid[n] == 1:
            data_point.extend([1, 0, 0, 0])
        elif gridworld.grid[n] == 2:
            data_point.extend([0, 1, 0, 0])
        elif gridworld.grid[n] == 3:
            data_point.extend([0, 0, 1, 0])
        else:
            data_point.extend([0, 0, 0, 0])
    return np.array(data_point)
def create_train_data(gridworld, trajectories):
    train_data = []
    train_labels = []
    for trajectory in trajectories:
        for t in trajectory:
            s, a = t[0], t[1]

            train_data.append(feature_vector(gridworld, s))
            train_labels.append(a)
    train_data = np.array(train_data)
    train_labels = np.array(train_labels)
    
    return train_data, train_labels
def is_wall(point):
    n = np.array(grid).shape[0]
    m = np.array(grid).shape[1]
    if point[0] < 0 or point[0] >= n or point[1] < 0 or point[1] >= m:
        return True
    return False
##################################################################

plot_cost_function(costs, grid, 'Ground Truth Cost')
gridworld = GridWorld(grid, costs, goal_location, show_grid=False)

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
    gridworld.plot_grid()
    gridworld.close_figure()
X, y = create_train_data(gridworld, all_demonstrations)

svm = SVC(kernel='linear')
svm.fit(X, y)

xx, yy = np.mgrid[0:4:5j, 0:4:5j]
points = np.vstack([xx.ravel(), yy.ravel()]).T
grid_list = [[0, 0, 3, 3,  0],
        [0, 1, 1, 3,  0],
        [0, 2, 1, 0,  0],
        [0, 2, 1, 0,  0],
        [0, 2, 2, 2,  0]]

test_points = []
for p in points:
    test_points.append(feature_vector(gridworld, p))

predictions = svm.predict(test_points)
for i, p in enumerate(points):
    label = predictions[i]
    grid_list[int(p[0])][int(p[1])] = label

point = (0, 0)
learned_traj_points = [point]
while point != goal_location and not is_wall(point):
    action = grid_list[point[0]][point[1]]
    point = gridworld.sim_transition(point, action)
    learned_traj_points.append(point)
learned_traj_points = np.array(learned_traj_points)

gridworld = GridWorld(grid, costs, goal_location)
gridworld.plot_grid()
ax = gridworld.ax
ax.set_title('Learned Trajectory')
ax.plot(learned_traj_points[:,1], learned_traj_points[:,0], c='k', linestyle='--')

plot_demonstrations(all_demonstrations, grid, costs, goal_location)

plt.show()
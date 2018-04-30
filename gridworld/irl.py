from __future__ import division
import numpy as np
from collections import deque
from grid import GridWorld
import matplotlib.pyplot as plt

def featurize(gridworld, trajectories):
    green, blue, yellow = [], [], []
    for i in range(gridworld.n):
        for j in range(gridworld.m):
            r = gridworld.grid[(i, j)]
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
    actions = ['l', 'r', 'u', 'd']
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

# number indicates color: (1: green, 2: blue, 3: yellow, 10: goal)
# number also indicates cost (1: least costly)
grid = np.array(
    [[0, 0, 3, 3,  0],
     [0, 1, 1, 3,  0],
     [0, 2, 1, 0, 10],
     [0, 2, 1, 0,  0],
     [0, 2, 2, 2,  0]
    ])
gridworld = GridWorld(grid)

all_trajectories = get_plausiable_trajectories(gridworld, (0, 0), (2, 4))

all_demonstrations = []
for _ in range(2):
    grid = np.array(
    [[0, 0, 3, 3,  0],
     [0, 1, 1, 3,  0],
     [0, 2, 1, 0, 10],
     [0, 2, 1, 0,  0],
     [0, 2, 2, 2,  0]
    ])
    gridworld = GridWorld(grid)
    trajectory = []
    goal_reached = False
    while not goal_reached:
        gridworld.print_grid()
        a = raw_input("Enter next move: ")
        while a not in ['l', 'r', 'u', 'd']:
            a = raw_input("Enter next move: ")
        t, goal_reached = gridworld.transition(a)
        trajectory.append(t)
    all_demonstrations.append(trajectory)
all_featurized = featurize(gridworld, all_trajectories)
demo_features = featurize(gridworld, all_demonstrations)

w = np.zeros(3)
alpha = 0.1
for _ in range(100):
    optimal_features = all_featurized[np.argmin(all_featurized.dot(w.T))]
    w = w * (1 - alpha) - alpha * np.mean(demo_features - optimal_features, axis=0)
learned_trajectory = all_trajectories[np.argmin(all_featurized.dot(w.T))]
print w

for trajectory in all_demonstrations:
    points = []
    for t in trajectory:
        points.append(t[0])
    points.append(trajectory[-1][-1])
    points = np.array(points)
    plt.plot(points[:,0], points[:,1], c='b')

points = []
for t in learned_trajectory:
    points.append(t[0])
points.append(learned_trajectory[-1][-1])
points = np.array(points)
plt.plot(points[:,0], points[:,1], c='r')

plt.show()
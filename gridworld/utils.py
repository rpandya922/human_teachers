from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from grid import GridWorld
from environment import Environment

def plot_cost_function(costs, grid, title=''):
    costs = np.array(costs) / np.linalg.norm(costs)
    grid_copy = np.copy(grid).astype(float)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] != 0:
                # colors are 1-indexed, 0 means white space
                grid_copy[i, j] = costs[grid[i, j] - 1]
    fig, ax = plt.subplots()
    # cmap = colors.ListedColormap(['xkcd:white', 'xkcd:light red', 'xkcd:red', 'xkcd:dark red'])
    # bounds = sorted(costs)
    # b1 = (bounds[0] - 1.1)
    # b2 = (bounds[0] - 1 + bounds[0]) / 2
    # b3 = (bounds[0] + bounds[1]) / 2
    # b4 = (bounds[1] + bounds[2]) / 2
    # b5 = bounds[2] + 0.1
    # bounds = [b1, b2, b3, b4, b5]
    # norm = colors.BoundaryNorm(bounds, cmap.N)
    ax.set_title(title)
    cax = ax.imshow(grid_copy, cmap='Greys')
    cbar = fig.colorbar(cax)
    ax.grid(axis='both', linestyle='-', color='k', linewidth=2)
    ax.set_xticks(np.arange(-0.5, 4.5, 1))
    ax.set_yticks(np.arange(-0.5, 4.5, 1))
def plot_demonstrations(demonstrations, grid, costs, goal_location):
    gridworld = GridWorld(grid, costs, goal_location)
    gridworld.plot_grid()
    ax = gridworld.ax
    ax.set_title('Demonstrations')
    for trajectory in demonstrations:
        points = []
        for t in trajectory:
            points.append(t[0])
        points.append(trajectory[-1][-1])
        points = np.array(points)
        ax.plot(points[:,1], points[:,0], c='k', linestyle='--')

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
def reward(state, action, s_prime, grid, living_reward):
    # state, s_prime: (i, j)
    # action: [0, 1, 2, 3] = [right, up, left, down]
    # if s_prime in get_valid_neighbors(state[0], state[1], grid):
    return grid[s_prime] + living_reward
def vi_optimal_trajectory(env, theta, style=None):
    grid = np.array(env.grid)
    start = tuple(env.start)
    goal = tuple(env.goal)
    threshold = 0.001
    gamma = 0.881111111111
    living_reward = env.living_reward
    goal_value = 7

    color_to_reward = {-1:theta[0], -0.5:theta[1], 0:theta[2], 0.5:theta[3], 1:theta[4]}

    if style is not None:
        all_reward_locs = []
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                if grid[(i, j)] != 0:
                    all_reward_locs.append((i, j))
        alpha = 1
        style_grid = np.zeros(grid.shape)
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                r = np.average([color_to_reward[grid[r]] * (np.sqrt((i - r[0])**2 + (j - r[1])**2)) for r in all_reward_locs])
                style_grid[i,j] = -alpha * r

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            grid[i,j] = color_to_reward[grid[i,j]]
    if style is not None:
        grid += style_grid
    grid[goal] = goal_value

    value_function_prev = np.zeros(grid.shape)
    value_function = np.zeros(grid.shape)
    finished = False

    while not finished:
        value_function_prev = np.copy(value_function)
        value_function = np.zeros(grid.shape)
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                s = (i, j)
                vals = []
                for a in list(range(4)):
                    # sums over all s', but deterministic so only one
                    n = next_state_from_action_idx(s, a)
                    if is_valid(n[0], n[1], grid):
                        vals.append(reward(s, a, n, grid, living_reward) + (gamma * value_function_prev[n]))
                    # else:
                    #     vals.append(reward(s, a, s) + (gamma * value_function_prev[s]))
                value_function[s] = max(vals)

        if (np.abs(value_function - value_function_prev) < threshold).all():
            finished = True
    policy = np.zeros(grid.shape)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            s = (i, j)
            vals = []
            for a in list(range(4)):
                # sums over all s', but deterministic so only one
                n = next_state_from_action_idx(s, a)
                if is_valid(n[0], n[1], grid):
                    vals.append(reward(s, a, n, grid, living_reward) + (gamma * value_function[n]))
                else:
                    vals.append(float('-inf'))
            action = np.argmax(vals)
            policy[i,j] = action

    path = [start]
    loc = start
    seen = set(start)
    while loc != goal:
        action = policy[loc]
        loc = next_state_from_action_idx(loc, action)
        if loc in seen:
            print "Optimal trajectory does not reach goal"
            break
        path.append(loc)
        seen.add(loc)
    return path
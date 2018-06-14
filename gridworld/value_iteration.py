from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import pickle
from utils import * 
from environment import Environment
from tqdm import tqdm

np.set_printoptions(precision=2)
def transition_prob(state, action, s_prime):
    # returns P(s_prime | state, action)
    if s_prime in get_valid_neighbors(state[0], state[1], grid):
        return 1
    return 0

def reward(state, action, s_prime):
    # state, s_prime: (i, j)
    # action: [0, 1, 2, 3] = [right, up, left, down]
    # if s_prime in get_valid_neighbors(state[0], state[1], grid):
    return grid[s_prime] + living_reward

def style_grid(grid):
    all_reward_locs = []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[(i, j)] != 0:
                all_reward_locs.append((i, j))
    alpha = 1
    style_grid = np.zeros(grid.shape)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            r = np.average([grid[r] * (np.sqrt((i - r[0])**2 + (j - r[1])**2)) for r in all_reward_locs])
            style_grid[i,j] = -alpha * r
    return style_grid

def parameter_search():
    file_name = "./data/environments.pkl"
    f = open(file_name, "rb")
    envs = pickle.load(f)
    f.close()

    env = envs['env_27']
    grid = np.array(env.grid)
    start = tuple(env.start)
    goal = tuple(env.goal)
    threshold = 0.001
    gamma = 0.7
    living_reward = -1.1
    # env_27: gamma=0.881111111111, living reward: -3, goal value: 7, white value: 2.5
    # will go down then collect all white and go to goal
    for gamma in tqdm(np.linspace(0.01, 0.99, 10)):
        for living_reward in tqdm(np.linspace(-3, -1, 10)):
            for goal_value in tqdm(np.linspace(1, 10, 10)):
                for white_value in tqdm(np.linspace(0.5, 5, 10)):

                    grid = np.array(env.grid)
                    color_to_reward = {-1:-1, -0.5:-0.5, 0:0, 0.5:0.5, 1:white_value}
                    for i in range(grid.shape[0]):
                        for j in range(grid.shape[1]):
                            grid[i,j] = color_to_reward[grid[i,j]]
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
                                        vals.append(reward(s, a, n) + (gamma * value_function_prev[n]))
                                    # else:
                                    #     vals.append(reward(s, a, s) + (gamma * value_function_prev[s]))
                                value_function[s] = max(vals)

                        if (np.abs(value_function - value_function_prev) < threshold).all():
                            finished = True
                    policy = np.array([['' for i in range(10)] for j in range(10)])
                    for i in range(grid.shape[0]):
                        for j in range(grid.shape[1]):
                            s = (i, j)
                            vals = []
                            for a in list(range(4)):
                                # sums over all s', but deterministic so only one
                                n = next_state_from_action_idx(s, a)
                                if is_valid(n[0], n[1], grid):
                                    vals.append(reward(s, a, n) + (gamma * value_function[n]))
                                else:
                                    vals.append(float('-inf'))
                            action = np.argmax(vals)
                            if action == 0:
                                policy[s] = 'r'
                            elif action == 1:
                                policy[s] = 'u'
                            elif action == 2:
                                policy[s] = 'l'
                            elif action == 3:
                                policy[s] = 'd'
                    if policy[start] != 'r' and policy[9,9] != 'l':
                        print
                        print gamma
                        print living_reward
                        print goal_value
                        print white_value
                        print value_function

                        fig, ax = plt.subplots()
                        env.show_grid(ax)
                        for i in range(grid.shape[0]):
                            for j in range(grid.shape[1]):
                                ax.text(j, i, policy[i,j], color='purple')
                        plt.show()
                    del grid
                    del value_function
                    del value_function_prev

file_name = "./data/environments.pkl"
f = open(file_name, "rb")
envs = pickle.load(f)
f.close()

env = envs['env_27']
grid = np.array(env.grid)
start = tuple(env.start)
goal = tuple(env.goal)
threshold = 0.001
gamma = 0.881111111111
living_reward = -3
goal_value = 7
white_value = 2.5
# env_27: gamma=0.881111111111, living reward: -3, goal value: 7, white value: 2.5
# will go down then collect all white and go to goal
grid = np.array(env.grid)
color_to_reward = {-1:-1, -0.5:-0.5, 0:0, 0.5:0.5, 1:white_value}
for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
        grid[i,j] = color_to_reward[grid[i,j]]
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
                    vals.append(reward(s, a, n) + (gamma * value_function_prev[n]))
                # else:
                #     vals.append(reward(s, a, s) + (gamma * value_function_prev[s]))
            value_function[s] = max(vals)

    if (np.abs(value_function - value_function_prev) < threshold).all():
        finished = True
policy = np.array([['' for i in range(10)] for j in range(10)])
for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
        s = (i, j)
        vals = []
        for a in list(range(4)):
            # sums over all s', but deterministic so only one
            n = next_state_from_action_idx(s, a)
            if is_valid(n[0], n[1], grid):
                vals.append(reward(s, a, n) + (gamma * value_function[n]))
            else:
                vals.append(float('-inf'))
        action = np.argmax(vals)
        if action == 0:
            policy[s] = 'r'
        elif action == 1:
            policy[s] = 'u'
        elif action == 2:
            policy[s] = 'l'
        elif action == 3:
            policy[s] = 'd'

path = [start]
loc = start
while loc != goal:
    action = policy[loc]
    if action == 'r':
        loc = next_state_from_action_idx(loc, 0)
    elif action == 'u':
        loc = next_state_from_action_idx(loc, 1)
    elif action == 'l':
        loc = next_state_from_action_idx(loc, 2)
    elif action == 'd':
        loc = next_state_from_action_idx(loc, 3)
    path.append(loc)
path_num = len(env.paths)
env.paths['path_' + str(path_num)] = path

fig, ax = plt.subplots()
env.show_grid(ax)
# for i in range(grid.shape[0]):
#     for j in range(grid.shape[1]):
#         ax.text(j, i, policy[i,j], color='purple')
env.show_path(ax, path_num)
plt.show()

from __future__ import division
import numpy as np
import csv
import ast
import matplotlib.pyplot as plt
import math
from environment import Environment
import pickle
from copy import deepcopy

def print_strategies():
    with open('./data/pilot_study_questiondata.txt', 'rb') as f:
        for row in f.readlines():
            data = ast.literal_eval(row)
            print "###################################################"
            for i in range(9):
                print data['strategy_' + str(i)]
            print "###################################################"
            print
def grid_to_tuple(grid): return tuple([tuple(r) for r in grid])
def path_to_ij(m, n, path, noisy=True):
    # path: list of indices in 2D array
    # n, m: dimensions of array
    ij_path = []
    for idx in path:
        if noisy:
            i = math.floor(idx / m) + np.random.uniform(-0.1, 0.1)
            j = idx % n + np.random.uniform(-0.1, 0.1)
        else:
            i = math.floor(idx / m)
            j = idx % n
        ij_path.append([i, j])
    return np.array(ij_path)
def idx_to_ij(idx, m=10, n=10):
    i = math.floor(idx / m)
    j = idx % n
    return int(i), int(j)
def show_grid_from_txt():
    fig, axes = plt.subplots(nrows=3, ncols=3)
    axes = np.array(axes).flatten()
    colors = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']
    color_names = ['Blue', 'Orange', 'Green', 'Red', 'Purple', 'Brown', 'Pink', 'Gray', 'Gold', 'Cyan']
    for grid_idx in range(9):
        grids = {}
        grid_order = []
        all_paths = []
        all_strategies = []
        # was too lazy to make 9 different lists, so we re-parse each time for more consise code
        with open('./data/pilot_study_questiondata.txt', 'rb') as f:
            for i, row in enumerate(f.readlines()):
                data = ast.literal_eval(row)
                if i == 0:
                    # since order of grids was randomized, pick first subject as "true" order
                    for j in range(9):
                        # lists can't be hashed
                        grid = grid_to_tuple(data['grid_' + str(j)])
                        grids[grid] = j
                        grid_order.append(grid)
                for j in range(9):
                    grid = grid_to_tuple(data['grid_' + str(j)])
                    # if grid j matches "true" grid_idx, add path j to list of all paths for grid_idx
                    if grids[grid] == grid_idx:
                        all_paths.append(data['path_' + str(j)])
                        all_strategies.append(data['strategy_' + str(j)])
        print "###################################################"
        print "Grid " + str(grid_idx) + " Strategies"
        for i, strategy in enumerate(all_strategies):
            print color_names[i] + ": " + strategy
            # print strategy
        print "###################################################"
        print
    # order: blue, orange, green, red, purple
        grid_0 = grid_order[grid_idx]
        ax = axes[grid_idx]
        ax.imshow(grid_0, cmap="Greys_r", vmin=-1, vmax=1)
        ax.grid(axis='both', linestyle='-', color='k', linewidth=2)
        ax.set_xticks(np.arange(-0.5, 10 + 0.5, 1))
        ax.set_yticks(np.arange(-0.5, 10 + 0.5, 1))
        ax.set_title('Grid ' + str(grid_idx))
        for i, path in enumerate(all_paths):
            if i in range(5):
                continue
            ij_path = path_to_ij(10, 10, path)
            ax.plot(ij_path[:,1], ij_path[:,0], linewidth=3, c=colors[i], alpha=1)
            # ax.plot(ij_path[:,1], ij_path[:,0], linewidth=3, alpha=1)
    plt.show()
def parse_from_csv(save=False):
    colors = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']
    color_names = ['Blue', 'Orange', 'Green', 'Red', 'Purple', 'Brown', 'Pink', 'Gray', 'Gold', 'Cyan']
    num_grids = 16
    num_users = 10
    # very unfinished function
    # proper way to parse data, but first half of pilot has no questiondata.csv file, so use txt file for now
    with open('./data/mturk_6_21_18/questiondata.csv', 'rb') as f:
        reader = csv.reader(f, delimiter=',')
        # dictionary mapping user id to dictionary of question -> answer pairs
        user_data = {}
        for i, row in enumerate(reader):
            user, question, answer = row
            try:
                user_data[user][question] = answer
            except:
                user_data[user] = {question: answer}
        # total number of questions in study, if any lower then user didn't finish
        num_keys = 138
        for user in user_data.keys():
            if len(user_data[user]) < num_keys:
                user_data.pop(user, None)
        
        grids = [0 for _ in range(num_grids)]
        demonstrations = [[] for _ in range(num_grids)]
        strategies = [[] for _ in range(num_grids)]
        starts = [0 for _ in range(num_grids)]
        goals = [0 for _ in range(num_grids)]
        true_rewards = [0 for _ in range(num_grids)]
        living_rewards = [0 for _ in range(num_grids)]
        colors = [-1, -0.5, 0, 0.5, 1]
        user0_data = user_data[user_data.keys()[0]]

        for i, grid_idx in enumerate(ast.literal_eval(user0_data['grid_order'])):
            grids[grid_idx] = ast.literal_eval(user0_data['grid_' + str(i)])
            starts[grid_idx] = idx_to_ij(ast.literal_eval(user0_data['start_loc_' + str(i)]))
            goals[grid_idx] = idx_to_ij(ast.literal_eval(user0_data['goal_loc_' + str(i)]))
            true_rewards[grid_idx] = ast.literal_eval(user0_data['reward_values_' + str(i)])
            living_rewards[grid_idx] = ast.literal_eval(user0_data['living_reward_' + str(i)])
        # for saving
        grids_copy = deepcopy(grids)
        for idx, grid in enumerate(grids):
            for i in range(10):
                for j in range(10):
                    color_idx = true_rewards[idx].index(grid[i][j])
                    # grids are saved with reward values at each square, 
                    # this changes them to be colors instead
                    grid[i][j] = colors[color_idx]

        for user in user_data.keys():
            data = user_data[user]
            grid_order = ast.literal_eval(data['grid_order'])

            for i, grid_idx in enumerate(grid_order):
                demonstration = ast.literal_eval(data['path_' + str(i)])
                strategy = data['strategy_' + str(i)]

                demonstrations[grid_idx].append(demonstration)
                strategies[grid_idx].append(strategy)

        if save:
            data_to_save = {'envs': []}
            for i in range(num_grids):
                env = Environment(grid=grids_copy[i], start=starts[i], goal=goals[i], 
                                  living_reward=living_rewards[i], true_rewards=true_rewards[i])
                for j in range(num_users):
                    path = demonstrations[i][j]
                    ij_path = path_to_ij(10, 10, path, noisy=False)
                    env.paths['path_' + str(j)] = ij_path
                data_to_save['envs'].append(env)
            file_name = './data/mturk_6_21_18/parsed_envs.pkl'
            f = open(file_name, "wb")
            pickle.dump(data_to_save, f)
            f.close()

        fig, axes = plt.subplots(nrows=4, ncols=4)
        axes = np.array(axes).flatten()

        for i in range(num_grids):
            ax = axes[i]
            env = Environment(grid=grids[i], start=starts[i], goal=goals[i], living_reward=living_rewards[i])

            print "####################################"
            print "Grid " + str(i)
            for j in range(num_users):
                path = demonstrations[i][j]
                ij_path = path_to_ij(10, 10, path)
                env.paths['path_' + str(j)] = ij_path
                print color_names[j] + ": " + strategies[i][j]
            print "####################################"
            print
            env.show_all_paths(ax)
            ax.set_title('Grid ' + str(i))
        plt.show()

parse_from_csv()

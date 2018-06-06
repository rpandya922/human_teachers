from __future__ import division
import numpy as np
import csv
import ast
import matplotlib.pyplot as plt
import math

def print_strategies():
    with open('./data/pilot_study_questiondata.txt', 'rb') as f:
        for row in f.readlines():
            data = ast.literal_eval(row)
            print "###################################################"
            for i in range(9):
                print data['strategy_' + str(i)]
            print "###################################################"
            print
def grid_to_tuple(grid):
    return tuple([tuple(r) for r in grid])
def path_to_ij(n, m, path):
    # path: list of indices in 2D array
    # n, m: dimensions of array
    ij_path = []
    for idx in path:
        i = math.floor(idx / m) + np.random.uniform(-0.1, 0.1)
        j = idx % n + np.random.uniform(-0.1, 0.1)
        ij_path.append([i, j])
    return np.array(ij_path)
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
def parse_from_csv():
    # very unfinished function
    # proper way to parse data, but first half of pilot has no questiondata.csv file, so use txt file for now
    with open('./data/questiondata.csv', 'rb') as f:
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
        num_keys = 43
        for user in user_data.keys():
            if len(user_data[user]) < num_keys:
                user_data.pop(user, None)
        print len(user_data.keys())
show_grid_from_txt()



from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import sys

def command_line():
    plt.figure()
    # initialize as all neutral
    grid = np.zeros((10,10))
    print grid
    plt.imshow(grid, cmap="Greys_r", vmin=-1, vmax=1)
    plt.pause(0.1)

    num_cost_areas = int(raw_input("Enter the number of high cost areas [0,1,2]: "))
    num_reward_areas = int(raw_input("Enter number of high reward areas [0,1,2]: "))

    # reward goes from -1:1 (for easy color mapping in turk study)
    if num_cost_areas == 0:
        costs = []
    elif num_cost_areas == 1:
        costs = [-1]
    elif num_cost_areas == 2:
        costs = [-1, -0.5]
    else:
        print "Need between 0 and 2 cost areas"
        sys.exit()

    if num_reward_areas == 0:
        rewards = []
    elif num_reward_areas == 1:
        rewards = [1]
    elif num_reward_areas == 2:
        rewards = [0.5, 1]
    else:
        print "Need between 0 and 2 reward areas"
        sys.exit()

    for cost in costs:
        start_loc = map(int, raw_input("Enter start location of reward " + str(cost) + " area: ").split(' '))
        direction = raw_input("Direction (h/v): ")

        # create 2x3 or 3x2 area with cost 
        if direction == 'h':
            for i in range(2):
                for j in range(3):
                    loc = (start_loc[0] + i, start_loc[1] + j)
                    grid[loc] = cost
        elif direction == 'v':
            for i in range(3):
                for j in range(2):
                    loc = (start_loc[0] + i, start_loc[1] + j)
                    grid[loc] = cost
        print repr(grid)
        plt.imshow(grid, cmap="Greys_r", vmin=-1, vmax=1)
        plt.pause(0.1)

    for reward in rewards:
        start_loc = map(int, raw_input("Enter start location of reward " + str(reward) + " area: ").split(' '))
        direction = raw_input("Direction (h/v): ")

        if direction == 'h':
            for i in range(2):
                for j in range(3):
                    loc = (start_loc[0] + i, start_loc[1] + j)
                    grid[loc] = reward
        elif direction == 'v':
            for i in range(3):
                for j in range(2):
                    loc = (start_loc[0] + i, start_loc[1] + j)
                    grid[loc] = reward
        print repr(grid)
        plt.imshow(grid, cmap="Greys_r", vmin=-1, vmax=1)
        plt.pause(0.1)

    plt.show()
def xy_to_ij(x, y):
    return (int(round(x)), int(round(y)))
def interactive():
    # initialize as all neutral
    grid = np.zeros((10,10))
    fig, ax = plt.subplots()
    start_loc = map(int, (raw_input("Start location: ") or "5 0").split(' '))
    goal_loc = map(int, (raw_input("End location: ") or "5 9").split(' '))
    def show_grid(grid, ax):
        ax.clear()
        cmap = plt.cm.gray
        norm = plt.Normalize(-1, 1)
        rgba = cmap(norm(grid))
        # colors start and goal pixels individually
        rgba[start_loc[0], start_loc[1], :3] = 0, 0, 1
        rgba[goal_loc[0], goal_loc[1], :3] = 1, 0, 0

        ax.imshow(rgba)
        ax.grid(axis='both', linestyle='-', color='k', linewidth=2)
        ax.set_xticks(np.arange(-0.5, 10 + 0.5, 1))
        ax.set_yticks(np.arange(-0.5, 10 + 0.5, 1))
        plt.pause(0.1)
    
    for reward in [-1, -0.5, 0.5, 1]:
        def onclick(event):
            # matrix indices vs x,y are flipped
            i, j = xy_to_ij(event.ydata, event.xdata)
            grid[i][j] = reward
            show_grid(grid, ax)

        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        show_grid(grid, ax)
        raw_input('Click Enter when done with ' + str(reward) + ' area: ')
        fig.canvas.mpl_disconnect(cid)
    print repr(grid)
interactive()
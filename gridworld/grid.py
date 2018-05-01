from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

class GridWorld():
    def __init__(self, grid, costs, goal_location, show_grid=True):
        self.grid = grid
        self.n = grid.shape[0]
        self.m = grid.shape[1]
        self.costs = costs
        self.agent_location = (0, 0)
        self.total_cost = 0
        self.goal_location = goal_location
        if show_grid:
            fig, ax = plt.subplots()
            self.fig = fig
            self.ax = ax
        self.actions = {'left': 'a', 'right': 'd', 'up': 'w', 'down': 's'}

    def transition(self, action):
        old_location = self.agent_location
        if action == self.actions['left']:
            new_location = (self.agent_location[0], max(self.agent_location[1] - 1, 0))
        elif action == self.actions['right']:
            new_location = (self.agent_location[0], min(self.agent_location[1] + 1, self.m - 1))
        elif action == self.actions['up']:
            new_location = (max(self.agent_location[0] - 1, 0), self.agent_location[1])
        elif action == self.actions['down']:
            new_location =(min(self.agent_location[0] + 1, self.n - 1), self.agent_location[1])
        else:
            print "Enter valid action [w, a, s, d]. "
        self.agent_location = new_location
        cost = 0
        if self.grid[self.agent_location] != 0:
            # grid has color/cost indices (1-indexed: 0 is colorless)
            cost = self.costs[self.grid[self.agent_location] - 1]
        self.total_cost += cost

        if self.agent_location == self.goal_location:
            print "Goal Reached."
            return (old_location, action, cost, self.agent_location), True
        return (old_location, action, cost, self.agent_location), False

    def sim_transition(self, location, action):
        if action == self.actions['left']:
            new_location = (location[0], max(location[1] - 1, 0))
        elif action == self.actions['right']:
            new_location = (location[0], min(location[1] + 1, self.m - 1))
        elif action == self.actions['up']:
            new_location = (max(location[0] - 1, 0), location[1])
        elif action == self.actions['down']:
            new_location =(min(location[0] + 1, self.n - 1), location[1])
        else:
            print "Enter valid action [w, a, s, d]. "
        return new_location

    def print_grid(self):
        grid_copy = np.copy(self.grid)
        grid_copy[self.agent_location] = -1

        print grid_copy
        print "Total Cost: " + str(self.total_cost)

    def plot_grid(self):
        cmap = colors.ListedColormap(['xkcd:orange', 'xkcd:white', 'xkcd:green', 'xkcd:blue', 'xkcd:yellow'])
        grid_copy = np.copy(self.grid)
        grid_copy[self.goal_location] = -1

        self.ax.clear()
        self.ax.imshow(grid_copy, cmap=cmap)
        self.ax.grid(axis='both', linestyle='-', color='k', linewidth=2)
        self.ax.set_xticks(np.arange(-0.5, self.m + 0.5, 1))
        self.ax.set_yticks(np.arange(-0.5, self.n + 0.5, 1))

        # matrix indices vs (x, y) need to be swapped
        self.ax.scatter(self.agent_location[1], self.agent_location[0], s=100, c='r')
        plt.pause(0.1)
    def close_figure(self):
        if self.fig is not None:
            plt.close(self.fig)



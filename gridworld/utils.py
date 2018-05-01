from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from grid import GridWorld

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

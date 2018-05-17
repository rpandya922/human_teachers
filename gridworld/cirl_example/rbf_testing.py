from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

epsilon = 0.8
def rbf(x, theta, centers):
    diffs = x - centers
    dists = np.linalg.norm(diffs, axis=1)**2
    rbf = np.exp(-epsilon * dists)
    return theta.dot(rbf)
def plot_grid(grid):
        # cmap = colors.ListedColormap(['xkcd:orange', 'xkcd:white', 'xkcd:green', 'xkcd:blue', 'xkcd:yellow'])
        plt.figure()
        plt.imshow(grid, cmap="Greys_r")
        # plt.grid(axis='both', linestyle='-', color='k', linewidth=2)
        plt.xticks(np.arange(-0.5, 10 + 0.5, 1))
        plt.yticks(np.arange(-0.5, 10 + 0.5, 1))
        plt.pause(0.1)

theta = np.array([1, -1, 1]) #feature weights for rbf functions
centers = np.array([(4, 3), (6, 5), (4, 7)])

grid = np.zeros((10, 10))

for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
        grid[i][j] = rbf(np.array([i, j]), theta, centers)

np.set_printoptions(precision=2)
g = grid - min(grid.flatten())
g = g / max(g.flatten())
plot_grid(g)
print g
plt.show()

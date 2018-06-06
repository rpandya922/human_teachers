from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

all_grids = []
with open('grids.txt') as f:
    for num_grids in range(9):
        grid = []
        for _ in range(10):
            line = f.readline().split(' ')
            row = []
            for i in line:
                try:
                    row.append(float(i))
                except:
                    pass
            grid.append(row)
        f.readline()
        all_grids.append(np.array(grid))
        print repr(np.array(grid))
1/0
fig, axes = plt.subplots(nrows=3, ncols=3)
axes = np.array(axes).flatten()

for i, grid in enumerate(all_grids):
    ax = axes[i]

    cmap = plt.cm.gray
    norm = plt.Normalize(-1, 1)
    rgba = cmap(norm(grid))
    print rgba[5, 5, :3]
    rgba[5, 0, :3] = 0, 1, 0
    rgba[5, 9, :3] = 1, 0, 0
    ax.imshow(rgba)
plt.show()
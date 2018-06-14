from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

class Environment():
    def __init__(self, grid=None, start=None, goal=None, living_reward=None, horizon=None, true_rewards=[-1, -0.5, 0, 0.5, 1]):
        """
        :param: grid -- n by m reward matrix (numpy array)
        :param: start -- (i, j) start location
        :param: goal -- (i, j) goal location
        :param: living_reward  -- negative real number 
        """
        self.grid = grid
        self.start = start
        self.goal = goal
        self.living_reward = living_reward
        # dictionary of paths, each path is list of (i, j) matrix indices
        # default 3: one for "optimal", others for different strategies
        self.paths = {'path_0': [], 'path_1': [], 'path_2': []}
        self.horizon = horizon
        # values [-1, -0.5, 0, 0.5, 1] are for matplotlib colors [black, dark gray, gray, light gray, white]
        # true_rewards is list of reward values for these colors in this order
        self.true_rewards = true_rewards
    
    def create_grid(self):
        """
        function to interactively create 10 by 10 grid rewards
        """
        # initialize as all neutral
        grid = np.zeros((10,10))
        fig, ax = plt.subplots()
        start_loc = map(int, (raw_input("Start location: ") or "5 0").split(' '))
        goal_loc = raw_input("End location: ")
        if goal_loc:
            goal_loc = map(int, goal_loc.split(' '))
        else:
            goal_loc = None
        living_reward = float(raw_input("Living reward: ") or 0)
        horizon = raw_input("Time Horizon: ")
        if horizon:
            horizon = float(horizon)
        else:
            horizon = None
        true_rewards = raw_input("Color rewards [black, dark gray, gray, light gray, white]: ")
        if true_rewards:
            true_rewards = map(float, true_rewards.split(' '))
        else:
            true_rewards = [-1, -0.5, 0, 0.5, 1]

        def show_grid(grid, ax, vmin=-1, vmax=1):
            ax.clear()
            cmap = plt.cm.gray
            norm = plt.Normalize(vmin, vmax)
            rgba = cmap(norm(grid))
            # colors start and goal pixels individually
            rgba[start_loc[0], start_loc[1], :3] = 0, 0, 1
            if goal_loc is not None:
                rgba[goal_loc[0], goal_loc[1], :3] = 1, 0, 0

            ax.imshow(rgba)
            ax.grid(axis='both', linestyle='-', color='k', linewidth=2)
            ax.set_xticks(np.arange(-0.5, 10 + 0.5, 1))
            ax.set_yticks(np.arange(-0.5, 10 + 0.5, 1))
            plt.pause(0.01)
        
        for reward in [-1, -0.5, 0.5, 1]:
            def onclick(event):
                # matrix indices vs x,y are flipped
                j, i = (int(round(event.xdata)), int(round(event.ydata)))
                grid[i][j] = reward
                show_grid(grid, ax)

            cid = fig.canvas.mpl_connect('button_press_event', onclick)
            show_grid(grid, ax)
            raw_input('Click Enter when done with ' + str(reward) + ' area: ')
            fig.canvas.mpl_disconnect(cid)
        plt.close(fig)
        self.grid = grid
        self.start = start_loc
        self.goal = goal_loc
        self.living_reward = living_reward
        self.horizon = horizon
        self.true_rewards = true_rewards
        return grid

    def get_grid(self):
        return self.grid
    
    def get_start_location(self):
        return self.start
    
    def get_goal_location(self):
        return self.goal
    
    def get_living_reward(self):
        return self.living_reward
    
    def show_grid(self, ax, vmin=-1, vmax=1):
        cmap = plt.cm.gray
        norm = plt.Normalize(vmin, vmax)
        rgba = cmap(norm(self.grid))

        # colors start and goal pixels individually
        rgba[self.start[0], self.start[1], :3] = 0, 0, 1
        if self.goal is not None:
            rgba[self.goal[0], self.goal[1], :3] = 1, 0, 0

        ax.imshow(rgba)
        ax.grid(axis='both', linestyle='-', color='k', linewidth=2)
        ax.set_xticks(np.arange(-0.5, 10 + 0.5, 1))
        ax.set_yticks(np.arange(-0.5, 10 + 0.5, 1))
        # plt.pause(0.01)
    
    def show_path(self, ax, path_num, noisy=False, label=""):
        """
        to be called only after show_grid has been called
        """
        path = np.array(self.paths['path_' + str(path_num)])
        if noisy:
            noise = np.random.uniform(-0.1, 0.1, size=path.shape)
        else:
            noise = 0
        new_path = path + noise
        # ax.plot(new_path[:,1], new_path[:,0], c='C' + str(path_num), linewidth=4.5, label=label)
        ax.plot(new_path[:,1], new_path[:,0], linewidth=4.5, label=label)
        # plt.pause(0.01)

    def show_all_paths(self, ax, show_legend=False):
        self.show_grid(ax)
        ax.set_title('Living cost: ' + str(-self.living_reward))
        for i in range(len(self.paths.keys())):
            if self.paths['path_' + str(i)] != []:
                self.show_path(ax, i, noisy=True)
    
    def add_path(self, path_num, label=""):
        path = 'path_' + str(path_num)
        self.paths[path] = []
        fig, ax = plt.subplots()
        self.show_grid(ax)
        plt.pause(0.01)
        def onclick(event):
            j, i = (int(round(event.xdata)), int(round(event.ydata))) # path will be of matrix indices
            self.paths[path].append((i, j)) 
            self.show_path(ax, path_num, label)
            plt.pause(0.01)
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        raw_input('Hit Enter when done')
        fig.canvas.mpl_disconnect(cid)
        plt.close(fig)

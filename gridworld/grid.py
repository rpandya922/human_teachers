from __future__ import division
import numpy as np

class GridWorld():
    def __init__(self, grid):
        self.grid = grid
        self.n = grid.shape[0]
        self.m = grid.shape[1]
        self.agent_location = (0, 0)
        self.total_reward = 0
        goal_location = np.where(self.grid == 10)
        self.goal_location = (goal_location[0][0], goal_location[1][0])

    def transition(self, action):
        old_location = self.agent_location
        if action == 'l':
            new_location = (self.agent_location[0], max(self.agent_location[1] - 1, 0))
        elif action == 'r':
            new_location = (self.agent_location[0], min(self.agent_location[1] + 1, self.m - 1))
        elif action == 'u':
            new_location = (max(self.agent_location[0] - 1, 0), self.agent_location[1])
        elif action == 'd':
            new_location =(min(self.agent_location[0] + 1, self.n - 1), self.agent_location[1])
        else:
            print "Enter valid action [l, r, u, d]. "
        print new_location
        self.agent_location = new_location
        reward = self.grid[self.agent_location]
        self.total_reward += reward

        if self.agent_location == self.goal_location:
            print "Goal Reached."
            return (old_location, action, reward, self.agent_location), True
        return (old_location, action, reward, self.agent_location), False

    def sim_transition(self, location, action):
        if action == 'l':
            new_location = (location[0], max(location[1] - 1, 0))
        elif action == 'r':
            new_location = (location[0], min(location[1] + 1, self.m - 1))
        elif action == 'u':
            new_location = (max(location[0] - 1, 0), location[1])
        elif action == 'd':
            new_location =(min(location[0] + 1, self.n - 1), location[1])
        else:
            print "Enter valid action [l, r, u, d]. "
        return new_location

    def print_grid(self):
        grid_copy = np.copy(self.grid)
        grid_copy[self.agent_location] = -1

        print grid_copy
        print "Total Reward: " + str(self.total_reward)

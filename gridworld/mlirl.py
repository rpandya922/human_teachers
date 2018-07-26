from __future__ import division
import numpy as np
from environment import Environment
from utils import *

class MLIRL():
    def __init__(self, environment, demonstrations, features):
        self.grid = environment.grid
        self.start = environment.start
        self.goal = environment.goal
        self.demonstrations = demonstrations
        self.features = features
    def solve(self):
        grid = self.grid
        start = self.start
        goal = self.goal
        features = self.features

        feature_map = featurize(grid, features)
        d = len(features) # number of features
        N = len(feature_map) # number of states
        N_ACTIONS = 4
        gamma = 0.95 # discount factor
        alpha = 0.01 # step size
        beta = 0.75 # rationality coefficient
        transitions = create_transitions(grid) # NxNxN_ACTIONS

        demo = self.demonstrations[0]

        demo_w_actions = []
        for idx, (i, j) in enumerate(demo):
            if idx == len(demo) - 1:
                break
            i2, j2 = demo[idx + 1]
            if i == i2 and j + 1 == j2:
                action = 0
            elif j == j2 and i - 1 == i2:
                action = 1
            elif i == i2 and j - 1 == j2:
                action = 2
            elif j == j2 and i + 1 == i2:
                action = 3
            state_idx = ij_to_idx(i, j, grid.shape[0])
            demo_w_actions.append((state_idx, action))

        demonstrations = [demo_w_actions]
        K = len(demonstrations) # number of demonstrations?

        # time horizon/number of iterations
        n = 500

        # initial random weights
        weights = np.random.uniform(size=d)
        # reward = demo_featurized.dot(weights)

        for t in range(n):
            q_values = feature_map.dot(weights).reshape(-1, 1) * np.ones((N, N_ACTIONS))
            values = feature_map.dot(weights) # Nx1
            # N x d, vector of gradients for each state with respect to weights
            values_derivative = np.copy(feature_map) # N x d

            # dQ_i(s, a)/dw_j
            q_val_derivative = np.zeros((N, N_ACTIONS, d))
            # partition function for each state 
            Z = np.zeros(N)
            # partition function derivative with respect to weights
            Z_derivative = np.zeros((N, d))
            # probabilistic policy
            policy = np.zeros((N, N_ACTIONS))
            # policy gradient with respect to weights
            policy_derivative = np.zeros((N, N_ACTIONS, d))
            # dLi/dwj
            likelihood_derivative_full = np.zeros((K, d))
            # dL/dwj
            likelihood_derivative = np.zeros(d)
            for i in range(K):
                for state in range(N):
                    for action in range(N_ACTIONS):
                        q_values[state, action] = feature_map[state].dot(weights) + gamma * \
                            sum([transitions[state, s_prime, action] * values[s_prime] for s_prime in range(N)])

                        for j in range(d):
                            q_val_derivative[state, action, j] = feature_map[state][j] + \
                                gamma * sum([transitions[state, s_prime, action] * values_derivative[s_prime, j] for s_prime in range(N)])
                for state in range(N):
                    Z[state] = sum(np.exp(beta * q_values[state]))
                for state in range(N):
                    for j in range(d):
                        Z_derivative[state, j] = beta * sum([np.exp(beta * q_values[state, action]) * q_val_derivative[state, action, j] \
                                                   for action in range(N_ACTIONS)])
                for state in range(N):
                    for action in range(N_ACTIONS):
                        policy[state, action] = np.exp(beta * q_values[state, action]) / Z[state]

                        for j in range(d):
                            policy_derivative[state, action, j] = (beta * Z[state] * np.exp(beta * q_values[state, action]) * \
                                q_val_derivative[state, action, j] - np.exp(beta * q_values[state, action]) * Z_derivative[state, j]) /\
                                (Z[state] ** 2)
                    values[state] = sum([policy[state, action] * q_values[state, action] for action in range(N_ACTIONS)])
                    values_derivative[state] = sum([q_values[state, action] * policy_derivative[state, action]  + \
                        policy[state, action] * q_val_derivative[state, action] for action in range(N_ACTIONS)])
                
                demo = demonstrations[i]
                for j in range(d):
                    for state, action in demo:
                        likelihood_derivative_full[i][j] += (1 / policy[state, action]) * policy_derivative[state, action, j]
                likelihood_derivative = likelihood_derivative_full[i]
            weights = weights + (alpha * likelihood_derivative)
        return weights / np.linalg.norm(weights)

def solve_paper_example():
    grid = np.zeros((5, 5))
    start = (0, 0)
    goal = (4, 4)
    black_squares = [(0, 2), (0, 4), (1, 0), (2, 2), (3, 0), (3, 4), (4, 2)]
    for i, j in black_squares:
        grid[i, j] = -1
    grid[goal] = 1

    # features: values of [black squares, background, goal]
    features = {-1:0, 0:1, 1:2}
    demo = [(0, 0), (0, 1), (1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (4, 3), (4, 4)]
    env = Environment(grid, start, goal)
    mlirl = MLIRL(env, [demo], features)
    print mlirl.solve()
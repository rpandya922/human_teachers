from __future__ import division
import numpy as np
import json
import readline
import pickle
import io
# [2, 3, 10, 14, 15, 16, 19, 24, 25, 26, 27, 28, 29, 30, 31, 32]
def prefilled_input(prompt, prefill=''):
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return raw_input(prompt)
   finally:
      readline.set_startup_hook()

file_name = prefilled_input(".pkl file to export: ", "./data/environments.pkl")
f = open(file_name, "rb")
envs = pickle.load(f)
f.close()

env_idxs = prefilled_input("Environments to export: ")
if env_idxs == "all":
    env_idxs = list(range(envs['num_envs']))
else:
    env_idxs = map(int, env_idxs.split(' '))
data = {}
for save_idx, idx in enumerate(env_idxs):
    env = envs['env_' + str(idx)]
    env.grid = np.array(env.grid)
    try:
        true_rewards = env.true_rewards
    except:
        true_rewards = [-1, -0.5, 0, 0.5, 1]
    grid_copy = np.copy(env.grid)
    for i in range(grid_copy.shape[0]):
        for j in range(grid_copy.shape[1]):
            if env.grid[i][j] == -1:
                # black
                grid_copy[i][j] = true_rewards[0]
            elif env.grid[i][j] == -0.5:
                # dark gray
                grid_copy[i][j] = true_rewards[1]
            elif env.grid[i][j] == 0:
                # gray
                grid_copy[i][j] = true_rewards[2]
            elif env.grid[i][j] == 0.5:
                # light gray
                grid_copy[i][j] = true_rewards[3]
            elif env.grid[i][j] == 1:
                # white
                grid_copy[i][j] = true_rewards[4]
    data['colors_' + str(save_idx)] = env.grid.tolist()
    data['rewards_' + str(save_idx)] = grid_copy.tolist()
    data['start_' + str(save_idx)] = env.start
    data['goal_' + str(save_idx)] = env.goal
    data['reward_values_' + str(save_idx)] = true_rewards
    data['living_reward_' + str(save_idx)] = env.living_reward
with open('./data/test.txt', 'w') as f:
    json.dump(data, f, sort_keys=True, ensure_ascii=False)

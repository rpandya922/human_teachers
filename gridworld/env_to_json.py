from __future__ import division
import numpy as np
import json
import readline
import pickle
import io

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
for idx in env_idxs:
    env = envs['env_' + str(idx)]
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
    data['colors_' + str(idx)] = env.grid
    data['rewards_' + str(idx)] = grid_copy.tolist()
with open('./data/test.txt', 'w') as f:
    json.dump(data, f, sort_keys=True, ensure_ascii=False)

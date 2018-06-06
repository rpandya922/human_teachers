from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from environment import Environment
import readline
import pickle

def prefilled_input(prompt, prefill=''):
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return raw_input(prompt)
   finally:
      readline.set_startup_hook()
if prefilled_input("New file? ", "n") == "y":
    file_name = prefilled_input("file name: ", "./data/new_environments.pkl")
    f = open(file_name, "wb")
    pickle.dump({'num_envs': 0, 'interesting_envs': []}, f)
    f.close()
else:
    file_name = prefilled_input("file to open: ", "./data/new_environments.pkl")

env = Environment()
env.create_grid()
env.add_path(0)
env.add_path(1)
env.add_path(2)
print env.grid
print env.start
print env.goal
print env.living_reward
print env.paths
print env.horizon
save = raw_input("Save [y/n]? ")
if save == "y":
    f = open(file_name, "rb")
    envs = pickle.load(f)
    f.close()

    i = envs['num_envs']
    envs['env_' + str(i)] = env
    envs['interesting_envs'].append(i)
    envs['num_envs'] = envs['num_envs'] + 1
    f = open(file_name, "wb")
    pickle.dump(envs, f)
    f.close()

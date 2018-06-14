from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from environment import Environment
import pickle
import readline

def prefilled_input(prompt, prefill=''):
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return raw_input(prompt)
   finally:
      readline.set_startup_hook()

file_name = prefilled_input(".pkl file to load: ", "./data/environments.pkl")

f = open(file_name, "rb")
envs = pickle.load(f)
f.close()
# env idxs to edit [14 16 19  2  3 10 15 18 22 23]
env_idx = prefilled_input("environment number to edit: ")
env = envs['env_' + str(env_idx)]
fig, ax = plt.subplots()
env.show_grid(ax)
plt.pause(0.01)

living_reward = float(prefilled_input("living reward: ", str(env.living_reward)))
env.living_reward = living_reward
time_horizon = prefilled_input("time horizon: ")
env.horizon = time_horizon

true_rewards = raw_input("Color rewards [black, dark gray, gray, light gray, white]: ")
if true_rewards:
    true_rewards = map(float, true_rewards.split(' '))
else:
    true_rewards = [-1, -0.5, 0, 0.5, 1]
env.true_rewards = true_rewards
for i in range(len(env.paths)):
    if env.paths['path_' + str(i)] == []:
        env.add_path(i)
        continue
    env.show_path(ax, i)
    plt.pause(0.01)
    if prefilled_input("edit path " + str(i) + "? ") == "y":
        env.add_path(i)
env.show_all_paths(ax)
if prefilled_input("save? ") == "y":
    f = open(file_name, "wb")
    pickle.dump(envs, f)
    f.close()
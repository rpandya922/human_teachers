from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import pickle
import Math
from utils import *
from environment import Environment

T = 20

file_name = "./data/environments.pkl"
f = open(file_name, "rb")
envs = pickle.load(f)
f.close()

# optimization variable: (x1,...,xT,u0,...,uT-1)
# x: box idx?
# u: 0-3 action

def index_to_ij(idx):
    i = Math.floor(idx / m)
    j = idx % n
    return (i, j)
def ij_to_index(i, j):
    return (i * n) + j

constraints = []
for i in range(T):
    def dyn_constraint(x, i=i):
        state = index_to_ij(Math.round(x[i]))
        action_idx = i + T
        action = Math.round(x[action_idx])
        
    constraints.append(dyn_constraint)

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import OneClassSVM
from kde_classifier import OneClassKDEClassifier
from utils import *

h1 = 0.01
h2 = 1e-3

def get_training_points():
    points = np.array([[0.5, 0],
                       [-0.5, 0],
                       [-0.8, 0],
                       [0.8, 0],
                       [0.2, 0],
                       [-0.2, 0],
                       [0.5, 0.3],
                       [-0.5, 0.3],
                       [-0.5, -0.3],
                       [0.5, -0.3]])
    return points
def get_training_points2():
    points = np.array([[0.5, 0],
                       [-0.5, 0]])
    return points
def train_and_plot(h, training_points, rule):
    # svm = OneClassSVM(kernel='rbf', gamma=gamma)
    kde = OneClassKDEClassifier(h=h)
    kde.fit(training_points)

    fig, axes = plt.subplots(ncols=1, nrows=1, subplot_kw={'aspect':'equal'})
    axes = np.ndarray.flatten(np.array(axes))
    ax = axes[0]

    visualize(kde, ax)
    ax.scatter(training_points[:,0], training_points[:,1], c='g')
    ax.set_title(accuracy(kde, rule))
def plot_rule_1():
    fig, ax1 = plt.subplots(nrows=1, ncols=1, subplot_kw={'aspect':'equal'})
    ax1 = np.ndarray.flatten(np.array(ax1))
    ax1 = ax1[0]
    visualize_rule(ax1, decision_rule)

    training_points1 = np.array([[0, 0.2], [0, -0.2], [0, 0.4], [0, -0.4],
                                 [-0.1, 0.3], [0.1, 0.3], [-0.1, -0.3],
                                 [0.1, -0.3]])
    xx, yy = np.mgrid[-0.3:0.3:10j, -0.6:0.6:20j]
    points = np.vstack([xx.ravel(), yy.ravel()]).T
    training_points2 = []
    for point in points:
        if (point[0] - 0)**2 + (point[1] - 0.3)**2 <= 0.3**2 or \
            (point[0] - 0)**2 + (point[1] + 0.3)**2 <= 0.3**2:
            training_points2.append(point)
    training_points2 = np.array(training_points2)

    train_and_plot(h1, training_points1, decision_rule)
    train_and_plot(h2, training_points2, decision_rule)
    plt.show()
def plot_rule_2():
    fig, ax1 = plt.subplots(nrows=1, ncols=1, subplot_kw={'aspect':'equal'})
    ax1 = np.ndarray.flatten(np.array(ax1))
    ax1 = ax1[0]
    visualize_rule(ax1, decision_rule2)

    training_points1 = np.array([[0, 0]])
    xx, yy = np.mgrid[-0.2:0.2:5j, -0.2:0.2:5j]
    points = np.vstack([xx.ravel(), yy.ravel()]).T
    training_points2 = []
    for point in points:
        if point[0]**2 + point[1]**2 <= 0.2**2:
            training_points2.append(point)
    training_points2 = np.array(training_points2)

    train_and_plot(h1, training_points1, decision_rule2)
    train_and_plot(h2, training_points2, decision_rule2)
    plt.show()
def plot_rule_3():
    fig, ax1 = plt.subplots(nrows=1, ncols=1, subplot_kw={'aspect':'equal'})
    ax1 = np.ndarray.flatten(np.array(ax1))
    ax1 = ax1[0]
    visualize_rule(ax1, decision_rule3)

    training_points1 = np.array([[0, 0], [0, 0.4],
                                 [0, -0.4], [0.4, 0],
                                 [0.3, 0.3], [0.3, -0.3],
                                 [-0.4, 0], [-0.3, 0.3], [-0.3, -0.3]])
    xx, yy = np.mgrid[-0.6:0.6:15j, -0.6:0.6:15j]
    points = np.vstack([xx.ravel(), yy.ravel()]).T
    training_points2 = []
    for point in points:
        if point[0]**2 + point[1]**2 <= 0.6**2:
            training_points2.append(point)
    training_points2 = np.array(training_points2)

    train_and_plot(h1, training_points1, decision_rule3)
    train_and_plot(h2, training_points2, decision_rule3)
    plt.show()
plot_rule_3()

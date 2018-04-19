from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import OneClassSVM

def visualize(classifier, ax):
    xx, yy = np.mgrid[-1:1:100j, -1:1:100j]
    positions = np.vstack([xx.ravel(), yy.ravel()])
    y_vals = classifier.predict(positions.T)
    ax.scatter(positions[0], positions[1], c=y_vals)
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
    points = np.array([[0.8, 0],
                       [-0.8, 0]])
    return points
def visualize_rule(ax):
    xx, yy = np.mgrid[-1:1:100j, -1:1:100j]
    positions = np.vstack([xx.ravel(), yy.ravel()])
    y_vals = [decision_rule(point) for point in positions.T]
    ax.scatter(positions[0], positions[1], c=y_vals)
def decision_rule(point):
    if (point[0] - 0.5)**2 + (point[1] - 0)**2 <= 0.3**2:
        return 1
    elif (point[0] + 0.5)**2 + (point[1] - 0)**2 <= 0.3**2:
        return 1
    return 0
def train_and_plot(gamma, training_points):
    svm = OneClassSVM(kernel='rbf', gamma=gamma)
    svm.fit(training_points)

    fig, axes = plt.subplots(ncols=1, nrows=1)
    axes = np.ndarray.flatten(np.array(axes))
    ax = axes[0]

    visualize(svm, ax)
    ax.scatter(training_points[:,0], training_points[:,1], c='g')

fig, ax1 = plt.subplots(nrows=1, ncols=1)
ax1 = np.ndarray.flatten(np.array(ax1))
ax1 = ax1[0]
visualize_rule(ax1)

train_and_plot(1, get_training_points2())
train_and_plot(4, get_training_points())
plt.show()

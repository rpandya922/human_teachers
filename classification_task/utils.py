from __future__ import division
import numpy as np

def visualize(classifier, ax):
    xx, yy = np.mgrid[-1:1:100j, -1:1:100j]
    positions = np.vstack([xx.ravel(), yy.ravel()])
    y_vals = classifier.predict(positions.T)
    ax.scatter(positions[0], positions[1], c=y_vals)
def visualize_rule(ax, rule):
    xx, yy = np.mgrid[-1:1:100j, -1:1:100j]
    positions = np.vstack([xx.ravel(), yy.ravel()])
    y_vals = [rule(point) for point in positions.T]
    ax.scatter(positions[0], positions[1], c=y_vals)
def accuracy(classifier, rule):
    xx, yy = np.mgrid[-1:1:100j, -1:1:100j]
    test_points = np.vstack([xx.ravel(), yy.ravel()]).T
    true_labels = np.array([rule(p) for p in test_points])
    predictions = np.clip(classifier.predict(test_points), a_min=0, a_max=None)
    return np.sum(predictions == true_labels) / len(true_labels)
def decision_rule(point):
    if (point[0] - 0)**2 + (point[1] - 0.3)**2 <= 0.3**2:
        return 1
    elif (point[0] - 0)**2 + (point[1] + 0.3)**2 <= 0.3**2:
        return 1
    return 0
def decision_rule2(point):
    if point[0]**2 + point[1]**2 <= 0.2**2:
        return 1
    return 0
def decision_rule3(point):
    if point[0]**2 + point[1]**2 <= 0.6**2:
        return 1
    return 0
def decision_rule4(point):
    if (point[0] - 0.5)**2 + (point[1] - 0)**2 <= 0.3**2 or \
       (point[0] + 0.5)**2 + (point[1] - 0)**2 <= 0.3**2:
        return 1
    return 0
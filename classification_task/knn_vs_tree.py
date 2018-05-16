from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

def visualize(classifier, ax):
    xx, yy = np.mgrid[-1:1:100j, -1:1:100j]
    positions = np.vstack([xx.ravel(), yy.ravel()])
    # y_vals = classifier.predict_proba(positions.T)[:,1]
    y_vals = classifier.predict(positions.T)
    ax.scatter(positions[0], positions[1], c=y_vals)
def visualize_rule(ax):
    xx, yy = np.mgrid[-1:1:100j, -1:1:100j]
    positions = np.vstack([xx.ravel(), yy.ravel()])
    y_vals = [decision_rule(point) for point in positions.T]
    ax.scatter(positions[0], positions[1], c=y_vals)
def decision_rule(point):
    if np.array(point).dot([-1, 1]) >= 0:
        return 1
    return 0
def get_knn_points():
    points = np.array([[-0.5, 0.5],
                       [0.5, -0.5]])
    return points, [decision_rule(p) for p in points]
def get_tree_points():
    points = np.array([[-0.9, -1],
                       [-0.9, -0.8],
                       [-0.8, -0.9],
                       [-0.8, -0.7],
                       [-0.7, -0.8],
                       [-0.7, -0.6],
                       [-0.6, -0.7],
                       [-0.6, -0.5],
                       [-0.5, -0.6],
                       [-0.5, -0.4],
                       [-0.4, -0.5],
                       [-0.4, -0.3],
                       [-0.3, -0.4],
                       [-0.3, -0.2],
                       [-0.2, -0.3],
                       [-0.2, -0.1],
                       [-0.1, -0.2],
                       [-0.1, 0.00],
                       [0.9, 1],
                       [0.9, 0.8],
                       [0.8, 0.9],
                       [0.8, 0.7],
                       [0.7, 0.8],
                       [0.7, 0.6],
                       [0.6, 0.7],
                       [0.6, 0.5],
                       [0.5, 0.6],
                       [0.5, 0.4],
                       [0.4, 0.5],
                       [0.4, 0.3],
                       [0.3, 0.4],
                       [0.3, 0.2],
                       [0.2, 0.3],
                       [0.2, 0.1],
                       [0.1, 0.2],
                       [0.1, 0.00]])
    return points, [decision_rule(p) for p in points]

classifiers = [KNeighborsClassifier(n_neighbors=1), DecisionTreeClassifier()]

points = [get_knn_points()[0], get_tree_points()[0]]
labels = [get_knn_points()[1], get_tree_points()[1]]

fig, axes = plt.subplots(nrows=2, ncols=2)

for i in range(len(classifiers)):
    for j in range(len(points)):
        ax = axes[i][j]
        classifier = classifiers[i]

        classifier.fit(points[j], labels[j])
        visualize(classifier, ax)
        ax.scatter(points[j][:,0], points[j][:,1])
plt.show()

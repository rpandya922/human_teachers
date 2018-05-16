from __future__ import division
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from kde_classifier import KDEClassifier
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal as mvn
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier

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
def decision_rule3(point):
    if point[0] + point[1] >= 0:
        return 1
    else:
        return 0
def decision_rule2(point):
    if point[0] >= 0 and point[1] >= 0:
        return 1
    elif point[0] <= 0 and point[1] <= 0:
        return 1
    return 0
def decision_rule(point):
    if point[0]**2 + point[1]**2 <= 0.3**2:
        return 1
    return 0
def probability_examples(examples, labels, classifier):
    probs = classifier.predict_proba(examples)[np.arange(len(labels)), labels]
    return np.prod(probs)
def prob_theta(examples, labels, classifier, prior):
    return prior * probability_examples(examples, labels, classifier)
def update_prior(examples, labels, classifiers, prior):
    posterior = [prob_theta(examples, labels, classifiers[i], prior[i]) for i in range(len(prior))]
    return np.array(posterior) / np.sum(posterior)

def best_knn_examples():
    demonstrations = np.array([[0, 0],
                               [0.1, 0],
                               [-0.1, 0],
                               [0, 0.1],
                               [0.5, 0],
                               [-0.5, 0],
                               [0, 0.5],
                               [0, -0.5]])
    y = [decision_rule(p) for p in demonstrations]
    return demonstrations, y

probability_theta = [0.5, 0.5]
axes_limits = ((-1, 1), (-1, 1))

# neigh = KDEClassifier(h=0.1)
neigh = KNeighborsClassifier(n_neighbors=1)
tree = MLPClassifier()

dem1 = (0.5, 0.5)
l1 = decision_rule(dem1)
dem2 = (0.5, -0.7)
l2 = decision_rule(dem2)
# dem3 = (-1, -0.5)
# l3 = decision_rule(dem3)
# dem4 = (-0.6, 0.2)
# l4 = decision_rule(dem4)
dem3 = (-0.6, -0.5)
l3 = decision_rule(dem3)
dem4 = (-0.7, 0.5)
l4 = decision_rule(dem4)
dem5 = (0, 0.5)
l5 = decision_rule(dem5)
dem6 = (0, 0)
l6 = decision_rule(dem6)
demonstrations = np.array([dem1, dem2, dem3, dem4, dem5, dem6])
y = [l1, l2, l3, l4, l5, l6]

neigh.fit(demonstrations, y)
tree.fit(demonstrations, y)

xx, yy = np.mgrid[-1:1:50j, -1:1:50j]
test_points = np.vstack([xx.ravel(), yy.ravel()]).T

# e = max(test_points, key=lambda x: abs(prob_theta([x], neigh.predict([x]), neigh, 0.5) - 
#     prob_theta([x], neigh.predict([x]), tree, 0.5)))

# print neigh.predict([e])
# print tree.predict([e])
fig, axes = plt.subplots(nrows=1, ncols=2)
axes = np.ndarray.flatten(np.array(axes))
visualize(neigh, axes[0])
visualize(tree, axes[1])
# axes[0].scatter(e[0], e[1], c='r', label='calculated example')
# axes[1].scatter(e[0], e[1], c='r', label='calculated example')

axes[0].scatter(demonstrations[:,0], demonstrations[:,1], c='g', label='given demonstrations')
axes[1].scatter(demonstrations[:,0], demonstrations[:,1], c='g', label='given demonstrations')

# print update_prior([e], [decision_rule(e)], [neigh, tree], probability_theta)

fig2, axes2 = plt.subplots(nrows=1, ncols=1)
axes2 = np.ndarray.flatten(np.array(axes2))
visualize_rule(axes2[0])
# axes2[0].scatter(e[0], e[1], c='r', label='calculated example')
axes2[0].scatter(demonstrations[:,0], demonstrations[:,1], c='g', label='given demonstrations')

axes[0].legend()
axes[1].legend()
axes2[0].legend()
plt.show()
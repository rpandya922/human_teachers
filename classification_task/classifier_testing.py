from __future__ import division
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from kde_classifier import KDEClassifier
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal as mvn

def visualize(classifier, ax):
    xx, yy = np.mgrid[-1:1:100j, -1:1:100j]
    positions = np.vstack([xx.ravel(), yy.ravel()])
    y_vals = classifier.predict(positions.T)
    ax.scatter(positions[0], positions[1], c=y_vals)
def decision_rule(point):
    if point[0] >= 0 and point[1] >= 0:
        return 1
    elif point[0] <= 0 and point[1] <= 0:
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
probability_theta = [0.5, 0.5]
axes_limits = ((-1, 1), (-1, 1))

neigh = KDEClassifier(h=0.1)
tree = DecisionTreeClassifier()

dem1 = (0.5, 0.5)
l1 = decision_rule(dem1)
dem2 = (0.5, -0.5)
l2 = decision_rule(dem2)
dem3 = (-1, -0.5)
l3 = decision_rule(dem3)
demonstrations = np.array([dem1, dem2, dem3])
y = [l1, l2, l3]

neigh.fit(demonstrations, y)
tree.fit(demonstrations, y)

xx, yy = np.mgrid[-1:1:50j, -1:1:50j]
test_points = np.vstack([xx.ravel(), yy.ravel()]).T

e = max(test_points, key=lambda x: prob_theta([x], [decision_rule(x)], neigh, 0.5) - 
    prob_theta([x], [decision_rule(x)], tree, 0.5))
print neigh.predict([e])
print tree.predict([e])
fig, axes = plt.subplots(nrows=1, ncols=2)
axes = np.ndarray.flatten(np.array(axes))
visualize(neigh, axes[0])
visualize(tree, axes[1])
axes[0].scatter(e[0], e[1], c='r')
axes[1].scatter(e[0], e[1], c='r')
print update_prior([e], [decision_rule(e)], [neigh, tree], probability_theta)
plt.show()
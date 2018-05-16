from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import OneClassSVM
from kde_classifier import OneClassKDEClassifier
from utils import *

h = 0.001
gamma = 10

def accurary(classifier, rule):
    test_points = random_training_points(rule, 1000)
    true_labels = np.array([rule(p) for p in test_points])
    predictions = np.clip(classifier.predict(test_points), a_min=0, a_max=None)
    return np.sum(predictions == true_labels) / len(true_labels)
def random_training_points(decision_rule, n):
    initial_points = np.random.uniform(-1, 1, size=(n*2, 2))
    points = []
    for point in initial_points:
        if decision_rule(point) and len(points) <= n:
            points.append(point[:])
    while len(points) <= n:
        point = np.random.uniform(-1, 1, size=(2,))
        if decision_rule(point):
            points.append(point)
    return np.array(points)
def train_and_plot(h, training_points, rule, classifier):
    if classifier == 'svm':
        c = OneClassSVM(kernel='rbf', gamma=h)
    elif classifier == 'kde':
        c = OneClassKDEClassifier(h=h)
    c.fit(training_points)

    fig, axes = plt.subplots(ncols=1, nrows=1, subplot_kw={'aspect':'equal'})
    axes = np.ndarray.flatten(np.array(axes))
    ax = axes[0]

    visualize(c, ax)
    ax.scatter(training_points[:,0], training_points[:,1], c='g')
    ax.set_title(accuracy(c, rule))
def train(h, training_points, rule, classifier):
    if classifier == 'svm':
        c = OneClassSVM(kernel='rbf', gamma=h)
    elif classifier == 'kde':
        c = OneClassKDEClassifier(h=h)
    c.fit(training_points)
    return accuracy(c, rule)
visualize_rule(plt.subplots(subplot_kw={'aspect':'equal'})[1], decision_rule3)

# training_points = random_training_points(decision_rule3, 20)
# train_and_plot(gamma, training_points, decision_rule3, 'svm')
# train_and_plot(h, training_points, decision_rule3, 'kde')
# plt.show()
# 1/0

plt.figure(2)
svm_accuracies = []
kde_accuracies = []
for n in np.arange(1, 100, 2):
    dataset = random_training_points(decision_rule3, n)
    svm_accuracies.append(train(gamma, dataset, decision_rule3, 'svm'))
    kde_accuracies.append(train(h, dataset, decision_rule3, 'kde'))
plt.plot(np.arange(1, 100, 2), svm_accuracies, label='svm')
plt.plot(np.arange(1, 100, 2), kde_accuracies, label='kde')
plt.xlabel('Number of (random) training points')
plt.ylabel('Classifier Accuracy')
plt.legend()
plt.show()

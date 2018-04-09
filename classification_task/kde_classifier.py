from __future__ import division
import numpy as np
from scipy.stats import multivariate_normal as mvn

class KDEClassifier():
    def __init__(self, h):
        self.h = h

    def fit(self, X, y):
        self.classes_ = np.sort(np.unique(y))
        training_sets = [X[y == yi] for yi in self.classes_]
        ## currently only for binary classification
        self.X1 = training_sets[0]
        self.X2 = training_sets[1]
        self.prior1 = len(self.X1) / len(X)
        self.prior2 = len(self.X2) / len(X)

        return self
    def predict_proba(self, X):
        def kernel1(x):
            DOF = len(x)
            cov = np.diag(np.ones(DOF)) * self.h
            likelihoods = mvn.pdf(self.X1, mean=x, cov=cov)
            return np.sum(likelihoods) / len(self.X1)
        def kernel2(x):
            DOF = len(x)
            cov = np.diag(np.ones(DOF)) * self.h
            likelihoods = mvn.pdf(self.X2, mean=x, cov=cov)
            return np.sum(likelihoods) / len(self.X2)
        probs = []
        for x in X:
            p1 = kernel1(x)
            p2 = kernel2(x)
            probs.append([p1/(p1+p2), p2/(p1+p2)])
        return np.array(probs)
    def predict(self, X):
        return self.classes_[np.argmax(self.predict_proba(X), 1)]

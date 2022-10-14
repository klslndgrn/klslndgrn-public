import numpy as np
from scipy import misc
from importlib import reload
from labfuns import *
import random


# =============================================================================
# ==== Functions for Bayes Classifier =========================================
# =============================================================================
def computePrior(labels, W=None):
    """Calculating Priors.
    Input: Labels = N vector of class labels.
    Output: Prior = C x 1 vector of class priors."""
    Npts = labels.shape[0]
    if W is None:
        W = np.ones((Npts, 1)) / Npts
    else:
        assert W.shape[0] == Npts
    classes = np.unique(labels)  # Unique classes
    Nclasses = np.size(classes)  # Number of unique classes

    prior = np.zeros((Nclasses, 1))  # Precomuting matrix

    # Computing the values of prior for each class.
    for i, c in enumerate(classes):
        idx = np.where(labels == c)[0]
        prior[i] = np.sum(W[idx]) / np.sum(W[:])
    return prior


def mlParams(X, labels, W=None):
    """Calculating the Maximum-Likelihood of Parameters.
    Input: X = N x d matrix of N datapoints.
    Output 1: mu = C x d matrix of class means
    (mu[i] = class i mean).
    Output 2: sigma = C x d x d matrix of class covariances
    (sigma[i] = class i sigma)."""

    assert X.shape[0] == labels.shape[0]
    Npts, Ndims = np.shape(X)
    classes = np.unique(labels)
    Nclasses = np.size(classes)

    if W is None:
        W = np.ones((Npts, 1)) / float(Npts)

    # Computing mu and sigma:
    mu = np.zeros((Nclasses, Ndims))
    sigma = np.zeros((Nclasses, Ndims, Ndims))

    for i in range(Nclasses):
        # Computing mu
        idx = np.where(labels == i)[0]
        mu[i] = sum(X[idx, :] * W[idx, :]) / sum(W[idx, :])

        # Computing sigma
        ximu = X[idx, :] - mu[i]
        mean = sum(np.square(ximu) * W[idx, :]) / sum(W[idx, :])
        sigma[i] = np.diag(mean)

    return mu, sigma


def classifyBayes(X, prior, mu, sigma):
    """Classification Function.
    Input 1: X = N x d matrix of M data points.
    Input 2: prior = C x 1 matrix of class priors.
    Input 3: mu = C x d matrix of class means.
    Input 4: sigma = C x d x d matrix of class covariances.
    Output: h = N vector of class predictions for test points."""

    Npts = X.shape[0]
    Nclasses, Ndims = np.shape(mu)
    logProb = np.zeros((Nclasses, Npts))

    # Loop across class means
    for i in range(Nclasses):
        logsig = -1 / 2 * np.log(np.linalg.det(sigma[i]))
        logprior = np.log(prior[i])
        dxmu = X - mu[i]
        sigmainv = np.linalg.inv(sigma[i])
        # Loop across datapoints
        for j in range(Npts):
            dxmusig = -1 / 2 * np.dot(np.dot(dxmu[j], sigmainv), np.transpose(dxmu[j]))
            logProb[i][j] = logsig + dxmusig + logprior

    h = np.argmax(logProb, axis=0)
    return h


# =============================================================================
# ==== Bayes Classifier =======================================================
# =============================================================================
class BayesClassifier(object):
    """Bayes Classifier Class"""

    def __init__(self):
        self.trained = False

    def trainClassifier(self, X, labels, W=None):
        rtn = BayesClassifier()
        rtn.prior = computePrior(labels, W)
        rtn.mu, rtn.sigma = mlParams(X, labels, W)
        rtn.trained = True
        return rtn

    def classify(self, X):
        return classifyBayes(X, self.prior, self.mu, self.sigma)


# =============================================================================
# ==== Testing the Maximum Likelihood estimates ===============================
# =============================================================================
# Call "genBlobs()" and "plotGaussian()" to verify estimates.
X, labels = genBlobs(centers=5)
mu, sigma = mlParams(X, labels)
plotGaussian(X, labels, mu, sigma)


# =============================================================================
# ==== Call testing functions =================================================
# =============================================================================
# Call the `testClassifier` and `plotBoundary` functions for this part.

# testClassifier(BayesClassifier(), dataset="iris", split=0.7)

# testClassifier(BayesClassifier(), dataset='vowel', split=0.7)

# plotBoundary(BayesClassifier(), dataset='iris',split=0.7)


# =============================================================================
# ==== Boosting Functions =====================================================
# =============================================================================
def trainBoost(base_classifier, X, labels, T=10):
    """Boosting the Classifier.
    Input 1: base_classifier = a classifier of the type that will be boosted.
    Input 2: X = N x d matrix of N datapoints.
    Input 3: labels = N vector of class labels.
    Input 4: T = number of boosting iterations.
    Output 1: classifiers = (maximum) length T Python list of trained
    classifiers.
    Output 2: alphas = (maximum) length T Python list of vote weights."""
    # these will come in handy later on
    Npts, Ndims = np.shape(X)

    classifiers = []  # append new classifiers to this list
    alphas = []  # append the vote weight of the classifiers to this list

    # The weights for the first iteration
    wCur = np.ones((Npts, 1)) / float(Npts)

    for i_iter in range(0, T):
        # A new classifier is trained given the current weights:
        classifiers.append(base_classifier.trainClassifier(X, labels, wCur))

        # Classification for each datapoint
        vote = classifiers[-1].classify(X)

        # Diracs Delta Function
        delta = np.reshape((vote == labels), (Npts, 1))

        # Computing error
        error = np.sum(wCur * (1 - delta)) + 1e-20

        # Voting weights. Low error -> Large voting weights.
        alpha = 1 / 2 * (np.log(1 - error) - np.log(error))
        alphaSign = (delta - 0.5) / (-0.5)

        # Updating weights:
        wCur = wCur * (np.exp(alphaSign * alpha))

        # Normalizing factor to ensure that sum of all eights = 1.
        Z = np.sum(wCur)
        wCur /= Z

        # Append new alpha
        alphas.append(alpha)

    return classifiers, alphas


# in:       X - N x d matrix of N data points
# classifiers - (maximum) length T Python list of trained classifiers as above
#      alphas - (maximum) length T Python list of vote weights
#    Nclasses - the number of different classes
# out:  yPred - N vector of class predictions for test points
def classifyBoost(X, classifiers, alphas, Nclasses):
    Npts = X.shape[0]
    Ncomps = len(classifiers)

    # With only one classifier -> Classifying directly:
    if Ncomps == 1:
        return classifiers[0].classify(X)
    else:
        # Creating a mattix with weighted votes:
        votes = np.zeros((Npts, Nclasses))
        for i in range(Ncomps):
            classified = classifiers[i].classify(X)
            for j in range(Npts):
                votes[j][classified[j]] += alphas[i]

        return np.argmax(votes, axis=1)


# =============================================================================
# ==== Booster Class ==========================================================
# =============================================================================
class BoostClassifier(object):
    """Classifier Booster Class"""

    def __init__(self, base_classifier, T=10):
        self.base_classifier = base_classifier
        self.T = T
        self.trained = False

    def trainClassifier(self, X, labels):
        rtn = BoostClassifier(self.base_classifier, self.T)
        rtn.nbr_classes = np.size(np.unique(labels))
        rtn.classifiers, rtn.alphas = trainBoost(
            self.base_classifier, X, labels, self.T
        )
        rtn.trained = True
        return rtn

    def classify(self, X):
        return classifyBoost(X, self.classifiers, self.alphas, self.nbr_classes)


# =============================================================================
# ==== Running Experiments ====================================================
# =============================================================================
# Call the "testClassifier()" and "plotBoundary()" functions for this part.

print(" ")
print("====================================================================")
print("=== BAYES + IRIS ===================================================")
print("====================================================================")
print("Testing Bayes Classifier on Iris dataset:")
testClassifier(BayesClassifier(), dataset="iris", split=0.7)
print(" ")
print("Testing BOOSTED Bayes Classifier on Iris dataset:")
testClassifier(BoostClassifier(BayesClassifier(), T=10), dataset="iris", split=0.7)
plotBoundary(BayesClassifier(), dataset="iris", split=0.7)
plotBoundary(BoostClassifier(BayesClassifier()), dataset="iris", split=0.7)

print(" ")
print("====================================================================")
print("=== BAYES + VOWEL ==================================================")
print("====================================================================")
print("Testing Bayes Classifier on Vowel dataset:")
testClassifier(BayesClassifier(), dataset="vowel", split=0.7)
print(" ")
print("Testing BOOSTED Bayes Classifier on Wowel dataset:")
testClassifier(BoostClassifier(BayesClassifier(), T=10), dataset="vowel", split=0.7)

print(" ")
print("====================================================================")
print("=== DECTREE + IRIS =================================================")
print("====================================================================")
print("Testing Decision Tree Classifier on Iris dataset:")
testClassifier(DecisionTreeClassifier(), dataset="iris", split=0.7)
print(" ")
print("Testing BOOSTED Decision Tree Classifier on Iris dataset:")
testClassifier(
    BoostClassifier(DecisionTreeClassifier(), T=10), dataset="iris", split=0.7
)
plotBoundary(DecisionTreeClassifier(), dataset="iris", split=0.7)
plotBoundary(BoostClassifier(DecisionTreeClassifier(), T=10), dataset="iris", split=0.7)

print(" ")
print("====================================================================")
print("=== DECTREE + VOWEL ================================================")
print("====================================================================")
print("Testing Decision Tree Classifier on Vowel dataset:")
testClassifier(DecisionTreeClassifier(), dataset="vowel", split=0.7)
print(" ")
print("Testing BOOSTED Decision Tree Classifier on Vowel dataset:")
testClassifier(
    BoostClassifier(DecisionTreeClassifier(), T=10), dataset="vowel", split=0.7
)

# =============================================================================
# ==== Bonus: Visualize faces classified using boosted decision trees =========
# =============================================================================
# Note that this part of the assignment is completely voluntary!
# First, let's check how a boosted decision tree classifier performs on the
# olivetti data. Note that we need to reduce the dimension a bit using PCA, as
# the original dimension of the image vectors is `64 x 64 = 4096` elements.

# testClassifier(BayesClassifier(), dataset='olivetti',split=0.7, dim=20)

# testClassifier(BoostClassifier(DecisionTreeClassifier(), T=10), dataset='olivetti',split=0.7, dim=20)

# You should get an accuracy around 70%.
# If you wish, you can compare this with using pure decision trees or a boosted
# bayes classifier. Not too bad, now let's try and classify a face as belonging
# to one of 40 persons!

# X,y,pcadim = fetchDataset('olivetti') # fetch the olivetti data
# xTr,yTr,xTe,yTe,trIdx,teIdx = trteSplitEven(X,y,0.7) # split into training and testing
# pca = decomposition.PCA(n_components=20) # use PCA to reduce the dimension to 20
# pca.fit(xTr) # use training data to fit the transform
# xTrpca = pca.transform(xTr) # apply on training data
# xTepca = pca.transform(xTe) # apply on test data
# use our pre-defined decision tree classifier together with the implemented
# boosting to classify data points in the training data
# classifier = BoostClassifier(DecisionTreeClassifier(), T=10).trainClassifier(xTrpca, yTr)
# yPr = classifier.classify(xTepca)
# choose a test point to visualize
# testind = random.randint(0, xTe.shape[0]-1)
# visualize the test point together with the training points used to train
# the class that the test point was classified to belong to
# visualizeOlivettiVectors(xTr[yTr == yPr[testind],:], xTe[testind,:])

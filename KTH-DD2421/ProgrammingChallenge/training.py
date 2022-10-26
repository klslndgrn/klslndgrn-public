# =============================================================================
# ==== NEEDED LIBRARIES =======================================================
# =============================================================================

# ==== GENERAL ================================================================
import numpy as np
import pandas as pd

# ==== SKLEARN ================================================================
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.model_selection import (
    train_test_split,
    RandomizedSearchCV,
    GridSearchCV,
    cross_val_score,
)
from sklearn.ensemble import (
    RandomForestClassifier,
    AdaBoostClassifier,
    GradientBoostingClassifier,
    ExtraTreesClassifier,
    VotingClassifier,
    HistGradientBoostingClassifier,
)
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB, ComplementNB
from sklearn.neighbors import NearestCentroid, KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFECV

# ==== KERAS ==================================================================
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.utils import to_categorical

# ==== Other ==================================================================
# import xgboost as xgb
# import lightgbm as ltb
# import catboost as cb

# =============================================================================


# =============================================================================
# ==== EXTRACTING AND REMODELING (Y) CLASS LABELS =============================
# =============================================================================
def remodel_labels(df, Type):
    """Extracing class labels and performing One Hot Encoding. Returns a new
    dataframe containing binary class labels."""
    # ==== Extracting class labels to name columns ====
    names = list(np.unique(df["y"].values))
    names.sort()
    namestring = "-".join(names)
    # ==== PERFORMING ENCODING ====
    if Type is None:
        encoder = LabelEncoder()
        classes = encoder.fit_transform(df["y"])
        # ==== Creating a new dataframe ====
        dfy = pd.DataFrame(classes)
        dfy.columns = [namestring]  # type: ignore
    else:
        Y = df["y"].values.reshape(-1, 1)
        encoder = OneHotEncoder()
        classes = encoder.fit_transform(Y).toarray()
        dfy = pd.DataFrame(classes)
        dfy.columns = names  # type: ignore
    # ==== Returning dataframe ====
    return dfy, encoder


# =============================================================================
# ==== EXTRACTING (X) DATA SAMPLES ============================================
# =============================================================================
def extracting_samples(df):
    """Extracting data samples"""
    # ==== Creating a copy of the DataFrame and dropping the class column ====
    dfx = df.copy()
    dfx.drop("y", inplace=True, axis=1)
    # ==== Returning dataframe ====
    return dfx


# =============================================================================
# ==== CREATING DATAFRAMES FOR (X) AND (Y) ====================================
# =============================================================================
def creating_dfXY(df, Type):
    """Creating X and Y dataframes from the processed dataframe."""
    # ==== Extracting class labels (Y) ====
    dfy, encoder = remodel_labels(df, Type)
    # ==== Extracting data samples (X) ====
    dfx = extracting_samples(df)
    # ==== Returning DataFrames (X) and (Y) ====
    # print(dfy)
    # print(dfx)
    return dfx, dfy, encoder


# =============================================================================
# ==== CONVERTING DATAFRAMES TO ARRAYS ========================================
# =============================================================================
def creating_XY(df, Type=None):
    dfx, dfy, encoder = creating_dfXY(df, Type)
    Y = np.array(dfy)
    X = np.array(dfx)
    N = Y.shape[0]
    return X, Y, N, encoder


# =============================================================================
# ==== SPLITTING DATASET INTO TRAINING AND  TESTING ===========================
# =============================================================================
def splitting_dataset(X, Y, TestFrac, Split, Type=None):
    if Split is True:
        Xtrain, Xtest, Ytrain, Ytest = train_test_split(
            X, Y, test_size=TestFrac, random_state=None
        )
        if Type is None:
            Ytrain = np.ravel(Ytrain)
            Ytest = np.ravel(Ytest)
        else:
            pass
    else:
        if Type is None:
            Ytrain = np.ravel(Y)
        else:
            Ytrain = Y
        Xtrain = X
        Xtest = None
        Ytest = None
    return Xtrain, Ytrain, Xtest, Ytest


# =============================================================================
# ==== CLASSIFICATION FUNCTIONS ===============================================
# ==== SKLEARN ================================================================
# =============================================================================
def training_OVR(Xtrain, Ytrain):
    """Training OneVsRestClassifier."""
    clf = OneVsRestClassifier(LinearSVC())
    clf.fit(Xtrain, Ytrain)
    return clf


def training_SVC(Xtrain, Ytrain):
    """Training SupportVectorClassifier."""
    clf = SVC()
    clf.fit(Xtrain, Ytrain)
    return clf


def training_LSVC(Xtrain, Ytrain):
    """Training LinearSupportVectorClassifier."""
    clf = LinearSVC()
    clf.fit(Xtrain, Ytrain)
    return clf


def training_RF(Xtrain, Ytrain):
    """Training RandomForestClassifier."""
    clf = RandomForestClassifier(
        n_estimators=200,
        min_samples_split=10,
        min_samples_leaf=4,
        max_depth=10,
        bootstrap=True,
    )
    clf.fit(Xtrain, Ytrain)
    return clf


def training_ERT(Xtrain, Ytrain):
    """Training ExtraRandomTreesClassifier."""
    clf = ExtraTreesClassifier()
    clf.fit(Xtrain, Ytrain)
    return clf


def training_ADA(Xtrain, Ytrain):
    """Training AdaBoostClassifier."""
    clf = AdaBoostClassifier(n_estimators=150)
    clf.fit(Xtrain, Ytrain)
    return clf


def training_GB(Xtrain, Ytrain):
    """Training GradientBoostingClassifier."""
    clf = GradientBoostingClassifier(n_estimators=100)
    clf.fit(Xtrain, Ytrain)
    return clf


def training_HGB(Xtrain, Ytrain):
    """Training HistogramGradientBoostingClassifier."""
    clf = HistGradientBoostingClassifier()
    clf.fit(Xtrain, Ytrain)
    return clf


def training_MLP(Xtrain, Ytrain):
    """Training MultipleLayerPerceptronClassifier."""
    clf = MLPClassifier(max_iter=10000)
    clf.fit(Xtrain, Ytrain)
    return clf


def training_NB(Xtrain, Ytrain):
    """Training GaussianNaiveBayesClassifier."""
    clf = GaussianNB()
    clf.fit(Xtrain, Ytrain)
    return clf


def training_CNB(Xtrain, Ytrain):
    """Training ComplementNaiveBayesClassifier."""
    clf = ComplementNB()
    clf.fit(Xtrain, Ytrain)
    return clf


def training_kNC(Xtrain, Ytrain):
    """Training kNearestCentroidClassifier."""
    clf = NearestCentroid()
    clf.fit(Xtrain, Ytrain)
    return clf


def training_kNN(Xtrain, Ytrain):
    """Training kNearestNeighborClassifier."""
    clf = KNeighborsClassifier()
    clf.fit(Xtrain, Ytrain)
    return clf


def training_LR(Xtrain, Ytrain):
    """Training LogisticRegressionClassifier."""
    clf = LogisticRegression(max_iter=10000)
    clf.fit(Xtrain, Ytrain)
    return clf


def training_VOTE(Xtrain, Ytrain):
    """Training VotingClassifier, which uses RandomForest, GuassianNaiveBayes
    GradientBoosting, and MultiLayerPerceptron."""
    clf1 = RandomForestClassifier()
    clf2 = GaussianNB()
    clf3 = GradientBoostingClassifier()
    clf4 = MLPClassifier(max_iter=10000)
    clf5 = HistGradientBoostingClassifier()
    clf = VotingClassifier(
        estimators=[
            ("rf", clf1),
            ("gnb", clf2),
            ("gb", clf3),
            ("mlp", clf4),
            ("hgb", clf5),
        ],
        voting="hard",
    )
    clf.fit(Xtrain, Ytrain)
    return clf


# # ==== EXPERIMENTAL =========================================================
# def training_XGB(Xtrain, Ytrain):
#     """Training XGBoostingClassifier."""
#     clf = xgb.XGBClassifier(verbose=0)
#     clf.fit(Xtrain, Ytrain)
#     return clf


# def training_LGBM(Xtrain, Ytrain):
#     """Training LightGBMClassifier."""
#     clf = ltb.LGBMClassifier(verbose=0)
#     clf.fit(Xtrain, Ytrain)
#     return clf


# def training_CAT(Xtrain, Ytrain):
#     """Training XGBoostingClassifier."""
#     clf = cb.CatBoostClassifier(verbose=0)
#     clf.fit(Xtrain, Ytrain)
#     return clf


# ==== SUMMARY ================================================================
def regular_classifiers(Xtrain, Ytrain, Xtest, Ytest, TrainMany):
    """Testing multiple classfiers from SKLEARN library"""
    # ==============================
    # ==== TRAINING CLASSIFIERS ====
    # ==============================
    if Xtest is not None and TrainMany is True:
        # ==== OneVsRest Classifier ====
        OVRclf = training_OVR(Xtrain, Ytrain)
        # ==== SupportVector Classifier ====
        SVCclf = training_SVC(Xtrain, Ytrain)
        # ==== SupportVector Classifier ====
        LSVCclf = training_LSVC(Xtrain, Ytrain)
        # ==== RandomForest Classifier ====
        RFclf = training_RF(Xtrain, Ytrain)
        # ==== ExtraRandomTrees Classifier ====
        ERTclf = training_ERT(Xtrain, Ytrain)
        # ==== AdaBoos Classifier ====
        ADAclf = training_ADA(Xtrain, Ytrain)
        # ==== GradientBoosting Classifier ====
        GBclf = training_GB(Xtrain, Ytrain)
        # ==== GradientBoosting Classifier ====
        HGBclf = training_HGB(Xtrain, Ytrain)
        # ==== MultiLayerPerceptron Classifier (ANN) ====
        MLPclf = training_MLP(Xtrain, Ytrain)
        # ==== GaussianNaiveBayes Classifier ====
        NBclf = training_NB(Xtrain, Ytrain)
        # ==== ComplementNaiveBayes Classifier ====
        CNBclf = training_CNB(Xtrain, Ytrain)
        # ==== kNearestCentroid Classifier ====
        KNCclf = training_kNC(Xtrain, Ytrain)
        # ==== kNearestNeighbor Classifier ====
        KNNclf = training_kNN(Xtrain, Ytrain)
        # ==== LogisticRegression Classifier ====
        LRclf = training_LR(Xtrain, Ytrain)
        # ==== Voting Classifier ====
        VOTEclf = training_VOTE(Xtrain, Ytrain)
        # # ==== XGBoosting Classifier ====
        # XGBclf = training_XGB(Xtrain, Ytrain)
        # # ==== LightGBM Classifier ====
        # LGBMclf = training_LGBM(Xtrain, Ytrain)
        # # ==== LightGBM Classifier ====
        # CATclf = training_CAT(Xtrain, Ytrain)
        # ===============================
        # ==== SCORES OF CLASSIFIERS ====
        # ===============================
        print("\n=========================================")
        print("==== RESULTS ============================")
        print(f"Score of OneVsRest: {OVRclf.score(Xtest, Ytest):.4f}")
        print(f"Score of SupportVector: {SVCclf.score(Xtest, Ytest):.4f}")
        print(
            f"Score of LinearSupportVector: {LSVCclf.score(Xtest, Ytest):.4f}"
        )
        print(f"Score of RandomForest: {RFclf.score(Xtest, Ytest):.4f}")
        print(f"Score of ExtraRandomTrees: {ERTclf.score(Xtest, Ytest):.4f}")
        print(f"Score of AdaBoost: {ADAclf.score(Xtest, Ytest):.4f}")
        print(f"Score of GradientBoosting: {GBclf.score(Xtest, Ytest):.4f}")
        print(
            f"Score of HistGradientBoosting: {HGBclf.score(Xtest, Ytest):.4f}"
        )
        print(
            f"Score of MultiLayerPerceptron: {MLPclf.score(Xtest, Ytest):.4f}"
        )
        print(f"Score of GaussianNaiveBayes: {NBclf.score(Xtest, Ytest):.4f}")
        print(
            f"Score of ComplementNaiveBayes: {CNBclf.score(Xtest, Ytest):.4f}"
        )
        print(f"Score of kNearestCentroid: {KNCclf.score(Xtest, Ytest):.4f}")
        print(f"Score of kNearestNeighbor: {KNNclf.score(Xtest, Ytest):.4f}")
        print(f"Score of LogisticRegression: {LRclf.score(Xtest, Ytest):.4f}")
        print(f"Score of VotingClassifier: {VOTEclf.score(Xtest, Ytest):.4f}")
    # print(f"Score of XGBClassifier: {XGBclf.score(Xtest, Ytest):.4f}")
    # print(f"Score of LightGBMClassifier: {LGBMclf.score(Xtest, Ytest):.4f}")
    # print(f"Score of CatBoostClassifier: {CATclf.score(Xtest, Ytest):.4f}")
    else:
        # ==== GradientBoosting Classifier ====
        GBclf = training_GB(Xtrain, Ytrain)
    # ==== RETURNING BEST CLASSIFIER ====
    topCLF = GBclf
    return topCLF


# =============================================================================
# ==== CROSS-VALIDATIOn =======================================================
# =============================================================================
def cross_validation(clf, Xtrain, Ytrain):
    # cvclf = cross_validate(clf, Xtrain, Ytrain, cv=10)
    cvclfs = cross_val_score(clf, Xtrain, Ytrain, cv=18)
    cvclfs = np.mean(cvclfs)
    print(f"\nCross Validation of Classifier gives = {cvclfs:.4f}\n")


# =============================================================================
# ==== FINDING HYPERPARAMETERS ================================================
# =============================================================================
def tuning_parameters_randCV(clf, Xtrain, Ytrain):
    # Number of trees in random forest
    n_estimators = [int(x) for x in np.linspace(start=10, stop=2000, num=10)]
    # Maximum number of levels in tree
    max_depth = [int(x) for x in np.linspace(10, 110, num=11)]
    max_depth.append(None)  # type: ignore
    # Minimum number of samples required to split a node
    min_samples_split = [2, 5, 10]
    # Minimum number of samples required at each leaf node
    min_samples_leaf = [1, 2, 4]
    # Method of selecting samples for training each tree
    bootstrap = [True, False]
    random_grid = {
        "n_estimators": n_estimators,
        "max_depth": max_depth,
        "min_samples_split": min_samples_split,
        "min_samples_leaf": min_samples_leaf,
        "bootstrap": bootstrap,
    }
    rcv = RandomizedSearchCV(
        estimator=clf,
        param_distributions=random_grid,
        n_iter=100,
        cv=5,
        n_jobs=-1,
        return_train_score=True,
        verbose=1,
    )
    rcv.fit(Xtrain, Ytrain)
    print(f"\nRandomizedSearchCV results = \n{rcv.best_params_}")
    classifier = rcv
    return classifier


def tuning_parameters_gridCV(clf, Xtrain, Ytrain):
    """Tuning parameters."""
    # ==== GRADIENT BOOSTING ====
    random_grid_GB = {
        "loss": ["log_loss"],
        "learning_rate": [0.01, 0.025, 0.05, 0.075, 0.1, 0.15, 0.2],
        "min_samples_split": np.linspace(0.1, 0.5, 12),
        "min_samples_leaf": np.linspace(0.1, 0.5, 12),
        "max_depth": [3, 5, 8],
        "max_features": ["log2", "sqrt"],
        "criterion": ["friedman_mse", "mae"],
        "subsample": [0.5, 0.618, 0.8, 0.85, 0.9, 0.95, 1.0],
        "n_estimators": [100],
    }

    rcv = GridSearchCV(
        estimator=clf,
        param_grid=random_grid_GB,
        cv=5,
        n_jobs=-1,
        return_train_score=True,
        verbose=2,
    )
    rcv.fit(Xtrain, Ytrain)
    print(f"\nGridSearchCV results = \n{rcv.best_params_}")
    classifier = rcv
    return classifier


# =============================================================================
# ==== FEATURE SELECTION ======================================================
# =============================================================================
def dropping_attributes(Xtrain, Ytrain, Xtest, Ytest):
    """Dropping one attribute at a time and calculating score."""
    cols = np.shape(Xtrain)[1]
    for i in range(cols):
        Xtrain_c = np.delete(Xtrain, i, axis=1)
        Ytrain_c = Ytrain
        Xtest_c = np.delete(Xtest, i, axis=1)
        Ytest_c = Ytest
        clf = training_GB(Xtrain_c, Ytrain_c)
        s = clf.score(Xtest_c, Ytest_c)
        print(f"Score when removing column {i} is {s:.4f}")


def feature_selection(CLF, Xtrain, Ytrain, Xtest, Ytest):
    """Using a sklearn function for Feature Selection."""
    selector = RFECV(CLF, step=1, cv=5)
    selector = selector.fit(Xtrain, Ytrain)
    s = selector.score(Xtest, Ytest)
    supp = pd.DataFrame(np.transpose(selector.support_))
    rank = pd.DataFrame(np.transpose(selector.ranking_))
    rc = pd.concat([rank, supp], axis=1)
    rc.columns = ["Rank", "Support"]  # type: ignore
    print(f"Score when Feature Selection: {s:.4f}")
    print(f"Ranking the attributes (1 is best): \n{rc}\n")


def comparing_features(Xtrain, Ytrain, Xtest, Ytest):
    """Comparing regular classifier with the one using selected features."""
    # ==== TRAINING CLASSIFIER ====
    GBclf = training_GB(Xtrain, Ytrain)
    # ==== DROPPING ATTRIBUTES ====
    print("\n==== DROPPING ATTRIBUTES ============================")
    print(f"Original score: {GBclf.score(Xtest, Ytest):.4f}")
    dropping_attributes(Xtrain, Ytrain, Xtest, Ytest)
    # ==== FEATURE SELECTION ====
    print("\n==== FEATURE SELEECTION ============================")
    feature_selection(GBclf, Xtrain, Ytrain, Xtest, Ytest)


# =============================================================================
# ==== CLASSIFICATION FUNCTIONS ===============================================
# ==== KERAS ==================================================================
# =============================================================================
def keras_classification(Xtrain, Ytrain):
    """Keras DeepNeuralNetwork Classifier."""
    # ==== INPUT DIMENSIONS AND OUTPUT DIMENSIONS ====
    dim = np.shape(Xtrain)[1]
    out = len(np.unique(Ytrain))
    Ytrain = to_categorical(Ytrain, out)
    # ==== INPUT DATA ====
    model = Sequential()
    model.add(Dense(20, activation="relu", input_dim=dim))
    model.add(Dropout(0.11))
    model.add(Dense(24, activation="relu"))
    model.add(Dropout(0.11))
    model.add(Dense(24, activation="relu"))
    model.add(Dense(out, activation="softmax"))
    # ==== COMPILING THE MODEL ====
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    # ==== BUILDING THE MODEL ====
    model.fit(Xtrain, Ytrain, epochs=200, validation_split=0.2, verbose="0")
    # ==== RETURNING MODEL ====
    return model


def keras_evaulate(model, Xtest, Ytest):
    """Evaluating the DNN classifier."""
    # ==== OUTPUT DIMENSIONS ====
    out = len(np.unique(Ytest))
    Ytest = to_categorical(Ytest, out)
    # ==== EVALUATING MODEL ====
    score = model.evaluate(Xtest, Ytest)[1]
    return score

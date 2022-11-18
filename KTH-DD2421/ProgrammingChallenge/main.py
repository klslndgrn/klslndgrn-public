# =============================================================================
# ==== NEEDED LIBRARIES =======================================================
# =============================================================================
from pathlib import Path
from data_processing import import_training_data, import_evaluation_data
from training import (
    regular_classifiers,
    creating_XY,
    splitting_dataset,
    comparing_features,
    keras_classification,
    keras_evaulate,
    # tuning_parameters_randCV,
    # tuning_parameters_gridCV,
    cross_validation,
)
from classify import (
    predict_labels,
    label_conversion,
    save_prediction,
    most_common,
    comparison
)

# =============================================================================
# ==== FINDING ABSOLUTE PATH TO FOLDER ========================================
global PATH
PATH = script_location = Path(__file__).absolute().parent
# =============================================================================


def run_classification(Runs=10):
    """Run Programming Challenge and finding the most common label."""
    print("\n=======================================")
    print("==== PROGRAMMING CHALLENGE ============")
    print("=======================================")

    # ==== Run Classification ====
    for i in range(Runs):
        CLF, encoder = run_training()
        classdf = run_evaluation(CLF, encoder)
        save_prediction(classdf)
    # ==== Finding Most Common Label ====
    labeldf = most_common()
    return labeldf


# =============================================================================
# ==== MAIN TRAINING AND EVALUATION ===========================================
# =============================================================================
def run_training(TestFrac=0.2, Split=False, TrainMany=False):
    # ==== IMPORTING ENCODED TRANING DATA ====
    tdf = import_training_data(PATH)

    # ==== COMPARING CLASSIFIERS ====
    CLF, Xtrain, Ytrain, Xtest, Ytest, labels = run_classifiers(
        tdf, TestFrac, Split, TrainMany
    )

    # ==== CROSS-VALIDATION ====
    cross_validation(CLF, Xtrain, Ytrain)

    return CLF, labels


# =============================================================================
# ==== INDIVIDUAL FUNCTIONS ===================================================
# =============================================================================
def run_classifiers(tdf, TestFrac, Split, TrainMany):
    print("\n=======================================")
    print("==== TRAINING =========================")
    print("=======================================\n")
    # ==== IMPORTING ENCODED TRANING DATA ====
    X, Y, N, encoder = creating_XY(tdf)
    # ==== SPLITTING DATASETS INTO TRAIN/TEST ====
    Xtrain, Ytrain, Xtest, Ytest = splitting_dataset(X, Y, TestFrac, Split)
    # ==== COMPARING MULTIPLE CLASSIFYERS
    CLF = regular_classifiers(Xtrain, Ytrain, Xtest, Ytest, TrainMany)
    # ==== Returning Test/Train Arrays ====
    return CLF, Xtrain, Ytrain, Xtest, Ytest, encoder


def run_features(Xtrain, Ytrain, Xtest, Ytest):
    comparing_features(Xtrain, Ytrain, Xtest, Ytest)


def run_keras(tdf, TestFrac, Split):
    print("\n=======================================")
    print("==== TRAINING KERAS ===================")
    X, Y, N, encoder = creating_XY(tdf)
    # ==== IMPORTING ENCODED TRANING DATA ====
    Xtrain, Ytrain, Xtest, Ytest = splitting_dataset(X, Y, TestFrac, Split)
    # ==== SPLITTING DATASETS INTO TRAIN/TEST ====
    model = keras_classification(Xtrain, Ytrain)
    score = keras_evaulate(model, Xtest, Ytest)
    print(f"\n Score of Keras: {score:.4f}\n")


def run_evaluation(CLF, encoder):
    print("\n=========================================")
    print("==== EVALUATION =========================")
    print("=========================================\n")
    df = import_evaluation_data(PATH)
    Y = predict_labels(CLF, df)
    classdf = label_conversion(Y, encoder)
    return classdf


# =============================================================================
# ==== RUN MAIN CODE ==========================================================
# =============================================================================
if __name__ == "__main__":
    labeldf = run_classification(Runs=1)
    comparison(labeldf)


# ==== TUNING PARAMETERS ====
# clfx1 = tuning_parameters_randCV(CLF1, Xtrain, Ytrain)
# print(f"Score of optimized classifier = {clfx1.score(Xtest, Ytest):.4f}")
# clfx2 = tuning_parameters_gridCV(CLF2, Xtrain, Ytrain)
# print(f"Score of optimized classifier = {clfx2.score(Xtest, Ytest):.4f}")

# ==== FEATURE SELECTING ====
# run_features(Xtrain, Ytrain, Xtest, Ytest)

# ==== RUNNING KERAS CLASSIFIER ====
# run_keras(tdf, TestFrac, Split)

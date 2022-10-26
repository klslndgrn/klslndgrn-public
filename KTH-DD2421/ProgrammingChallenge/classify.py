from pathlib import Path
from os import path
import numpy as np
import pandas as pd


def predict_labels(CLF, df):
    """Predicting labels using selected classifier."""
    X = np.array(df)
    Y = CLF.predict(X)
    return Y


def label_conversion(Y, encoder):
    """Inversing the LabelEncoder to provide original labels."""
    classes = encoder.inverse_transform(Y)
    classes = pd.DataFrame(classes, columns=["Labels"])
    return classes


def save_prediction(classdf):
    """Save prediction to two files."""
    append_csv_data(classdf)
    save_csv_data(classdf)


def output_writer_directory(Type):
    """Finding output file directory path."""
    dir = Path(__file__).absolute().parent
    if Type == "Append":
        directory = dir / "predictions.csv"
    elif Type == "Save":
        directory = dir / "prediction.txt"
    else:
        directory = dir / "prediction_most-common.txt"
    return directory


def append_csv_data(df, Type="Append"):
    """Appending simulation results to a CSV to be able to find most commonly
    predicted label."""
    dir = output_writer_directory(Type)
    if path.exists(dir) is True:
        dfy = df.copy()
        dfx = pd.read_csv(dir)
        cols = list(range(dfx.shape[1]))
        dfx.columns = cols  # type: ignore
        dfy.columns = ["LATEST"]
        dfx.reset_index(drop=True, inplace=True)
        df = pd.concat([dfx, dfy], axis=1)
    else:
        pass
    df.to_csv(dir, mode="w", index=False, header=True, sep=",")


def save_csv_data(df, Type="Save"):
    """Save data to a text-file."""
    dir = output_writer_directory(Type)
    df.to_csv(dir, mode="w", index=False, header=False, sep=",")


def most_common(FromType="Append", ToType="MostCommon"):
    """Finding the most commmon label for each row in the CSV-file."""
    dir = output_writer_directory(FromType)
    fulldf = pd.read_csv(dir)
    common = fulldf.mode(axis=1)
    # ==== Dropping second column if there are a draw in most common ====
    if common.shape[1] >= 2:
        common.drop(1, inplace=True, axis=1)
    else:
        pass
    dir = output_writer_directory(ToType)
    common.to_csv(dir, mode="w", index=False, header=False, sep=",")
    common.columns = ["Predicted Labels"]
    print("\nThe final prediction of the labels are:")
    print("=========================================")
    print(common)
    print("=========================================\n")
    return common

# =============================================================================
# ==== NEEDED LIBRARIES =======================================================
# =============================================================================
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
from scipy import stats


# =============================================================================
# ==== IMPORTING RAW DATA =====================================================
# =============================================================================
def import_raw_data(PATH, DataType):
    """Importing raw training or evaulation data depening on DataType.
    DataType must be "Train" or "Evaulate"."""
    if DataType == "Train":
        print("\nImporting raw TRAINING data.\n")
        datafile = r"{}\TrainOnMe-4.csv".format(PATH)
        raw_df = pd.read_csv(datafile, index_col=0)
    elif DataType == "Evaluate":
        print("\nImporting raw EVALUATION data.\n")
        datafile = r"{}\EvaluateOnMe-4.csv".format(PATH)
        raw_df = pd.read_csv(datafile, index_col=0)
    else:
        raise ValueError('Define Data as "Train" or "Evaluate".')
    # ==== Returning values ====
    return raw_df


# =============================================================================
# ==== DATA FILTERING =========================================================
# =============================================================================
def filtering_nan(raw_df):
    """A function to remove samples containing NaN values."""
    # ==== Removing samples containing NaN values ====
    df = raw_df.dropna()
    nDf = len(df.index)
    nRaw = len(raw_df.index)
    diff = nRaw - nDf
    print(f"\nData is filtered. {diff} samples contining NaN are removed.\n")
    # ==== Returning values ====
    return df


def filtering_strings(df):
    """Filtering DataFrame to replace unwanted strings with NaN."""
    # ==== Columns to check ====
    cols = [
        "x1",
        "x2",
        "x3",
        "x4",
        "x5",
        "x6",
        "x8",
        "x9",
        "x10",
        "x11",
        "x13",
    ]
    # ==== Convert strings to numeric, which leads to strings being NaN ====
    df[cols] = df[cols].apply(pd.to_numeric, errors="coerce")
    # ==== Returning values ====
    return df


def filtering_data(df):
    """Filter data by removing unwanted strings and NaN-values."""
    # ==== Converting unwanted strings into NaN ====
    df = filtering_strings(df)
    # ==== Removing NaN ====
    df = filtering_nan(df)
    # ==== Returning values ====
    return df


# =============================================================================
# ==== EXTRACTING CHARACTERISTICS =============================================
# =============================================================================
def characteristics(df, DataType):
    """Displaying characteristics of imported data."""
    # ==== Finding Unique values and printing characteristics ====
    print("=======================================\n")
    if DataType == "Train":
        classes = unique_values(df, "y")
        ux7 = unique_values(df, "x7")
        ux12 = unique_values(df, "x12")
        # ==== Returning values ====
        return [ux7, ux12, classes]
    else:
        ux7 = unique_values(df, "x7")
        ux12 = unique_values(df, "x12")
        # ==== Returning values ====
        return [ux7, ux12]


def unique_values(df, string):
    """Finding Unique Values"""
    x = np.array(df[string])
    xU = list(np.unique(x))
    xU.sort()
    xDict = {}
    for i in xU:
        xDict[i] = np.count_nonzero(x == i)
    xDict = dict(sorted(xDict.items(), key=lambda item: item[1], reverse=True))
    print(f"Counting labels ({string}): {xDict}.\n")
    # ==== Returning values ====
    return xU


# =============================================================================
# ==== REPLACING DATA =========================================================
# =============================================================================
def replacing_data(df, DataType):
    """Replacing misspelled strings"""
    char = characteristics(df, DataType)
    ux7 = char[0]
    ux12 = char[1]
    if "chottis" in ux7:
        df = df.replace(
            "chottis",
            "Schottis",
        )
        print('Replacing "chottis" with "Schottis".')
    if "olka" in ux7:
        df = df.replace("olka", "Polka")
        print('Replacing "olka" with "polka".')
    if "YEP True" in ux12:
        df = df.replace("YEP True", "True")
        print('Replacing "YEP True" with "True".')
    if "YEP True" in ux12:
        df = df.replace("Nope False", "False")
        print('Replacing "Nope False" with "False".')
    # ==== Returning values ====
    return df


def boolean_to_int(df):
    """Replacing Boolean (True and False) with 1 and 0."""
    # ==== Replacing True with 1.0 ====
    df = df.replace("True", 1)
    # # ==== Replacing False with 0.0 ====
    df = df.replace("False", 0)
    df["x12"] = df["x12"].astype(float)
    # ==== Returning values ====
    print("Replacing True/False with 1/0.\n")
    return df


# =============================================================================
# ==== ENCODING DATA COLUMNS ==================================================
# =============================================================================
def one_hot_encoding(df):
    """One Hot Encoding of Dimension 7."""
    # ==== Converting into array and then performing one hot encoding ====
    X7 = df["x7"].values.reshape(-1, 1)
    # ==== OneHotEncoder() from sklearn ====
    oheX7 = OneHotEncoder().fit_transform(X7).toarray()
    print("One Hot Encoding (x7).\n")
    # ==== Returning values ====
    return oheX7


def one_hot_array(df):
    """One Hot Encoding of Labels."""
    # ==== Converting into array and then performing one hot encoding ====
    Y = df["y"].values.reshape(-1, 1)
    # ==== OneHotEncoder() from sklearn ====
    oheY = OneHotEncoder().fit_transform(Y).toarray()
    # ==== Returning values ====
    return oheY


# =============================================================================
# ==== MERGING DATA ===========================================================
# =============================================================================
def merge_dataframe(df, ohe, colnames):
    """Merging dataframe"""
    # ==== Removing x7 (being replaced with One Hot Encoder) ====
    df.drop("x7", inplace=True, axis=1)
    df.reset_index(drop=True, inplace=True)
    # ==== Creating dataframe from One Hot Encoder ====
    oheDF = pd.DataFrame(ohe, columns=colnames)
    oheDF.reset_index(drop=True, inplace=True)
    # ==== Merging dataframes ====
    df_new = pd.concat([df, oheDF], axis=1)
    heads = list(df_new.columns)
    # ==== Returning values ====
    return df_new, heads


# =============================================================================
# ==== FILTERING OUTLIERS =====================================================
# =============================================================================
def filtering_outliers(df):
    """Filtering for outliers using Z-score."""
    # ==== Removing label column ====
    yDF = df.pop("y")
    # ==== Finding indices where there is outliers ====
    idx = (np.abs(stats.zscore(df)) < 3).all(axis=1)
    # ==== Removing outliers and resetting indices ====
    dfs = df[idx]
    dfs.reset_index(drop=True, inplace=True)  # resetting indices
    # ==== Removing outliers and resetting indices ====
    yDFx = yDF[idx]
    yDFx.reset_index(drop=True, inplace=True)  # resetting indices
    # ==== Merging DataFrames into one ====
    df = pd.concat([yDFx, dfs], axis=1)
    # ==== Returning values ====
    return df


def filtering_outliers_eval(df):
    """Filtering for outliers using Z-score."""
    # ==== Finding indices where there is outliers ====
    idx = (np.abs(stats.zscore(df)) < 3).all(axis=1)
    # ==== Removing outliers and resetting indices ====
    dfs = df[idx]
    dfs.reset_index(drop=True, inplace=True)  # resetting indices
    # ==== Returning values ====
    return df


# =============================================================================
# ==== NORMALIZATION ==========================================================
# =============================================================================
def scaling_dataframe(df, heads, DataType):
    """Scaling dataframe between 0 and 1."""
    # ==== Depending on Train/Evaulation: ====
    if DataType == "Train":
        # ==== Removing label-column ====
        yDF = df.pop("y")
        # ==== Scaling dataframe ====
        df = pd.DataFrame(MinMaxScaler().fit_transform(df))
        # ==== Merging dataframes ====
        df = pd.concat([yDF, df], axis=1)
        df.columns = heads
    else:
        # ==== Scaling dataframe ====
        df = pd.DataFrame(MinMaxScaler().fit_transform(df))
        df.columns = heads
    # ==== Returning values ====
    return df


# =============================================================================
# ==== DATA PROCESSING ========================================================
# =============================================================================
def data_encoding(df, DataType):
    """Encoding data. (1.) Boolean to 1/0. (2.) One Hot Encoding. (3.)
    Normalizing. (4.) Merging DataFrames."""
    # ==== Converting boolean to 1/0 ====
    df = boolean_to_int(df)
    # ==== One Hot Encoding X7 ====
    oheX7 = one_hot_encoding(df)
    # ==== Finding Characteristics ====
    colnames = characteristics(df, DataType)[0]
    # ==== Merging One Hot Encoded data with previous data ====
    df, heads = merge_dataframe(df, oheX7, colnames)
    # ==== Depending on Train/Evaulation: ====
    if DataType == "Train":
        # ==== Filtering for outliers ====
        df = filtering_outliers(df)
    # elif DataType == "Evaluate":
    #     df = filtering_outliers_eval(df)
    else:
        pass
    # ==== Scaling dataframe between 0 and 1 ====
    df = scaling_dataframe(df, heads, DataType)
    # ==== Returning values ====
    return df


# =============================================================================
# ==== IMPORT TRAINING DATA ===================================================
# =============================================================================
def import_training_data(PATH):
    """Import and process training data"""
    # ==== Setting type =====
    DataType = "Train"
    # ==== Importing raw data =====
    r_df = import_raw_data(PATH, DataType)
    raw_df = r_df.copy()
    # ==== Filtering data and removing NaN values =====
    df = filtering_data(raw_df)
    # ==== Replacing misspelled data ====
    df = replacing_data(df, DataType)
    # ==== Data encoding ====
    df = data_encoding(df, DataType)
    # ==== Length differences ====
    dfN = df.shape[0]
    rdfN = r_df.shape[0]
    diffN = np.abs(dfN - rdfN)
    # ==== Returning values ====
    # print(f'Raw training data = \n{raw_df}')
    # print(f'Encoded training data = \n{df}')
    print(f'\nData processing results: {diffN} data samples removed.\n')
    return df


# =============================================================================
# ==== IMPORTING EVALUATION DATA ==============================================
# =============================================================================
def import_evaluation_data(PATH):
    """Import and process training data"""
    # ==== Setting type =====
    DataType = "Evaluate"
    # ==== Importing raw data =====
    r_df = import_raw_data(PATH, DataType)
    raw_df = r_df.copy()
    # ==== Data encoding ====
    df = data_encoding(raw_df, DataType)
    # ==== Length differences ====
    dfN = df.shape[0]
    rdfN = r_df.shape[0]
    diffN = np.abs(dfN - rdfN)
    # ==== Returning values ====
    # print(f'Raw evaluation data = \n{r_df}')
    # print(f'Encoded evaluation data = \n{df}')
    print(f'\nData processing results: {diffN} data samples removed.\n')
    return df

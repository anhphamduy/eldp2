import numpy as np
import pandas as pd
from sklearn import preprocessing


def normalise_data(x):
    if type(x) != np.array:
        x = np.array(x)
    return pd.Series(preprocessing.normalize(x[:, np.newaxis], axis=0).ravel())


def get_jaccard_sim(str1, str2):
    a = set(str1.split())
    b = set(str2.split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))

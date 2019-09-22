import numpy as np
import pandas as pd
from sklearn import preprocessing

import nltk


def normalise_number_data(x):
    if type(x) != np.array:
        x = np.array(x)
    return pd.Series(preprocessing.normalize(x[:, np.newaxis], axis=0).ravel())


def normalise_word_data(x):
    return x.applymap(nltk.stem.PorterStemmer().stem)


def get_jaccard_sim(str1, str2):
    a = set(str1.split())
    b = set(str2.split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))


def cross_join_dataframes(left, right):
    return (
        left.assign(key=1).merge(right.assign(key=1), on='key').drop('key', 1))

def get_gaussian_similarity(d, scale, origin=0):

    if scale <= 0:
        raise ValueError("The scale must be larger than 0. ")

    d = (abs(d - origin))

    expr = '2**(-((d)/scale)**2)'

    return pd.eval(expr)

def _get_multiindex(x):

    if isinstance(x, (pd.DataFrame, pd.Series)):
        return x.index
    elif isinstance(x, pd.MultiIndex):
        return x
    else:
        raise ValueError("Expected one of: pandas.DataFrame, "
                         "pandas.Series, pandas.MultiIndex")
        
        
def true_positives(links_true, links_pred):

    links_true = _get_multiindex(links_true)
    links_pred = _get_multiindex(links_pred)

    return len(links_true & links_pred)

def confusion_matrix(links_true, links_pred, total=None):
    """Compute the confusion matrix.
    The confusion matrix is of the following form:
    +----------------------+-----------------------+----------------------+
    |                      |  Predicted Positives  | Predicted Negatives  |
    +======================+=======================+======================+
    | **True Positives**   | True Positives (TP)   | False Negatives (FN) |
    +----------------------+-----------------------+----------------------+
    | **True Negatives**   | False Positives (FP)  | True Negatives (TN)  |
    +----------------------+-----------------------+----------------------+
    The confusion matrix is an informative way to analyse a prediction. The
    matrix can used to compute measures like precision and recall. The count
    of true prositives is [0,0], false negatives is [0,1], true negatives
    is [1,1] and false positives is [1,0].
    Parameters
    ----------
    links_true: pandas.MultiIndex, pandas.DataFrame, pandas.Series
        The true (or actual) links.
    links_pred: pandas.MultiIndex, pandas.DataFrame, pandas.Series
        The predicted links.
    total: int, pandas.MultiIndex
        The count of all record pairs (both links and non-links). When the
        argument is a pandas.MultiIndex, the length of the index is used. If
        the total is None, the number of True Negatives is not computed.
        Default None.
    Returns
    -------
    numpy.array
        The confusion matrix with TP, TN, FN, FP values.
    Note
    ----
    The number of True Negatives is computed based on the total argument.
    This argument is the number of record pairs of the entire matrix.
    """

    links_true = _get_multiindex(links_true)
    links_pred = _get_multiindex(links_pred)

    tp = true_positives(links_true, links_pred)
    fp = false_positives(links_true, links_pred)
    fn = false_negatives(links_true, links_pred)

    if total is None:
        tn = numpy.nan
    else:
        
        if isinstance(total, pandas.MultiIndex):
            total = len(total)
        tn = true_negatives(links_true, links_pred, total)

    return numpy.array([[tp, fn], [fp, tn]])

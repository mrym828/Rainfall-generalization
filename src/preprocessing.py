import numpy as np

def fit_standardizer(X_train):
    """
    Fit standardization parameters using training data only.

    Parameters:
    -----------
    X_train: np.ndarray

    Returns:
    ----------
    mean: np.ndarray
    std: np.ndarray
    """

    X_train = np.asarray(X_train, dtype= float)

    mean = np.mean(X_train, axis=0)
    std = np.std(X_train, axis=0)
    std = np.where(std == 0, 1.0, std)
    return mean, std

def transform_standardizer(X, mean, std):
    """
    Standardize features using previously fitted parameters
    """
    X = np.asarray(X, dtype=float)

    centered = X - mean
    X_scaled = centered / std

    return X_scaled


import numpy as np

from src.preprocessing import (
    fit_standardizer,
    transform_standardizer
)


def test_standardizer_training_data():

    X_train = np.array([
        [10, 100],
        [20, 200],
        [30, 300]
    ])

    mean, std = fit_standardizer(X_train)
    X_scaled = transform_standardizer(X_train, mean, std)

    assert np.allclose(
        np.mean(X_scaled, axis=0),
        np.zeros(2)
    )

    assert np.allclose(
        np.std(X_scaled, axis=0),
        np.ones(2)
    )


    assert X_scaled.shape == X_train.shape


def test_standardizer_no_data_leakage():

    X_train = np.array([
        [10, 100],
        [20, 200],
        [30, 300]
    ])

    X_test = np.array([
        [1000, 5000],
        [2000, 6000]
    ])

    mean, std = fit_standardizer(X_train)

    X_test_scaled = transform_standardizer(X_test, mean, std)

    assert np.allclose(mean, [20,200])

    expected = (X_test - mean) / std

    assert np.allclose(X_test_scaled, expected)

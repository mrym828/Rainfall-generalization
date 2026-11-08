import numpy as np
import pytest
from src.models.ridge_gd import RidgeRegressionGD


def test_ridge_gd_predictions():

    X_train = np.array([[1], [2], [3], [4]])
    y_train = np.array([2, 4, 6, 8])

    model = RidgeRegressionGD(
        learning_rate=0.05,
        iterations=1000,
        lambda_=0.1
    )

    model.fit(X_train, y_train)

    predictions = model.predict(
        np.array([[5], [6]])
    )

    expected = np.array([9.90179, 11.86249])

    assert np.allclose(predictions, expected, atol=1e-5)


def test_predict_before_fit():

    model = RidgeRegressionGD()

    with pytest.raises(ValueError):
        model.predict(np.array([[5]]))


def test_cost_decreases():

    X_train = np.array([[1], [2], [3], [4]])
    y_train = np.array([2, 4, 6, 8])

    model = RidgeRegressionGD(
        learning_rate=0.05,
        iterations=1000,
        lambda_=0.1
    )

    model.fit(X_train, y_train)

    assert model.cost_history[-1] < model.cost_history[0]


def test_regularization_strength():

    X = np.array([[1], [2], [3], [4]])
    y = np.array([2, 4, 6, 8])

    weak_model = RidgeRegressionGD(
        learning_rate=0.05,
        iterations=1000,
        lambda_=0.01
    )

    strong_model = RidgeRegressionGD(
        learning_rate=0.05,
        iterations=1000,
        lambda_=10.0
    )

    weak_model.fit(X, y)
    strong_model.fit(X, y)

    weak_weight = weak_model.theta[1]
    strong_weight = strong_model.theta[1]

    print("Weak regularization:", weak_weight)
    print("Strong regularization:", strong_weight)

    assert abs(strong_weight) < abs(weak_weight)


def test_gradient_correctness():

    X = np.array([
        [1.0, 1.0],
        [1.0, 2.0],
        [1.0, 3.0]
    ])

    y = np.array([2.0, 4.0, 6.0])

    model = RidgeRegressionGD(lambda_=0.1)
    model.theta = np.array([0.5, 1.5])

    m = len(y)
    epsilon = 1e-6

    errors = X @ model.theta - y

    theta_reg = model.theta.copy()
    theta_reg[0] = 0

    analytical = (
        (X.T @ errors) / m
        + (model.lambda_ / m) * theta_reg
    )

    numerical = np.zeros_like(model.theta)

    for j in range(len(model.theta)):
        original = model.theta[j]

        model.theta[j] = original + epsilon
        cost_plus = model.calculate_cost(X, y)

        model.theta[j] = original - epsilon
        cost_minus = model.calculate_cost(X, y)

        model.theta[j] = original

        numerical[j] = (
            cost_plus - cost_minus
        ) / (2 * epsilon)

    print("Analytical gradient:", analytical)
    print("Numerical gradient:", numerical)

    assert np.allclose(
        analytical,
        numerical,
        atol=1e-5
    )

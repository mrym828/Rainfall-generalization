
import numpy as np
import pytest

from src.models.random_forest import (
    DecisionTreeRegressor,
    RandomForest,
)


def test_regression_tree_split():
    """A depth-one tree should recover a simple known split."""
    X = np.array([[1], [2], [3], [7], [8], [9]], dtype=float)
    y = np.array([2, 3, 2.5, 12, 13, 12.5], dtype=float)

    tree = DecisionTreeRegressor(
        max_depth=1,
        random_state=42
    )
    tree.fit(X, y)

    assert tree.root.feature_idx == 0
    assert np.isclose(tree.root.threshold, 5.0)

    expected = np.array([2.5, 2.5, 12.5, 12.5])
    X_new = np.array([[1.5], [4], [6], [8.5]])

    assert np.allclose(tree.predict(X_new), expected)


def test_forest_prediction_shape():
    """Forest predictions should match the number of input rows."""
    X = np.arange(30, dtype=float).reshape(10, 3)
    y = np.arange(10, dtype=float)

    forest = RandomForest(
        n_estimators=5,
        max_depth=3,
        max_features=2,
        random_state=42
    )
    forest.fit(X, y)

    predictions = forest.predict(X)

    assert predictions.shape == (10,)
    assert np.isfinite(predictions).all()


def test_forest_reproducibility():
    """Identical seeds and data should produce identical predictions."""
    X = np.arange(30, dtype=float).reshape(10, 3)
    y = np.arange(10, dtype=float)

    params = dict(
        n_estimators=5,
        max_depth=3,
        max_features=2,
        random_state=42
    )

    forest_1 = RandomForest(**params).fit(X, y)
    forest_2 = RandomForest(**params).fit(X, y)

    assert np.allclose(
        forest_1.predict(X),
        forest_2.predict(X)
    )


def test_predict_before_fit():
    """An unfitted forest must reject prediction requests."""
    forest = RandomForest()

    with pytest.raises(ValueError):
        forest.predict(np.array([[1.0, 2.0]]))

import pandas as pd
from src.validation import manual_loso


def test_manual_loso():
    data = pd.DataFrame({
        "STATION": ["A", "A", "B", "B", "C", "C"],
        "RAINFALL": [0, 5, 2, 8, 0, 10]
    })

    folds = list(manual_loso(data))

    assert len(folds) == 3

    for station, train_df, test_df in folds:
        assert station not in train_df["STATION"].values
        assert (test_df["STATION"] == station).all()
        assert len(train_df) == 4
        assert len(test_df) == 2

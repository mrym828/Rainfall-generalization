import pandas as pd
from src.feature_engineering import create_rainfall_lags, create_lag_qc

def test_create_rainfall_lags():
    data = pd.DataFrame({
        'STATION': ['A', 'A', 'A', 'B','B','B'],
        'MONTH': pd.period_range('2020-01', periods=3, freq='M').tolist() * 2,
        'PRCP_TOTAL': [10,20,30,5,15,25]
    })

    result = create_rainfall_lags(data, max_lag=2)

    station_a = result[result['STATION'] == 'A'].reset_index(drop=True)
    station_b = result[result['STATION'] == 'B'].reset_index(drop=True)

    assert station_a['PRCP_LAG_0'].tolist() == [10,20,30]

    assert pd.isna(station_a.loc[0, "PRCP_LAG_1"])
    assert station_a.loc[1, "PRCP_LAG_1"] == 10
    assert station_a.loc[2, "PRCP_LAG_1"] == 20

    assert pd.isna(station_a.loc[0, "PRCP_LAG_2"])
    assert pd.isna(station_a.loc[1, "PRCP_LAG_2"])
    assert station_a.loc[2, "PRCP_LAG_2"] == 10

    assert station_b.loc[1, "PRCP_LAG_1"] == 5

def test_create_lag_qc():
    data = pd.DataFrame({
        "STATION": ["A", "A", "A", "A"],
        "MONTH": pd.period_range(
            "2020-01", periods=4, freq="M"
        ),
        "PRCP_COMPLETENESS": [100, 60, 100, 100],
        "ELIGIBLE_ALL_90": [True, True, True, True]
    })

    result = create_lag_qc(data, max_lag=2, threshold=90)

    assert result.loc[0, "LAG_QC_90"] == False
    assert result.loc[1, "LAG_QC_90"] == False

    assert result.loc[2, "LAG_QC_90"] == False
    assert result.loc[3, "LAG_QC_90"] == False

    assert result["ELIGIBLE_B_90"].sum() == 0
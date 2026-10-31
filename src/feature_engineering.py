import pandas as pd

def create_rainfall_lags(df, max_lag=2):
    """
    Create rainfall lag features for each station.

    - Lag 0: Current month's rainfall
    - Lag 1: Previous month's rainfall
    - Lag 2: Rainfall two months ago
    """

    result = df.sort_values(['STATION','MONTH']).copy()
    result['PRCP_LAG_0'] = result['PRCP_TOTAL']

    for lag in range(1, max_lag + 1):
        result[f'PRCP_LAG_{lag}'] = (
            result.groupby("STATION")['PRCP_TOTAL'].shift(lag)
        )

    return result

def create_lag_qc(df, max_lag=2, threshold=90):
    """
    Create rainfall lag completeness features and determine eligibility for Feature Set B.

    Assumes a complete station-month calendar.
    """

    result = df.sort_values(['STATION','MONTH']).copy()
    result['PRCP_QC_LAG_0'] = result['PRCP_COMPLETENESS']

    for lag in range(1, max_lag + 1):
        result[f'PRCP_QC_LAG_{lag}'] = (
            result.groupby('STATION')['PRCP_COMPLETENESS'].shift(lag)
        )
        
    lag_qc_columns = [
        f"PRCP_QC_LAG_{lag}"
        for lag in range(max_lag + 1)
    ]

    result['LAG_QC_90'] = (
        result[lag_qc_columns].ge(threshold).all(axis=1)
    )
    result['ELIGIBLE_B_90'] = (
        result['ELIGIBLE_ALL_90']
        & result['LAG_QC_90']
    )

    return result
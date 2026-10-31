
def manual_loso(df, station_col="STATION"):
    """
    This function generates a Leave-One-Station-Out cross-validation folds.

    Parameters:
    -----------
    df : pandas dataframe
    station_col : str

    Returns:
    -------
    tuple (test_station, train_df, test_df)
    """

    stations = sorted(df[station_col].unique())

    for test_station in stations:
        train_df = df[df[station_col] != test_station].copy()
        test_df = df[df[station_col] == test_station].copy()

        train_stations = set(train_df[station_col])
        test_stations = set(train_df[station_col])

        yield test_station, train_df, test_df
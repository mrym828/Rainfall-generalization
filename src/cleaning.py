import pandas as pd
import numpy as np

MISSING_CODES ={
    'PRCP': 99.99,
    'TEMP': 9999.9,
    'MAX': 9999.9,
    'MIN': 9999.9,
    'DEWP': 9999.9,
    'WDSP': 999.9,
    'MXSPD': 999.9,
    'VISIB': 999.9,
    'SLP': 9999.9
}

def replace_missing_values(df) -> pd.DataFrame:
    """
    Replace missing values in the DataFrame with NaN based on predefined missing codes.

    Parameters:
    df (pd.DataFrame): Input DataFrame containing weather data.

    Returns:
    pd.DataFrame: DataFrame with missing values replaced by NaN.
    """
    cleaned_df = df.copy()
    for column, missing_value in MISSING_CODES.items():
        if column in df.columns:
            cleaned_df[column] = cleaned_df[column].replace(missing_value, np.nan)
    return cleaned_df


def convert_units(df) -> pd.DataFrame:
    """
    Convert units of specific columns in the DataFrame.

    Parameters:
    df (pd.DataFrame): Input DataFrame containing weather data.

    Returns:
    pd.DataFrame: DataFrame with converted units.
    """
    converted_df = df.copy()
    
    # Convert temperature from F to degrees Celsius
    if 'TEMP'  in converted_df.columns:
        converted_df['TEMP'] = (converted_df['TEMP'] - 32) * 5/9
    if 'MAX' in converted_df.columns:
        converted_df['MAX'] = (converted_df['MAX'] - 32) * 5/9
    if 'MIN' in converted_df.columns:
        converted_df['MIN'] = (converted_df['MIN'] - 32) * 5/9
    if 'DEWP' in converted_df.columns:
        converted_df['DEWP'] = (converted_df['DEWP'] - 32) * 5/9

    # Convert precipitation from hundredths of inches to mm
    if 'PRCP' in converted_df.columns:
        converted_df['PRCP'] = converted_df['PRCP'] * 25.4  # Convert to mm

    # convert wind speed from knots to km/s
    if 'WDSP' in converted_df.columns:
        converted_df['WDSP'] = converted_df['WDSP'] * 1.852  # Convert to km/h
    if 'MXSPD' in converted_df.columns:
        converted_df['MXSPD'] = converted_df['MXSPD'] * 1.852  # Convert to km/h

    # convert visibility from miles to km
    if 'VISIB' in converted_df.columns: 
        converted_df['VISIB'] = converted_df['VISIB'] * 1.60934  # Convert to km    

    return converted_df
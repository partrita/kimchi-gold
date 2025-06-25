"""
Detects outliers in Kimchi premium data.

This module reads the logged Kimchi premium data and uses statistical methods
(IQR) to determine if the latest premium percentage is an outlier compared to
the data from the past year.
"""
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

CURRENT_DIR: Path = Path(__file__).resolve().parent
"""Current directory of this script."""

ROOT_DIR: Path = CURRENT_DIR.parent.parent
"""Project root directory."""

DATA_DIR: Path = ROOT_DIR / "data"
"""Directory where data files are stored."""
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATA_FILE: Path = DATA_DIR / "kimchi_gold_price_log.csv"
"""Path to the CSV file containing logged Kimchi premium data."""

def is_outlier(df: pd.DataFrame, column: str) -> bool:
    """
    Determines if the latest value in a DataFrame column is an outlier.

    The outlier detection is based on the Interquartile Range (IQR) method,
    applied to data from the last 365 days. The '날짜' column in the DataFrame
    is expected to contain date information. The function assumes the last row
    of the filtered yearly data represents the "today's" or latest data point.

    :param df: DataFrame containing the data to analyze. Must include a '날짜' column
               and the specified `column` for outlier detection.
    :type df: pd.DataFrame
    :param column: The name of the column in which to detect outliers.
    :type column: str
    :return: True if the latest value in the specified column is an outlier,
             False otherwise. Returns False if the DataFrame is empty, if there's
             no data within the last year, or if the specified column is not found.
    :rtype: bool
    """
    if df.empty:
        return False

    # Ensure '날짜' column is datetime objects
    df['날짜'] = pd.to_datetime(df['날짜'])

    today = datetime.now().date()
    one_year_ago = today - timedelta(days=365)

    # Filter data for the last year up to today
    recent_year_data = df[(df['날짜'].dt.date >= one_year_ago) & (df['날짜'].dt.date <= today)].copy()

    if recent_year_data.empty:
        return False

    try:
        Q1 = recent_year_data[column].quantile(0.25)
        Q3 = recent_year_data[column].quantile(0.75)
    except KeyError:
        # Column not found in the dataframe
        print(f"Error: Column '{column}' not found in DataFrame for outlier check.")
        return False

    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Assuming the last entry in recent_year_data is the latest value
    latest_value = recent_year_data.iloc[-1][column]

    return (latest_value < lower_bound) or (latest_value > upper_bound)

def check_kimchi_premium_outlier() -> bool:
    """
    Checks if the latest Kimchi premium percentage is an outlier.

    Reads data from `DATA_FILE`, then uses `is_outlier` to check the
    '김치프리미엄(%)' column. Prints error messages if the data file is not
    found or if other data processing errors occur.

    :return: True if the latest Kimchi premium is an outlier, False otherwise
             or if an error occurs.
    :rtype: bool
    """
    try:
        df = pd.read_csv(DATA_FILE)
        return is_outlier(df, '김치프리미엄(%)')
    except FileNotFoundError:
        print(f"Error: 파일 '{DATA_FILE}'을 찾을 수 없습니다.")
        return False
    except Exception as e:
        print(f"Error during data processing: {e}")
        return False

if __name__ == "__main__":
    # Example usage: Check for outlier and print the boolean result.
    # This is particularly useful for GitHub Actions to capture the output.
    result: bool = check_kimchi_premium_outlier()
    print(result)
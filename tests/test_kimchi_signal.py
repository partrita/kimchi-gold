import pytest
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import io # Moved import io to the top
from unittest.mock import patch, mock_open

from kimchi_gold.kimchi_signal import is_outlier, check_kimchi_premium_outlier, DATA_FILE as SIGNAL_DATA_FILE

# Helper to create mock CSV data
def create_mock_csv_data(data_list, include_header=True):
    header = "날짜,국내금(원/g),국제금(달러/온스),환율(원/달러),김치프리미엄(원/g),김치프리미엄(%)\n"
    lines = []
    if include_header:
        lines.append(header)
    for row in data_list:
        lines.append(",".join(map(str, row)) + "\n")
    return "".join(lines)

@pytest.fixture
def mock_data_file(tmp_path):
    return tmp_path / "mock_kimchi_gold_price_log.csv"

def test_is_outlier_empty_df():
    df = pd.DataFrame()
    assert not is_outlier(df, '김치프리미엄(%)')

def test_is_outlier_no_recent_data():
    today = datetime.now().date()
    two_years_ago = (today - timedelta(days=365*2)).strftime("%Y-%m-%d")
    data = [[two_years_ago, 100000, 2000, 1300, 5000, 5.0]]
    df = pd.read_csv(io.StringIO(create_mock_csv_data(data)))
    assert not is_outlier(df, '김치프리미엄(%)')


def test_is_outlier_normal_value(mock_data_file):
    today_str = datetime.now().strftime("%Y-%m-%d")
    data = []
    for i in range(10): # Some historical data
        past_date = (datetime.now() - timedelta(days=30 * (i + 1))).strftime("%Y-%m-%d")
        data.append([past_date, 100000, 2000, 1300, 1000 + i*10, 1.0 + i*0.01])
    # Add today's data - normal
    data.append([today_str, 100000, 2000, 1300, 1050, 1.05]) # Normal value

    df = pd.read_csv(io.StringIO(create_mock_csv_data(data)))
    df['날짜'] = pd.to_datetime(df['날짜']) # Convert date column

    # Manually filter for the last year for this test's logic
    one_year_ago = datetime.now().date() - timedelta(days=365)
    df_filtered = df[df['날짜'].dt.date >= one_year_ago].copy()

    assert not is_outlier(df_filtered, '김치프리미엄(%)')


def test_is_outlier_high_value(mock_data_file):
    today_str = datetime.now().strftime("%Y-%m-%d")
    data = []
    for i in range(10):
        past_date = (datetime.now() - timedelta(days=30 * (i + 1))).strftime("%Y-%m-%d")
        data.append([past_date, 100000, 2000, 1300, 1000, 1.0])
    # Add today's data - high outlier
    data.append([today_str, 100000, 2000, 1300, 5000, 5.0]) # High outlier

    df = pd.read_csv(io.StringIO(create_mock_csv_data(data)))
    df['날짜'] = pd.to_datetime(df['날짜'])

    one_year_ago = datetime.now().date() - timedelta(days=365)
    df_filtered = df[df['날짜'].dt.date >= one_year_ago].copy()

    assert is_outlier(df_filtered, '김치프리미엄(%)')


def test_is_outlier_low_value(mock_data_file):
    today_str = datetime.now().strftime("%Y-%m-%d")
    data = []
    for i in range(10):
        past_date = (datetime.now() - timedelta(days=30 * (i + 1))).strftime("%Y-%m-%d")
        # Make premium values higher to make the low value an outlier
        data.append([past_date, 100000, 2000, 1300, 3000 + i*10, 3.0 + i*0.01])
    # Add today's data - low outlier
    data.append([today_str, 100000, 2000, 1300, 100, 0.1]) # Low outlier

    df = pd.read_csv(io.StringIO(create_mock_csv_data(data)))
    df['날짜'] = pd.to_datetime(df['날짜'])

    one_year_ago = datetime.now().date() - timedelta(days=365)
    df_filtered = df[df['날짜'].dt.date >= one_year_ago].copy()

    assert is_outlier(df_filtered, '김치프리미엄(%)')


@patch('kimchi_gold.kimchi_signal.pd.read_csv')
def test_check_kimchi_premium_outlier_normal(mock_read_csv, mock_data_file):
    today_str = datetime.now().strftime("%Y-%m-%d")
    data = []
    for i in range(10):
        past_date = (datetime.now() - timedelta(days=30 * (i + 1))).strftime("%Y-%m-%d")
        data.append([past_date, 100000, 2000, 1300, 1000 + i*10, 1.0 + i*0.01])
    data.append([today_str, 100000, 2000, 1300, 1050, 1.05])

    # Create DataFrame directly to avoid calling the mocked pd.read_csv
    columns = ["날짜", "국내금(원/g)", "국제금(달러/온스)", "환율(원/달러)", "김치프리미엄(원/g)", "김치프리미엄(%)"]
    mock_df = pd.DataFrame(data, columns=columns)
    mock_df['날짜'] = pd.to_datetime(mock_df['날짜']) # Ensure date conversion for the mock

    mock_read_csv.return_value = mock_df

    with patch('kimchi_gold.kimchi_signal.DATA_FILE', mock_data_file):
        assert not check_kimchi_premium_outlier()
    mock_read_csv.assert_called_once_with(mock_data_file)


@patch('kimchi_gold.kimchi_signal.pd.read_csv')
def test_check_kimchi_premium_outlier_is_outlier(mock_read_csv, mock_data_file):
    today_str = datetime.now().strftime("%Y-%m-%d")
    data = []
    for i in range(10):
        past_date = (datetime.now() - timedelta(days=30 * (i + 1))).strftime("%Y-%m-%d")
        data.append([past_date, 100000, 2000, 1300, 1000, 1.0])
    data.append([today_str, 100000, 2000, 1300, 5000, 5.0]) # High outlier

    # Create DataFrame directly to avoid calling the mocked pd.read_csv
    columns = ["날짜", "국내금(원/g)", "국제금(달러/온스)", "환율(원/달러)", "김치프리미엄(원/g)", "김치프리미엄(%)"]
    mock_df = pd.DataFrame(data, columns=columns)
    mock_df['날짜'] = pd.to_datetime(mock_df['날짜']) # Ensure date conversion for the mock

    mock_read_csv.return_value = mock_df

    with patch('kimchi_gold.kimchi_signal.DATA_FILE', mock_data_file):
        assert check_kimchi_premium_outlier()
    mock_read_csv.assert_called_once_with(mock_data_file)


@patch('kimchi_gold.kimchi_signal.pd.read_csv', side_effect=FileNotFoundError)
def test_check_kimchi_premium_outlier_file_not_found(mock_read_csv, capsys, mock_data_file):
    with patch('kimchi_gold.kimchi_signal.DATA_FILE', mock_data_file):
        assert not check_kimchi_premium_outlier()
    captured = capsys.readouterr()
    assert f"Error: 파일 '{str(mock_data_file)}'을 찾을 수 없습니다." in captured.out
    mock_read_csv.assert_called_once_with(mock_data_file)


@patch('kimchi_gold.kimchi_signal.pd.read_csv')
def test_check_kimchi_premium_outlier_other_exception(mock_read_csv, capsys, mock_data_file):
    mock_read_csv.side_effect = Exception("Some other error")
    with patch('kimchi_gold.kimchi_signal.DATA_FILE', mock_data_file):
        assert not check_kimchi_premium_outlier()
    captured = capsys.readouterr()
    assert "Error during data processing: Some other error" in captured.out
    mock_read_csv.assert_called_once_with(mock_data_file)

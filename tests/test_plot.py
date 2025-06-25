import pytest
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta, date # Ensure 'date' is imported
from unittest.mock import patch, MagicMock
import io

from kimchi_gold.plot import Config, FilePaths, load_and_preprocess_data, plot_kimchi_premium, plot_gold_prices, plot_exchange_rate, main as plot_main

# Helper to create mock CSV data
def create_mock_plot_csv_data(data_list, include_header=True):
    header = "날짜,국내금(원/g),국제금(달러/온스),환율(원/달러),김치프리미엄(원/g),김치프리미엄(%)\n"
    lines = []
    if include_header:
        lines.append(header)
    for row_item in data_list: # Changed 'row' to 'row_item'
        lines.append(",".join(map(str, row_item)) + "\n")
    return "".join(lines)

@pytest.fixture(autouse=True) # Apply to all tests in this module
def mock_plot_settings(monkeypatch):
    """Sets a consistent Config.MONTHS and updates FilePaths for all plot tests."""
    monkeypatch.setattr(Config, 'MONTHS', 3)
    Config.OUTPUT_FILENAME = f"kimchi_gold_price_recent_{Config.MONTHS}months.png"
    # Assuming FilePaths.DATA_DIR is static or correctly set up elsewhere
    # Let's ensure FilePaths.DATA_DIR is a Path object for consistency if used in tests
    FilePaths.DATA_DIR = Path(FilePaths.DATA_DIR)
    FilePaths.OUTPUT_FILE = FilePaths.DATA_DIR / Config.OUTPUT_FILENAME
    # Create the data directory if it doesn't exist, for savefig
    FilePaths.DATA_DIR.mkdir(parents=True, exist_ok=True)


@pytest.fixture
def sample_csv_data():
    today = datetime.now().date()
    data_list = [] # Renamed 'data' to 'data_list' to avoid conflict
    for i in range(Config.MONTHS * 30 + 60): # Create enough data
        date_str = (today - timedelta(days=i)).strftime("%Y-%m-%d") # Renamed 'date' to 'date_str'
        data_list.append([date_str, 100000 + i, 2000 + i*0.1, 1300 + i*0.01, 5000 - i*10, 5.0 - i*0.01])
    return data_list

@pytest.fixture
def temp_data_file(tmp_path, sample_csv_data):
    # This specific filename is used by plot.py's FilePaths by default
    data_file = tmp_path / Config.DATA_FILENAME
    csv_content = create_mock_plot_csv_data(sample_csv_data)
    data_file.write_text(csv_content, encoding="utf-8")
    # Patch FilePaths.DATA_FILE to point to this temp file for the duration of the test
    with patch.object(FilePaths, 'DATA_FILE', data_file):
        yield data_file


def test_load_and_preprocess_data_success(temp_data_file):
    months_to_load = Config.MONTHS
    df = load_and_preprocess_data(temp_data_file, months_to_load)

    assert not df.empty
    assert df.index.dtype == 'object' # Index is of datetime.date objects
    if not df.empty:
        assert isinstance(df.index[0], date) # Check type of first element

    # plot.py calculates N months ago as `today - timedelta(days=months * 30)`
    min_expected_date = datetime.now().date() - timedelta(days=months_to_load * 30)

    assert df.index.min() >= min_expected_date
    assert df.index.max() <= datetime.now().date() # Max date should be today or in the past
    # Check if roughly the correct number of data points are loaded
    assert abs(len(df) - (months_to_load * 30)) <= 5 # Allow some leeway for month calculation


def test_load_and_preprocess_data_file_not_found(tmp_path):
    non_existent_file = tmp_path / "not_exists.csv"
    with pytest.raises(FileNotFoundError, match=f"Error: {non_existent_file} not found."):
        load_and_preprocess_data(non_existent_file, Config.MONTHS)

def test_load_and_preprocess_data_no_recent_data(tmp_path):
    data_file = tmp_path / "old_data.csv"
    # Create data that is older than Config.MONTHS
    old_date_str = (datetime.now().date() - timedelta(days=Config.MONTHS * 30 + 90)).strftime("%Y-%m-%d")
    csv_content = create_mock_plot_csv_data([[old_date_str, 100, 20, 13, 5, 0.5]])
    data_file.write_text(csv_content, encoding="utf-8")

    with pytest.raises(ValueError, match=f"No data available for the last {Config.MONTHS} months."):
        load_and_preprocess_data(data_file, Config.MONTHS)


@patch('kimchi_gold.plot.plt')
def test_plot_kimchi_premium(mock_plt):
    mock_ax = MagicMock()
    # Create an index of datetime.date objects, as that's what load_and_preprocess_data produces
    idx = pd.Index([datetime.now().date() - timedelta(days=i) for i in range(5)], dtype='object')
    df = pd.DataFrame({'김치프리미엄(%)': [1.0, 1.1, 1.2, 1.3, 1.4]}, index=idx)

    plot_kimchi_premium(mock_ax, df, Config.MONTHS) # Use Config.MONTHS from mock_plot_settings

    mock_ax.plot.assert_called_once()
    pd.testing.assert_index_equal(mock_ax.plot.call_args[0][0], df.index)
    pd.testing.assert_series_equal(mock_ax.plot.call_args[0][1], df["김치프리미엄(%)"], check_dtype=False)
    mock_ax.set_ylabel.assert_called_with("Kimchi Premium (%)")
    mock_ax.set_title.assert_called_with(f"Recent {Config.MONTHS} Months: Kimchi Premium (%)")
    mock_ax.legend.assert_called_once()
    mock_ax.grid.assert_called_with(True)

@patch('kimchi_gold.plot.plt')
def test_plot_gold_prices(mock_plt):
    mock_ax = MagicMock()
    idx = pd.Index([datetime.now().date() - timedelta(days=i) for i in range(5)], dtype='object')
    df_data = {
        '국내금(원/g)': [100.0, 101.0, 102.0, 103.0, 104.0],
        '국제금(달러/온스)': [20.0, 21.0, 22.0, 23.0, 24.0],
        '환율(원/달러)': [1000.0, 1001.0, 1002.0, 1003.0, 1004.0]
    }
    df = pd.DataFrame(df_data, index=idx)

    plot_gold_prices(mock_ax, df, Config.MONTHS)

    assert mock_ax.plot.call_count == 2
    pd.testing.assert_index_equal(mock_ax.plot.call_args_list[0][0][0], df.index)
    pd.testing.assert_series_equal(mock_ax.plot.call_args_list[0][0][1], df["국내금(원/g)"], check_dtype=False)

    international_adjusted = df["국제금(달러/온스)"] * (1 / 31.1035) * df["환율(원/달러)"]
    pd.testing.assert_index_equal(mock_ax.plot.call_args_list[1][0][0], df.index)
    pd.testing.assert_series_equal(mock_ax.plot.call_args_list[1][0][1], international_adjusted, check_dtype=False)

    mock_ax.set_ylabel.assert_called_with("Price (KRW/g)")
    mock_ax.legend.assert_called_once()
    mock_ax.grid.assert_called_with(True)

@patch('kimchi_gold.plot.plt')
def test_plot_exchange_rate(mock_plt):
    mock_ax = MagicMock()
    idx = pd.Index([datetime.now().date() - timedelta(days=i) for i in range(5)], dtype='object')
    df = pd.DataFrame({'환율(원/달러)': [1000.0, 1001.0, 1002.0, 1003.0, 1004.0]}, index=idx)

    plot_exchange_rate(mock_ax, df, Config.MONTHS)

    mock_ax.plot.assert_called_once()
    pd.testing.assert_index_equal(mock_ax.plot.call_args[0][0], df.index)
    pd.testing.assert_series_equal(mock_ax.plot.call_args[0][1], df["환율(원/달러)"], check_dtype=False)
    mock_ax.set_ylabel.assert_called_with("Exchange Rate (KRW/USD)")
    mock_ax.legend.assert_called_once()
    mock_ax.grid.assert_called_with(True)


@patch('kimchi_gold.plot.load_and_preprocess_data')
@patch('kimchi_gold.plot.plt')
# Removed patch for FilePaths.DATA_DIR.mkdir
def test_plot_main_success(mock_plt, mock_load_data, temp_data_file, capsys):
    idx = pd.Index([datetime.now().date() - timedelta(days=i) for i in range(Config.MONTHS * 30)], dtype='object')
    mock_df_data = {
        '김치프리미엄(%)': [1.0] * len(idx), '국내금(원/g)': [100.0] * len(idx),
        '국제금(달러/온스)': [20.0] * len(idx), '환율(원/달러)': [1000.0] * len(idx)
    }
    mock_df = pd.DataFrame(mock_df_data, index=idx)
    mock_load_data.return_value = mock_df

    mock_fig, mock_axes = MagicMock(), [MagicMock(), MagicMock(), MagicMock()]
    mock_plt.subplots.return_value = (mock_fig, mock_axes)

    plot_main() # temp_data_file fixture patches FilePaths.DATA_FILE

    # DATA_DIR.mkdir is called at module level in plot.py and possibly by mock_plot_settings
    # We are interested in the call from load_and_preprocess_data or main if any.
    # mock_module_mkdir.assert_any_call(parents=True, exist_ok=True) # from plot.py module level
    # The autouse fixture mock_plot_settings also calls mkdir.

    mock_load_data.assert_called_once_with(FilePaths.DATA_FILE, Config.MONTHS)

    mock_plt.style.use.assert_called_once_with("seaborn-v0_8-whitegrid")
    mock_plt.subplots.assert_called_once_with(nrows=3, ncols=1, figsize=(12, 15))

    assert mock_axes[0].plot.called
    assert mock_axes[1].plot.called
    assert mock_axes[2].plot.called

    mock_plt.tight_layout.assert_called_once()
    mock_plt.savefig.assert_called_once_with(FilePaths.OUTPUT_FILE) # OUTPUT_FILE is updated by mock_plot_settings

    # plot_main() itself doesn't print success. This is handled by the if __name__ == "__main__": block.
    captured = capsys.readouterr()
    assert captured.out == ""


@patch('kimchi_gold.plot.load_and_preprocess_data', side_effect=FileNotFoundError("Mocked: File not found."))
# Removed patch for FilePaths.DATA_DIR.mkdir
def test_plot_main_load_data_file_not_found(mock_load_data_error, temp_data_file, capsys):
    plot_main() # plot_main itself prints the error and returns

    captured = capsys.readouterr()
    assert "Mocked: File not found." in captured.out
    # No further exception should be raised by plot_main

@patch('kimchi_gold.plot.load_and_preprocess_data', side_effect=ValueError("Mocked: No data."))
# Removed patch for FilePaths.DATA_DIR.mkdir
def test_plot_main_load_data_value_error(mock_load_data_error, temp_data_file, capsys):
    plot_main() # plot_main itself prints the error and returns

    captured = capsys.readouterr()
    assert "Mocked: No data." in captured.out
    # No further exception should be raised by plot_main

@patch('kimchi_gold.plot.load_and_preprocess_data')
@patch('kimchi_gold.plot.plt') # Fully mock plt to control savefig behavior
# Removed patch for FilePaths.DATA_DIR.mkdir
def test_plot_main_savefig_exception(mock_plt_full, mock_load_data, temp_data_file):
    idx = pd.Index([datetime.now().date() - timedelta(days=i) for i in range(Config.MONTHS * 30)], dtype='object')
    mock_df_data = {
        '김치프리미엄(%)': [1.0] * len(idx), '국내금(원/g)': [100.0] * len(idx),
        '국제금(달러/온스)': [20.0] * len(idx), '환율(원/달러)': [1000.0] * len(idx)
    }
    mock_df = pd.DataFrame(mock_df_data, index=idx)
    mock_load_data.return_value = mock_df

    # Configure subplots return value for this mock
    mock_fig, mock_axes = MagicMock(), [MagicMock(), MagicMock(), MagicMock()]
    mock_plt_full.subplots.return_value = (mock_fig, mock_axes)

    mock_plt_full.savefig.side_effect = Exception("Mocked: Failed to save plot")

    # plot_main does not catch exceptions from plt.savefig() itself. So, it should propagate.
    with pytest.raises(Exception, match="Mocked: Failed to save plot"):
        plot_main() # temp_data_file fixture patches FilePaths.DATA_FILE

    # Verify mkdir was called (e.g. by module or settings fixture)
    # mock_module_mkdir.assert_any_call(parents=True, exist_ok=True)

# Test the __main__ block execution part if possible (optional, can be complex)
# For now, testing plot_main() is the primary goal.
# The print statement for success/failure in plot.py's __main__ block is not tested here.
# That would require running plot.py as a script and capturing stdout,
# or refactoring plot.py to make that part more testable.
# The current tests for plot_main cover its direct behavior.

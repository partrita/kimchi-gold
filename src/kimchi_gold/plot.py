"""
Generates and saves plots related to Kimchi premium for gold.

This module reads logged gold price and Kimchi premium data, then generates
three plots:
1. Kimchi Premium (%) over time.
2. Domestic vs. International Gold Prices (KRW/g) over time.
3. USD/KRW Exchange Rate over time.

The generated plots are saved as a single PNG image file.
Configuration for the plot, such as the number of months of data to display
and filenames, is managed by the `Config` and `FilePaths` classes.
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
from datetime import datetime, timedelta # Keep datetime for type hints if needed
# Import 'date' specifically if you are using it for type hints for date objects
from datetime import date as DateType # Alias for clarity
from matplotlib.axes import Axes
from matplotlib.figure import Figure


class Config:
    """
    Manages application settings, specifically for data visualization.

    Defines the period of data to display and filenames for data and output.

    :ivar MONTHS: The number of recent months of data to include in the plots.
    :vartype MONTHS: int
    :ivar DATA_FILENAME: The filename of the CSV log containing gold price data.
    :vartype DATA_FILENAME: str
    :ivar OUTPUT_FILENAME: The base filename for the generated plot image.
                           The number of months from `MONTHS` is incorporated into the final name.
    :vartype OUTPUT_FILENAME: str
    """

    MONTHS: int = 12
    """Number of past months to display in the plots. Default is 12."""

    DATA_FILENAME: str = "kimchi_gold_price_log.csv"
    """Filename for the input CSV data log."""

    OUTPUT_FILENAME: str = (
        f"kimchi_gold_price_recent_{MONTHS}months.png"
    )
    """
    Filename for the output plot image.
    Dynamically includes the number of months defined in `MONTHS`.
    """


class FilePaths:
    """
    Manages file and directory paths used by the plotting script.

    Defines paths for the current script directory, project root, data directory,
    input data file, and output plot file.

    :cvar CURRENT_DIR: Path to the directory containing this script.
    :vartype CURRENT_DIR: Path
    :cvar ROOT_DIR: Path to the project's root directory.
    :vartype ROOT_DIR: Path
    :cvar DATA_DIR: Path to the directory where data files are stored/expected.
    :vartype DATA_DIR: Path
    :cvar DATA_FILE: Full path to the input CSV data file, derived from `DATA_DIR` and `Config.DATA_FILENAME`.
    :vartype DATA_FILE: Path
    :cvar OUTPUT_FILE: Full path to the output plot image file, derived from `DATA_DIR` and `Config.OUTPUT_FILENAME`.
    :vartype OUTPUT_FILE: Path
    """

    CURRENT_DIR: Path = Path(__file__).resolve().parent
    """Path to the directory where this script is located."""

    ROOT_DIR: Path = CURRENT_DIR.parent.parent
    """Path to the root directory of the project."""

    DATA_DIR: Path = ROOT_DIR / "data"
    """Path to the data storage directory."""

    DATA_FILE: Path = DATA_DIR / Config.DATA_FILENAME
    """Full path to the CSV data log file."""

    OUTPUT_FILE: Path = DATA_DIR / Config.OUTPUT_FILENAME
    """Full path where the generated plot image will be saved."""

# Ensure data directory exists when module is loaded
FilePaths.DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_and_preprocess_data(data_file: Path, months: int) -> pd.DataFrame:
    """
    Loads and preprocesses gold price data from a CSV file.

    Reads the CSV, converts the '날짜' (date) column to `datetime.date` objects,
    sets this column as the DataFrame index, and filters the data to include
    only the records from the specified number of recent months.

    :param data_file: Path to the input CSV file.
    :type data_file: Path
    :param months: The number of recent months of data to retain.
    :type months: int
    :return: A DataFrame with a `datetime.date` index, filtered for the specified period.
    :rtype: pd.DataFrame
    :raises FileNotFoundError: If `data_file` does not exist.
    :raises ValueError: If no data is available for the specified recent `months`.
    """
    try:
        df: pd.DataFrame = pd.read_csv(data_file)
    except FileNotFoundError:
        # Re-raise with a more specific message if desired, or let it propagate
        raise FileNotFoundError(f"Error: Data file '{data_file}' not found.")

    df["날짜"] = pd.to_datetime(df["날짜"]).dt.date # Convert to datetime.date objects
    df = df.set_index("날짜")

    today: DateType = datetime.now().date() # Use DateType alias for clarity
    # Calculate N months ago by subtracting N*30 days. This is an approximation.
    months_ago: DateType = today - timedelta(days=months * 30)

    df_period: pd.DataFrame = df[df.index >= months_ago]

    if df_period.empty:
        raise ValueError(f"No data available for the last {months} months.")

    return df_period


def plot_kimchi_premium(ax: Axes, df: pd.DataFrame, months: int) -> None:
    """
    Plots the Kimchi premium percentage over time on a given Matplotlib Axes.

    :param ax: The Matplotlib Axes object on which to draw the plot.
    :type ax: matplotlib.axes.Axes
    :param df: DataFrame containing the data to plot. Expected to have a
               `datetime.date` index and a '김치프리미엄(%)' column.
    :type df: pd.DataFrame
    :param months: The number of months the data represents, used for the plot title.
    :type months: int
    """
    ax.plot(
        df.index,
        df["김치프리미엄(%)"],
        label="Kimchi Premium (%)",
        color="red",
        linestyle="--",
        marker="d",
    )
    ax.set_ylabel("Kimchi Premium (%)")
    ax.set_title(f"Recent {months} Months: Kimchi Premium (%)")
    ax.legend(loc="upper left")
    ax.tick_params(axis="x", rotation=45)
    ax.xaxis.set_major_locator(mdates.AutoDateLocator()) # Auto-scales date ticks
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d")) # Formats date ticks
    ax.grid(True)


def plot_gold_prices(ax: Axes, df: pd.DataFrame, months: int) -> None:
    """
    Plots domestic and international gold prices (KRW/g) on a given Matplotlib Axes.

    International gold price is converted from USD/ounce to KRW/gram using
    the '환율(원/달러)' column from the DataFrame.

    :param ax: The Matplotlib Axes object on which to draw the plot.
    :type ax: matplotlib.axes.Axes
    :param df: DataFrame containing the data. Expected to have a `datetime.date` index
               and columns '국내금(원/g)', '국제금(달러/온스)', and '환율(원/달러)'.
    :type df: pd.DataFrame
    :param months: The number of months the data represents, used for the plot title.
    :type months: int
    """
    ax.plot(
        df.index,
        df["국내금(원/g)"],
        label="Domestic Gold (KRW/g)",
        marker="o",
    )
    # Calculate international gold price in KRW/g
    international_krw_g = df["국제금(달러/온스)"] * (1 / 31.1035) * df["환율(원/달러)"]
    ax.plot(
        df.index,
        international_krw_g,
        label="International Gold (KRW/g, FX adjusted)",
        marker="x",
    )
    ax.set_ylabel("Price (KRW/g)")
    ax.set_title(f"Recent {months} Months: Domestic vs International Gold Price")
    ax.legend()
    ax.tick_params(axis="x", rotation=45)
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax.grid(True)


def plot_exchange_rate(ax: Axes, df: pd.DataFrame, months: int) -> None:
    """
    Plots the USD/KRW exchange rate over time on a given Matplotlib Axes.

    :param ax: The Matplotlib Axes object on which to draw the plot.
    :type ax: matplotlib.axes.Axes
    :param df: DataFrame containing the data. Expected to have a `datetime.date` index
               and a '환율(원/달러)' column.
    :type df: pd.DataFrame
    :param months: The number of months the data represents, used for the plot title.
    :type months: int
    """
    ax.plot(
        df.index,
        df["환율(원/달러)"],
        label="Exchange Rate (KRW/USD)",
        color="purple",
        marker="^",
    )
    ax.set_ylabel("Exchange Rate (KRW/USD)")
    ax.set_title(f"Recent {months} Months: Exchange Rate Trend")
    ax.legend()
    ax.tick_params(axis="x", rotation=45)
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax.grid(True)


def main():
    """
    Main function to generate and save the consolidated gold price plots.

    It loads data, creates a figure with three subplots (for Kimchi premium,
    gold prices, and exchange rate), plots the data on these subplots,
    and saves the figure to a file specified by `FilePaths.OUTPUT_FILE`.
    Handles `FileNotFoundError` and `ValueError` during data loading by
    printing an error message and exiting. Other exceptions during plotting
    will propagate.
    """
    # Data directory is created when the module is loaded.
    # FilePaths.DATA_DIR.mkdir(parents=True, exist_ok=True) # This is now at module level

    try:
        df_period: pd.DataFrame = load_and_preprocess_data(
            FilePaths.DATA_FILE, Config.MONTHS
        )
    except FileNotFoundError as e:
        print(e)
        return # Exit if data file not found
    except ValueError as e:
        print(e)
        return # Exit if no recent data

    plt.style.use("seaborn-v0_8-whitegrid")
    fig: Figure
    axes_list: list[Axes] # Renamed 'axes' to 'axes_list' to avoid conflict with matplotlib.axes
    fig, axes_list = plt.subplots(nrows=3, ncols=1, figsize=(12, 15))
    plt.subplots_adjust(hspace=0.5) # Adjust vertical spacing between subplots

    plot_kimchi_premium(axes_list[0], df_period, Config.MONTHS)
    plot_gold_prices(axes_list[1], df_period, Config.MONTHS)
    plot_exchange_rate(axes_list[2], df_period, Config.MONTHS)

    plt.tight_layout() # Adjust layout to prevent overlapping elements
    plt.savefig(FilePaths.OUTPUT_FILE)


if __name__ == "__main__":
    # This block executes when the script is run directly.
    # It calls the main plotting function and prints success or failure messages.
    try:
        main()
        # Success message uses Config.MONTHS and FilePaths.OUTPUT_FILE which are module-level
        print(
            f"{Config.MONTHS}개월 그래프가 성공적으로 '{FilePaths.OUTPUT_FILE}'에 저장되었습니다"
        )
    except Exception as e:
        # General exception catch for any errors not handled within main()
        print(
            f"시각화 실패: {e}"
        )

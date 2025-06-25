"""
Collects and logs Kimchi premium data for gold.

This script fetches current domestic and international gold prices,
calculates the Kimchi premium, and appends the data to a CSV log file.
It avoids duplicate entries for the same day.
"""
import csv
from datetime import datetime
from pathlib import Path
from typing import List, Tuple
from kimchi_gold.now_price import calc_kimchi_premium

CURRENT_DIR: Path = Path(__file__).resolve().parent
"""Current directory of this script."""

ROOT_DIR: Path = CURRENT_DIR.parent.parent
"""Project root directory."""

DATA_DIR: Path = ROOT_DIR / "data"
"""Directory to store data files."""
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATA_FILE: Path = DATA_DIR / "kimchi_gold_price_log.csv"
"""Path to the CSV file where gold price data is logged."""


def is_today_logged(filename: Path) -> bool:
    """
    Checks if data for the current date (YYYY-MM-DD) is already logged in the CSV file.

    :param filename: Path to the CSV file.
    :type filename: Path
    :return: True if today's data is already logged, False otherwise.
    :rtype: bool
    """
    if not filename.exists():
        return False
    today_str: str = datetime.now().strftime("%Y-%m-%d")
    with filename.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)  # Skip header
        for row in reader:
            if row and row[0].startswith(today_str): # Check if the date part matches
                return True
    return False


def write_to_csv(row: List[str], filename: Path = DATA_FILE) -> None:
    """
    Writes a data row to the specified CSV file.

    If the file does not exist, it creates the file and writes a header row first.
    Appends the new row to the end of the file.

    :param row: A list of strings representing the data to be written.
    :type row: List[str]
    :param filename: Path to the CSV file. Defaults to DATA_FILE.
    :type filename: Path, optional
    """
    file_exists: bool = filename.exists()
    with filename.open(mode="a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            # Write header
            writer.writerow(
                [
                    "날짜",
                    "국내금(원/g)",
                    "국제금(달러/온스)",
                    "환율(원/달러)",
                    "김치프리미엄(원/g)",
                    "김치프리미엄(%)",
                ]
            )
        writer.writerow(row)


def collect_data() -> None:
    """
    Collects current gold price data, calculates Kimchi premium, and logs it.

    If data for the current day is already logged, it prints a message and exits.
    Otherwise, it fetches prices using `calc_kimchi_premium`, formats the data,
    and writes it to the CSV log file. Prints success or failure messages.
    """
    if is_today_logged(DATA_FILE):
        print("오늘 데이터가 이미 존재합니다. 수집을 중단합니다.")
        return
    try:
        result: Tuple[float, float, float, float, float, float] = calc_kimchi_premium()
        domestic, international, _international_krw_per_g, usdkrw, diff, premium = result
        today_date_str: str = datetime.now().strftime("%Y-%m-%d") # Use a more descriptive name

        # Prepare data row for CSV
        # Values are domestic price, international price (USD/oz), USD/KRW exchange rate,
        # premium in KRW/g, and premium in percentage.
        data_row: List[str] = [
            today_date_str,
            f"{domestic:.2f}",
            f"{international:.2f}",
            f"{usdkrw:.2f}",
            f"{diff:.2f}",
            f"{premium:.2f}",
        ]
        write_to_csv(data_row)
        print(f"수집 완료: {data_row}")
    except Exception as e:
        print(f"수집 실패: {e}")


if __name__ == "__main__":
    collect_data()

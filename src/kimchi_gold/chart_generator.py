"""
김치 프리미엄과 금 가격 데이터의 차트를 생성하는 모듈입니다.
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
from datetime import datetime, timedelta
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from .configuration import (
    DATA_STORAGE_DIRECTORY,
    DEFAULT_CHART_DISPLAY_MONTHS,
    CHART_OUTPUT_FILE_NAME,
)





def load_and_preprocess_gold_price_data(
    source_csv_file_path: Path, analysis_period_months: int
) -> pd.DataFrame:
    """
    CSV 파일에서 데이터를 읽어오고, 날짜 형식으로 변환한 뒤,
    최근 'analysis_period_months' 개월의 데이터만 필터링하는 함수입니다.

    Args:
        source_csv_file_path: 읽어올 CSV 파일의 경로
        analysis_period_months: 보고 싶은 최근 개월 수

    Returns:
        pd.DataFrame: 날짜를 인덱스로 가지고 필터링된 데이터프레임

    Raises:
        FileNotFoundError: 지정된 데이터 파일이 없을 경우 발생
        ValueError: 최근 'analysis_period_months' 동안의 데이터가 없을 경우 발생
    """
    try:
        historical_data_df: pd.DataFrame = pd.read_csv(source_csv_file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: {source_csv_file_path} not found.")

    # 날짜 컬럼을 datetime.date 형식으로 변환
    historical_data_df.loc[:, "날짜"] = pd.to_datetime(historical_data_df["날짜"]).dt.date
    historical_data_df = historical_data_df.set_index("날짜")

    current_date = datetime.now().date()
    cutoff_date = current_date - timedelta(days=analysis_period_months * 30)

    filtered_period_data = historical_data_df[historical_data_df.index >= cutoff_date]

    if filtered_period_data.empty:
        raise ValueError(
            f"No data available for the last {analysis_period_months} months."
        )

    return filtered_period_data


def generate_kimchi_premium_chart(
    chart_axes: Axes, chart_data_df: pd.DataFrame, display_period_months: int
) -> None:
    """
    김치 프리미엄(%) 데이터를 선 그래프로 그리는 함수입니다.

    Args:
        chart_axes: 그래프를 그릴 Matplotlib Axes 객체
        chart_data_df: 그래프에 사용할 데이터프레임 (날짜를 인덱스로 가져야 함)
        display_period_months: 그래프 제목에 표시할 기간 (개월 수)
    """
    (line,) = chart_axes.plot(
        chart_data_df.index,
        chart_data_df["김치프리미엄(%)"],
        label="Kimchi Premium (%)",
        color="red",
        linestyle="--",
        marker="o",
    )
    chart_axes.set_ylabel("Kimchi Premium (%)")
    chart_axes.set_title(f"Recent {display_period_months} Months: Kimchi Premium (%)")
    chart_axes.legend(handles=[line], loc="upper left")
    chart_axes.tick_params(axis="x", rotation=45)
    chart_axes.xaxis.set_major_locator(mdates.AutoDateLocator())
    chart_axes.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    chart_axes.grid(True)


def generate_gold_prices_comparison_chart(
    chart_axes: Axes, chart_data_df: pd.DataFrame, display_period_months: int
) -> None:
    """
    국내 금 가격과 국제 금 가격 (환율 조정) 데이터를 선 그래프로 그리는 함수입니다.

    Args:
        chart_axes: 그래프를 그릴 Matplotlib Axes 객체
        chart_data_df: 그래프에 사용할 데이터프레임
        display_period_months: 그래프 제목에 표시할 기간 (개월 수)
    """
    (line1,) = chart_axes.plot(
        chart_data_df.index,
        chart_data_df["국내금(원/g)"],
        label="Domestic Gold (KRW/g)",
        marker="o",
    )

    # 국제 금 가격을 원/g 단위로 환산
    international_gold_price_krw_per_gram = (
        chart_data_df["국제금(달러/온스)"]
        * (1 / 31.1035)
        * chart_data_df["환율(원/달러)"]
    )

    (line2,) = chart_axes.plot(
        chart_data_df.index,
        international_gold_price_krw_per_gram,
        label="International Gold (KRW/g, FX adjusted)",
        marker="x",
    )
    chart_axes.set_ylabel("Price (KRW/g)")
    chart_axes.set_title(
        f"Recent {display_period_months} Months: Domestic vs International Gold Price"
    )
    chart_axes.legend(handles=[line1, line2])
    chart_axes.tick_params(axis="x", rotation=45)
    chart_axes.xaxis.set_major_locator(mdates.AutoDateLocator())
    chart_axes.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    chart_axes.grid(True)


def generate_exchange_rate_trend_chart(
    chart_axes: Axes, chart_data_df: pd.DataFrame, display_period_months: int
) -> None:
    """
    환율(달러/원) 데이터를 선 그래프로 그리는 함수입니다.

    Args:
        chart_axes: 그래프를 그릴 Matplotlib Axes 객체
        chart_data_df: 그래프에 사용할 데이터프레임
        display_period_months: 그래프 제목에 표시할 기간 (개월 수)
    """
    (line,) = chart_axes.plot(
        chart_data_df.index,
        chart_data_df["환율(원/달러)"],
        label="Exchange Rate (KRW/USD)",
        color="purple",
        marker="o",
    )
    chart_axes.set_ylabel("Exchange Rate (KRW/USD)")
    chart_axes.set_title(f"Recent {display_period_months} Months: Exchange Rate Trend")
    chart_axes.legend(handles=[line])
    chart_axes.tick_params(axis="x", rotation=45)
    chart_axes.xaxis.set_major_locator(mdates.AutoDateLocator())
    chart_axes.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    chart_axes.grid(True)


def create_comprehensive_gold_price_charts():
    """
    메인 실행 함수입니다.
    데이터를 로드하고 전처리한 후, 세 개의 그래프를 생성하고 저장합니다.
    """
    # Define configuration variables locally
    display_period_months = DEFAULT_CHART_DISPLAY_MONTHS
    source_data_file_name = "kimchi_gold_price_log.csv"
    output_chart_file_name = CHART_OUTPUT_FILE_NAME

    # Construct paths locally
    data_storage_directory = DATA_STORAGE_DIRECTORY
    source_data_csv_file = data_storage_directory / source_data_file_name
    output_chart_image_file = data_storage_directory / output_chart_file_name

    data_storage_directory.mkdir(parents=True, exist_ok=True)

    try:
        filtered_historical_data = load_and_preprocess_gold_price_data(
            source_data_csv_file,
            display_period_months,
        )
    except FileNotFoundError as file_error:
        print(file_error)
        return
    except ValueError as data_error:
        print(data_error)
        return

    plt.style.use("seaborn-v0_8-whitegrid")

    chart_figure: Figure
    chart_axes_list: list[Axes]
    chart_figure, chart_axes_list = plt.subplots(nrows=3, ncols=1, figsize=(12, 15))
    plt.subplots_adjust(hspace=0.5)

    generate_kimchi_premium_chart(
        chart_axes_list[0],
        filtered_historical_data,
        display_period_months,
    )
    generate_gold_prices_comparison_chart(
        chart_axes_list[1],
        filtered_historical_data,
        display_period_months,
    )
    generate_exchange_rate_trend_chart(
        chart_axes_list[2],
        filtered_historical_data,
        display_period_months,
    )

    plt.tight_layout()
    plt.savefig(output_chart_image_file)





if __name__ == "__main__":
    try:
        create_comprehensive_gold_price_charts()
        # Need to reconstruct the message as ChartFilePaths and GoldPriceChartConfiguration are gone
        display_period_months = DEFAULT_CHART_DISPLAY_MONTHS
        output_chart_file_name = CHART_OUTPUT_FILE_NAME
        data_storage_directory = DATA_STORAGE_DIRECTORY
        output_chart_image_file = data_storage_directory / output_chart_file_name

        print(
            f"{display_period_months}개월 그래프가 "
            f"성공적으로 {output_chart_image_file}에 저장되었습니다"
        )
    except Exception as chart_generation_error:
        print(f"시각화 실패: {chart_generation_error}")

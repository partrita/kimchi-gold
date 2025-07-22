import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
from datetime import datetime, timedelta
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from kimchi_gold.config import logger, DATA_FILE, PLOT_OUTPUT_FILE, MONTHS_TO_PLOT


def load_and_preprocess_data(data_file: Path, months: int) -> pd.DataFrame:
    """
    CSV 파일에서 데이터를 읽어오고, 날짜 형식으로 변환한 뒤,
    최근 'months' 개월의 데이터만 필터링하는 함수입니다.

    Args:
        data_file (Path): 읽어올 CSV 파일의 경로.
        months (int): 보고 싶은 최근 개월 수.

    Returns:
        pd.DataFrame: 날짜를 인덱스로 가지고 필터링된 데이터프레임.

    Raises:
        FileNotFoundError: 지정된 데이터 파일이 없을 경우 발생합니다.
        ValueError: 최근 'months' 동안의 데이터가 없을 경우 발생합니다.
    """
    try:
        df: pd.DataFrame = pd.read_csv(
            data_file
        )  # CSV 파일을 pandas DataFrame으로 읽어옵니다.
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Error: {data_file} not found."
        )  # 파일이 없으면 에러를 발생시킵니다.

    df["날짜"] = pd.to_datetime(
        df["날짜"]
    ).dt.date  # '날짜' 컬럼을 datetime.date 형식으로 변환합니다.
    df = df.set_index("날짜")  # '날짜' 컬럼을 DataFrame의 인덱스로 설정합니다.

    today: datetime.date = datetime.now().date()  # 현재 날짜를 구합니다.
    months_ago: datetime.date = today - timedelta(
        days=months * 30
    )  # 대략 'months' 개월 전의 날짜를 계산합니다. (정확한 월 계산은 아님)
    df_period: pd.DataFrame = df[
        df.index >= months_ago
    ]  # 인덱스(날짜)를 기준으로 최근 'months' 동안의 데이터를 필터링합니다.

    if df_period.empty:
        raise ValueError(
            f"No data available for the last {months} months."
        )  # 필터링된 데이터가 없으면 에러를 발생시킵니다.

    return df_period  # 필터링된 DataFrame을 반환합니다.


def plot_kimchi_premium(ax: Axes, df: pd.DataFrame, months: int) -> None:
    """
    김치 프리미엄(%) 데이터를 선 그래프로 그리는 함수입니다.

    Args:
        ax (Axes): 그래프를 그릴 Matplotlib Axes 객체.
        df (pd.DataFrame): 그래프에 사용할 데이터프레임 (날짜를 인덱스로 가져야 함).
        months (int): 그래프 제목에 표시할 기간 (개월 수).
    """
    ax.plot(
        df.index,  # x축은 날짜
        df["김치프리미엄(%)"],  # y축은 김치 프리미엄 (%) 컬럼
        label="Kimchi Premium (%)",  # 범례에 표시될 레이블
        color="red",  # 선 색깔
        linestyle="--",  # 선 스타일 (dashed)
        marker="d",  # 데이터 포인트 마커 (diamond)
    )
    ax.set_ylabel("Kimchi Premium (%)")  # y축 레이블 설정
    ax.set_title(f"Recent {months} Months: Kimchi Premium (%)")  # 그래프 제목 설정
    ax.legend(loc="upper left")  # 범례 위치 설정 (좌측 상단)
    ax.tick_params(
        axis="x", rotation=45
    )  # x축 눈금 레이블을 45도 회전하여 가독성을 높입니다.
    ax.xaxis.set_major_locator(
        mdates.AutoDateLocator()
    )  # x축 주요 눈금 위치를 자동으로 설정합니다.
    ax.xaxis.set_major_formatter(
        mdates.DateFormatter("%Y-%m-%d")
    )  # x축 날짜 형식 설정 (YYYY-MM-DD)
    ax.grid(True)  # 격자선 표시


def plot_gold_prices(ax: Axes, df: pd.DataFrame, months: int) -> None:
    """
    국내 금 가격과 국제 금 가격 (환율 조정) 데이터를 선 그래프로 그리는 함수입니다.

    Args:
        ax (Axes): 그래프를 그릴 Matplotlib Axes 객체.
        df (pd.DataFrame): 그래프에 사용할 데이터프레임.
        months (int): 그래프 제목에 표시할 기간 (개월 수).
    """
    ax.plot(
        df.index,
        df["국내금(원/g)"],
        label="Domestic Gold (KRW/g)",
        marker="o",
    )
    ax.plot(
        df.index,
        df["국제금(달러/온스)"]
        * (1 / 31.1035)
        * df["환율(원/달러)"],  # 국제 금 가격을 원/g 단위로 환산
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
    환율(원/달러) 데이터를 선 그래프로 그리는 함수입니다.

    Args:
        ax (Axes): 그래프를 그릴 Matplotlib Axes 객체.
        df (pd.DataFrame): 그래프에 사용할 데이터프레임.
        months (int): 그래프 제목에 표시할 기간 (개월 수).
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


def main(data_file: Path = DATA_FILE, output_file: Path = PLOT_OUTPUT_FILE, months: int = MONTHS_TO_PLOT):
    """
    메인 실행 함수입니다.
    데이터를 로드하고 전처리한 후, 세 개의 그래프를 생성하고 저장합니다.
    """
    try:
        df_period: pd.DataFrame = load_and_preprocess_data(
            data_file, months
        )
    except (FileNotFoundError, ValueError) as e:
        logger.error(e)
        return

    plt.style.use("seaborn-v0_8-whitegrid")
    fig: Figure
    axes: list[Axes]
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(12, 15))
    plt.subplots_adjust(hspace=0.5)

    plot_kimchi_premium(axes[0], df_period, months)
    plot_gold_prices(axes[1], df_period, months)
    plot_exchange_rate(axes[2], df_period, months)

    plt.tight_layout()
    plt.savefig(output_file)


if __name__ == "__main__":
    try:
        main()
        logger.info(
            f"{MONTHS_TO_PLOT}개월 그래프가 성공적으로 {PLOT_OUTPUT_FILE}에 저장되었습니다"
        )
    except Exception as e:
        logger.error(f"시각화 실패: {e}")

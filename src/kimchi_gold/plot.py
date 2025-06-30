import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from dateutil.relativedelta import relativedelta
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from kimchi_gold.config import DATA_FILE, PlotConfig, DATA_DIR

def load_and_preprocess_data(data_file: str, months: int) -> pd.DataFrame:
    """
    CSV 파일에서 데이터를 읽어오고, 날짜 형식으로 변환한 뒤,
    최근 'months' 개월의 데이터만 필터링하는 함수입니다.
    """
    try:
        df = pd.read_csv(data_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: {data_file} not found.")

    df["날짜"] = pd.to_datetime(df["날짜"]).dt.date
    df = df.set_index("날짜")

    today = datetime.now().date()
    months_ago = today - relativedelta(months=months)
    df_period = df[df.index >= months_ago]

    if df_period.empty:
        raise ValueError(f"No data available for the last {months} months.")

    return df_period

def setup_plot_style(ax: Axes, title: str, ylabel: str):
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.legend()
    ax.tick_params(axis='x', rotation=45)
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax.grid(True)

def plot_kimchi_premium(ax: Axes, df: pd.DataFrame, months: int) -> None:
    ax.plot(df.index, df["김치프리미엄(%)"], label="Kimchi Premium (%)", color="red", linestyle="--", marker="d")
    setup_plot_style(ax, f"Recent {months} Months: Kimchi Premium (%)", "Kimchi Premium (%)")

def plot_gold_prices(ax: Axes, df: pd.DataFrame, months: int) -> None:
    ax.plot(df.index, df["국내금(원/g)"], label="Domestic Gold (KRW/g)", marker="o")
    ax.plot(df.index, df["국제금(달러/온스)"] * (1 / 31.1035) * df["환율(원/달러)"], label="International Gold (KRW/g, FX adjusted)", marker="x")
    setup_plot_style(ax, f"Recent {months} Months: Domestic vs International Gold Price", "Price (KRW/g)")

def plot_exchange_rate(ax: Axes, df: pd.DataFrame, months: int) -> None:
    ax.plot(df.index, df["환율(원/달러)"], label="Exchange Rate (KRW/USD)", color="purple", marker="^")
    setup_plot_style(ax, f"Recent {months} Months: Exchange Rate Trend", "Exchange Rate (KRW/USD)")

def create_and_save_plot(months: int, output_filename: str):
    try:
        df_period = load_and_preprocess_data(DATA_FILE, months)
    except (FileNotFoundError, ValueError) as e:
        print(e)
        return

    plt.style.use(PlotConfig.STYLE)
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(12, 15))
    plt.subplots_adjust(hspace=0.5)

    plot_kimchi_premium(axes[0], df_period, months)
    plot_gold_prices(axes[1], df_period, months)
    plot_exchange_rate(axes[2], df_period, months)

    plt.tight_layout()
    output_path = DATA_DIR / output_filename
    plt.savefig(output_path)
    print(f"{months}개월 그래프가 성공적으로 {output_path}에 저장되었습니다")

def main():
    """
    메인 실행 함수입니다.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    create_and_save_plot(12, PlotConfig.OUTPUT_FILENAME_12M)
    create_and_save_plot(6, PlotConfig.OUTPUT_FILENAME_6M)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"시각화 실패: {e}")

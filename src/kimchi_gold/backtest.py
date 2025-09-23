import pandas as pd
import argparse
from datetime import datetime
import sys
from pathlib import Path


def run_backtest(data, initial_investment=1000000, start_date=None, buy_threshold=-3.0, sell_threshold=3.0):
    """Run the backtest strategy on the given data.

    Args:
        data: DataFrame containing price data
        initial_investment: Initial investment amount in KRW (default 1,000,000)
        start_date: Optional datetime to filter data from
        buy_threshold: Threshold for buy signals (default -3.0)
        sell_threshold: Threshold for sell signals (default 3.0)

    Returns:
        The DataFrame with backtest results
    """
    # 백테스팅 매개변수
    commission_rate = 0.0016  # 0.16%
    slippage_rate = 0.0005  # 예시 슬리피지 0.05%
    rebuy_threshold = 0.16  # 재매수 임계값 0.16%
    buy_price = None
    gold_quantity = 0  # 보유 금 수량 (그램)

    # Filter by start date if provided
    if start_date:
        data = data[data["date"] >= start_date].copy()
        if len(data) == 0:
            print(f"No data available after {start_date}")
            return None
        # Reset index after filtering
        data = data.reset_index(drop=True)
    else:
        # Make a copy to avoid SettingWithCopyWarning
        data = data.copy()

    # 거래 기록 및 포지션
    data["position"] = 0
    data["returns"] = 0.0
    data["pnl"] = 0.0  # 손익 기록
    data["portfolio_value"] = float(initial_investment)  # 포트폴리오 가치 (float 타입으로 명시)
    
    current_cash = initial_investment  # 현재 현금
    total_trades = 0  # 총 거래 횟수

    # 백테스팅 루프
    for i in range(1, len(data)):
        # 매수 조건 1: 일반 매수 (괴리율이 buy_threshold 이하)
        if (
            data.loc[i - 1, "disparity"] <= buy_threshold
            and data.loc[i - 1, "position"] == 0
            and current_cash > 0
        ):
            data.loc[i, "position"] = 1
            buy_price = data.loc[i, "krx_gold"] * (1 + slippage_rate + commission_rate)
            gold_quantity = current_cash / buy_price  # 구매 가능한 금 수량
            current_cash = 0  # 전액 투자
            total_trades += 1
            print(f"매수: {data.loc[i, 'date']}, 가격: {buy_price:.2f}원/g, 수량: {gold_quantity:.2f}g, 괴리율: {data.loc[i, 'disparity']:.2f}%")

        # 매수 조건 2: 재매수 (매도 후 괴리율이 0.16% 이내)
        elif (
            abs(data.loc[i - 1, "disparity"]) <= rebuy_threshold
            and data.loc[i - 1, "position"] == 0
            and current_cash > 0
        ):
            data.loc[i, "position"] = 1
            buy_price = data.loc[i, "krx_gold"] * (1 + slippage_rate + commission_rate)
            gold_quantity = current_cash / buy_price  # 구매 가능한 금 수량
            current_cash = 0  # 전액 투자
            total_trades += 1
            print(f"재매수: {data.loc[i, 'date']}, 가격: {buy_price:.2f}원/g, 수량: {gold_quantity:.2f}g, 괴리율: {data.loc[i, 'disparity']:.2f}%")

        # 매도 조건
        elif (
            data.loc[i - 1, "disparity"] >= sell_threshold
            and data.loc[i - 1, "position"] == 1
            and gold_quantity > 0
        ):
            sell_price = data.loc[i, "krx_gold"] * (1 - slippage_rate - commission_rate)
            current_cash = gold_quantity * sell_price  # 매도 후 현금
            profit_loss = current_cash - initial_investment
            data.loc[i, "pnl"] = profit_loss
            data.loc[i, "position"] = 0
            total_trades += 1
            print(
                f"매도: {data.loc[i, 'date']}, 가격: {sell_price:.2f}원/g, 수량: {gold_quantity:.2f}g, 현금: {current_cash:.0f}원, 손익: {profit_loss:.0f}원, 괴리율: {data.loc[i, 'disparity']:.2f}%"
            )
            gold_quantity = 0

        # 포지션 유지
        else:
            data.loc[i, "position"] = data.loc[i - 1, "position"]
        
        # 포트폴리오 가치 계산
        if data.loc[i, "position"] == 1:
            # 금을 보유 중인 경우
            data.loc[i, "portfolio_value"] = float(gold_quantity * data.loc[i, "krx_gold"])
        else:
            # 현금만 보유 중인 경우
            data.loc[i, "portfolio_value"] = float(current_cash)

    # 최종 포트폴리오 가치 계산
    final_value = data.iloc[-1]["portfolio_value"]
    total_return = final_value - initial_investment
    return_rate = (total_return / initial_investment) * 100
    
    print(f"\n=== 백테스팅 결과 ===")
    print(f"초기 투자금: {initial_investment:,.0f}원")
    print(f"최종 포트폴리오 가치: {final_value:,.0f}원")
    print(f"총 수익: {total_return:,.0f}원")
    print(f"수익률: {return_rate:.2f}%")
    print(f"총 거래 횟수: {total_trades}회")
    
    if total_trades > 0:
        avg_return_per_trade = total_return / (total_trades / 2)  # 매수-매도 한 쌍을 1거래로 계산
        print(f"거래당 평균 수익: {avg_return_per_trade:.0f}원")

    return data


def load_data(file_path):
    """Load and prepare the data from CSV file."""
    data = pd.read_csv(file_path)

    # 날짜,국내금(원/g),국제금(달러/온스),환율(원/달러),김치프리미엄(원/g),김치프리미엄(%)
    data.columns = [
        "date",
        "krx_gold",
        "Inter_gold",
        "exchange_rate",
        "disparity_won",
        "disparity",
    ]

    # Convert date string to datetime
    data["date"] = pd.to_datetime(data["date"])

    return data


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Run a backtest on Kimchi Premium Gold strategy."
    )
    parser.add_argument(
        "--investment",
        type=int,
        default=1000000,
        help="Initial investment amount in KRW (default: 1,000,000)",
    )
    parser.add_argument(
        "--start-date", type=str, help="Start date in YYYY-MM-DD format"
    )
    parser.add_argument(
        "--buy-threshold",
        type=float,
        default=-3.0,
        help="Threshold for buy signals (default: -3.0)",
    )
    parser.add_argument(
        "--sell-threshold",
        type=float,
        default=3.0,
        help="Threshold for sell signals (default: 3.0)",
    )

    return parser.parse_args()


def main():
    """Main function to run the backtest."""
    args = parse_args()

    # Parse start date if provided
    start_date = None
    if args.start_date:
        try:
            start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
        except ValueError:
            print("Error: Invalid date format. Please use YYYY-MM-DD format.")
            sys.exit(1)

    # Load data using pathlib
    data_file = Path.cwd() / "data" / "kimchi_gold_price_log.csv"

    if not data_file.exists():
        print(f"Error: Data file not found at {data_file}")
        print(f"Current working directory: {Path.cwd()}")
        sys.exit(1)

    try:
        data = load_data(data_file)
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)

    # Run backtest
    run_backtest(
        data,
        initial_investment=args.investment,
        start_date=start_date,
        buy_threshold=args.buy_threshold,
        sell_threshold=args.sell_threshold,
    )


if __name__ == "__main__":
    main()

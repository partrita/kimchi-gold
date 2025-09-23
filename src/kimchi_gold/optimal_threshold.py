import pandas as pd
import argparse
from datetime import datetime
import sys
from pathlib import Path
from backtest import run_backtest, load_data
import numpy as np


def run_optimization(data, initial_investment=1000000, start_date=None, 
                    threshold_min=0.5, threshold_max=5.0, threshold_step=0.5):
    """Run optimization to find the best threshold values.
    
    Args:
        data: DataFrame containing price data
        initial_investment: Initial investment amount in KRW
        start_date: Optional datetime to filter data from
        threshold_min: Minimum threshold to test
        threshold_max: Maximum threshold to test
        threshold_step: Step size for threshold testing
    
    Returns:
        DataFrame with optimization results
    """
    results = []
    
    # Generate threshold values to test
    thresholds = np.arange(threshold_min, threshold_max + threshold_step, threshold_step)
    
    print(f"=== 최적 임계값 탐색 시작 ===")
    print(f"테스트 범위: {threshold_min}% ~ {threshold_max}% (단계: {threshold_step}%)")
    print(f"총 테스트 횟수: {len(thresholds)}회")
    print("-" * 60)
    
    for i, threshold in enumerate(thresholds, 1):
        print(f"진행률: {i}/{len(thresholds)} - 임계값: ±{threshold:.1f}%", end=" ... ")
        
        # Run backtest with current threshold (buy = -threshold, sell = +threshold)
        try:
            # Suppress print output from backtest
            import io
            import contextlib
            
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                result_data = run_backtest(
                    data.copy(),
                    initial_investment=initial_investment,
                    start_date=start_date,
                    buy_threshold=-threshold,
                    sell_threshold=threshold
                )
            
            if result_data is not None and len(result_data) > 0:
                # Calculate performance metrics
                final_value = result_data.iloc[-1]["portfolio_value"]
                total_return = final_value - initial_investment
                return_rate = (total_return / initial_investment) * 100
                
                # Count trades
                position_changes = (result_data["position"].diff() != 0).sum()
                total_trades = position_changes
                
                results.append({
                    "threshold": threshold,
                    "buy_threshold": -threshold,
                    "sell_threshold": threshold,
                    "final_value": final_value,
                    "total_return": total_return,
                    "return_rate": return_rate,
                    "total_trades": total_trades
                })
                
                print(f"수익률: {return_rate:.2f}%, 거래횟수: {total_trades}")
            else:
                print("데이터 없음")
                
        except Exception as e:
            print(f"오류: {str(e)}")
    
    return pd.DataFrame(results)


def display_results(results_df):
    """Display optimization results in a nice format."""
    if len(results_df) == 0:
        print("결과가 없습니다.")
        return
    
    # Sort by return rate
    results_df = results_df.sort_values("return_rate", ascending=False)
    
    print("\n" + "=" * 80)
    print("최적화 결과 (수익률 기준 정렬)")
    print("=" * 80)
    
    # Display top 10 results
    top_results = results_df.head(10)
    
    print(f"{'순위':<4} {'임계값':<8} {'수익률':<10} {'총수익':<12} {'최종가치':<12} {'거래횟수':<8}")
    print("-" * 80)
    
    for i, (_, row) in enumerate(top_results.iterrows(), 1):
        print(f"{i:<4} ±{row['threshold']:.1f}%{'':<3} "
              f"{row['return_rate']:>8.2f}% "
              f"{row['total_return']:>10,.0f}원 "
              f"{row['final_value']:>11,.0f}원 "
              f"{row['total_trades']:>6.0f}회")
    
    # Best result details
    best = results_df.iloc[0]
    print("\n" + "=" * 50)
    print("최적 결과 상세")
    print("=" * 50)
    print(f"최적 임계값: ±{best['threshold']:.1f}%")
    print(f"매수 임계값: {best['buy_threshold']:.1f}%")
    print(f"매도 임계값: {best['sell_threshold']:.1f}%")
    print(f"최종 수익률: {best['return_rate']:.2f}%")
    print(f"총 수익: {best['total_return']:,.0f}원")
    print(f"최종 포트폴리오 가치: {best['final_value']:,.0f}원")
    print(f"총 거래 횟수: {best['total_trades']:.0f}회")
    
    if best['total_trades'] > 0:
        avg_return_per_trade = best['total_return'] / (best['total_trades'] / 2)
        print(f"거래당 평균 수익: {avg_return_per_trade:,.0f}원")


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Find optimal threshold values for Kimchi Premium Gold strategy."
    )
    parser.add_argument(
        "--investment",
        type=int,
        default=1000000,
        help="Initial investment amount in KRW (default: 1,000,000)"
    )
    parser.add_argument(
        "--start-date", 
        type=str, 
        help="Start date in YYYY-MM-DD format"
    )
    parser.add_argument(
        "--min-threshold",
        type=float,
        default=0.5,
        help="Minimum threshold to test (default: 0.5)"
    )
    parser.add_argument(
        "--max-threshold",
        type=float,
        default=5.0,
        help="Maximum threshold to test (default: 5.0)"
    )
    parser.add_argument(
        "--step",
        type=float,
        default=0.5,
        help="Step size for threshold testing (default: 0.5)"
    )
    
    return parser.parse_args()


def main():
    """Main function to run the optimization."""
    args = parse_args()
    
    # Parse start date if provided
    start_date = None
    if args.start_date:
        try:
            start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
        except ValueError:
            print("Error: Invalid date format. Please use YYYY-MM-DD format.")
            sys.exit(1)
    
    # Load data
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
    
    # Run optimization
    results = run_optimization(
        data,
        initial_investment=args.investment,
        start_date=start_date,
        threshold_min=args.min_threshold,
        threshold_max=args.max_threshold,
        threshold_step=args.step
    )
    
    # Display results
    display_results(results)


if __name__ == "__main__":
    main()
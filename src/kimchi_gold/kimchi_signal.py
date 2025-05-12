import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

CURRENT_DIR: Path = Path(__file__).resolve().parent
ROOT_DIR: Path = CURRENT_DIR.parent.parent  # 루트 폴더
DATA_DIR: Path = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DATA_FILE: Path = DATA_DIR / "kimchi_gold_price_log.csv"

def is_outlier(df: pd.DataFrame, column: str) -> bool:
    """
    특정 컬럼의 최근 1년 데이터를 기준으로 사분위수를 계산하고,
    오늘 날짜의 데이터가 이상치인지 여부를 반환합니다.

    Args:
        df (pd.DataFrame): 데이터프레임
        column (str): 확인할 컬럼명

    Returns:
        bool: 오늘 데이터가 이상치면 True, 아니면 False
    """
    if df.empty:
        return False

    df['날짜'] = pd.to_datetime(df['날짜'])
    today = datetime.now().date()
    one_year_ago = today - timedelta(days=365)
    recent_year_data = df[(df['날짜'].dt.date >= one_year_ago) & (df['날짜'].dt.date <= today)].copy()

    if recent_year_data.empty:
        return False

    Q1 = recent_year_data[column].quantile(0.25)
    Q3 = recent_year_data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    latest_value = recent_year_data.iloc[-1][column] #가장 최근 데이터가 오늘 데이터라고 가정

    return (latest_value < lower_bound) or (latest_value > upper_bound)

def check_kimchi_premium_outlier():
    """
    김치 프리미엄(%) 데이터의 최근 1년치 사분위수를 계산하고,
    오늘 김치 프리미엄(%) 값이 이상치인지 확인하여 True 또는 False를 반환합니다.
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
    result = check_kimchi_premium_outlier()
    print(result) # GitHub Actions에서 결과를 캡처하기 위해 print 합니다.
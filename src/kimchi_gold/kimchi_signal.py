import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from kimchi_gold.config import DATA_FILE

def is_outlier(df: pd.DataFrame, column: str) -> bool:
    """
    특정 컬럼의 최근 1년 데이터를 기준으로 사분위수를 계산하고,
    가장 최근 데이터가 이상치인지 여부를 반환합니다.
    """
    if df.empty:
        return False

    df['날짜'] = pd.to_datetime(df['날짜']).dt.date
    df = df.set_index('날짜')

    one_year_ago = datetime.now().date() - relativedelta(years=1)
    recent_year_data = df[df.index >= one_year_ago].copy()

    if len(recent_year_data) < 2: # 최소 2개의 데이터 포인트가 필요
        return False

    Q1 = recent_year_data[column].quantile(0.25)
    Q3 = recent_year_data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    latest_value = recent_year_data.iloc[-1][column]

    return (latest_value < lower_bound) or (latest_value > upper_bound)

def check_kimchi_premium_outlier() -> bool:
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
    print(result)
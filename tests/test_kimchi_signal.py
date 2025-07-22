import pandas as pd
import pytest
from datetime import datetime, timedelta
from kimchi_gold.kimchi_signal import is_outlier

@pytest.fixture
def sample_data():
    today = datetime.now()
    dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(365)]
    prices = [100 + i for i in range(365)]
    df = pd.DataFrame({'날짜': dates, '김치프리미엄(%)': prices})
    return df

def test_is_outlier_no_outlier(sample_data):
    assert is_outlier(sample_data, '김치프리미엄(%)') == False

def test_is_outlier_with_outlier(sample_data):
    today_str = datetime.now().strftime('%Y-%m-%d')
    sample_data.loc[sample_data['날짜'] == today_str, '김치프리미엄(%)'] = 1000
    assert is_outlier(sample_data, '김치프리미엄(%)') == True

def test_is_outlier_empty_dataframe():
    df = pd.DataFrame({'날짜': [], '김치프리미엄(%)': []})
    assert is_outlier(df, '김치프리미엄(%)') == False

def test_is_outlier_no_today_data(sample_data):
    sample_data = sample_data[sample_data['날짜'] != datetime.now().date()]
    assert is_outlier(sample_data, '김치프리미엄(%)') == False

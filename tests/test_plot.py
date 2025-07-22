import pandas as pd
import pytest
from pathlib import Path
from datetime import datetime, timedelta
from kimchi_gold.plot import main as plot_main
from kimchi_gold.config import DATA_FILE, PLOT_OUTPUT_FILE

@pytest.fixture(scope="module")
def setup_test_data(tmpdir_factory):
    data_dir = tmpdir_factory.mktemp("data")
    data_file = data_dir.join("test_data.csv")
    today = datetime.now()
    dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]
    df = pd.DataFrame({
        '날짜': dates,
        '국내금(원/g)': [70000 + i*100 for i in range(30)],
        '국제금(달러/온스)': [1800 + i for i in range(30)],
        '환율(원/달러)': [1200 + i for i in range(30)],
        '김치프리미엄(원/g)': [1000 + i*10 for i in range(30)],
        '김치프리미엄(%)': [1.5 + i*0.01 for i in range(30)]
    })
    df.to_csv(data_file, index=False)
    return data_file, data_dir

def test_plot_main(setup_test_data):
    test_data_file, test_data_dir = setup_test_data
    output_file = test_data_dir / "test_plot.png"

    try:
        plot_main(data_file=test_data_file, output_file=output_file)
        assert output_file.exists()
    except Exception as e:
        pytest.fail(f"plot_main failed with {e}")

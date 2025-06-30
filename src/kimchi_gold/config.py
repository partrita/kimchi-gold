"""
중앙 설정 파일
"""
from pathlib import Path

# --- 경로 설정 ---
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "data"
DATA_FILE = DATA_DIR / "kimchi_gold_price_log.csv"

# --- 데이터 수집 설정 ---
NAVER_FINANCE_URLS = {
    "domestic_gold": "https://m.stock.naver.com/marketindex/metals/M04020000",
    "international_gold": "https://m.stock.naver.com/marketindex/metals/GCcv1",
    "usd_krw": "https://m.stock.naver.com/marketindex/exchange/FX_USDKRW",
}
REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://m.stock.naver.com/",
}

# --- 시각화 설정 ---
class PlotConfig:
    """
    시각화 관련 설정을 관리하는 클래스
    """
    MONTHS = 12
    OUTPUT_FILENAME_12M = "kimchi_gold_price_recent_12months.png"
    OUTPUT_FILENAME_6M = "kimchi_gold_price_recent_6months.png"
    STYLE = "seaborn-v0_8-whitegrid"

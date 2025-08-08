"""
kimchi-gold 프로젝트의 설정과 상수들을 정의하는 모듈입니다.
"""

from pathlib import Path
from typing import Dict

# 파일 경로 설정
CURRENT_MODULE_DIRECTORY = Path(__file__).resolve().parent
PROJECT_ROOT_DIRECTORY = CURRENT_MODULE_DIRECTORY.parent.parent
DATA_STORAGE_DIRECTORY = PROJECT_ROOT_DIRECTORY / "data"
DATA_STORAGE_DIRECTORY.mkdir(parents=True, exist_ok=True)

# 데이터 파일 경로
GOLD_PRICE_DATA_CSV_FILE = DATA_STORAGE_DIRECTORY / "kimchi_gold_price_log.csv"

# HTTP 요청 헤더
REQUEST_HEADERS: Dict[str, str] = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://m.stock.naver.com/",
}

# 네이버 금융 URL들
NAVER_DOMESTIC_GOLD_URL = "https://m.stock.naver.com/marketindex/metals/M04020000"
NAVER_INTERNATIONAL_GOLD_URL = "https://m.stock.naver.com/marketindex/metals/GCcv1"
NAVER_USD_KRW_EXCHANGE_URL = "https://m.stock.naver.com/marketindex/exchange/FX_USDKRW"

# CSV 파일 헤더
CSV_COLUMN_HEADERS = [
    "날짜",
    "국내금(원/g)",
    "국제금(달러/온스)",
    "환율(원/달러)",
    "김치프리미엄(원/g)",
    "김치프리미엄(%)",
]

# 단위 변환 상수
TROY_OUNCE_TO_GRAM_CONVERSION_RATE = 31.1035

# 시각화 설정
DEFAULT_CHART_DISPLAY_MONTHS = 12
CHART_OUTPUT_FILE_NAME = f"kimchi_gold_price_recent_{DEFAULT_CHART_DISPLAY_MONTHS}months.png"

# 하위 호환성을 위한 별칭들
DATA_FILE = GOLD_PRICE_DATA_CSV_FILE
HEADERS = REQUEST_HEADERS
DOMESTIC_GOLD_URL = NAVER_DOMESTIC_GOLD_URL
INTERNATIONAL_GOLD_URL = NAVER_INTERNATIONAL_GOLD_URL
USD_KRW_URL = NAVER_USD_KRW_EXCHANGE_URL
CSV_HEADERS = CSV_COLUMN_HEADERS
TROY_OUNCE_TO_GRAM = TROY_OUNCE_TO_GRAM_CONVERSION_RATE
DEFAULT_CHART_MONTHS = DEFAULT_CHART_DISPLAY_MONTHS
CHART_OUTPUT_FILENAME = CHART_OUTPUT_FILE_NAME

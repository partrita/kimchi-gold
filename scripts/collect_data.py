#!/usr/bin/env python
"""
금 가격 데이터 수집 스크립트

이 스크립트는 GitHub Actions에서 순환 import 문제 없이 실행하기 위해 만들어졌습니다.
패키지를 import하지 않고 직접 모듈 파일을 로드합니다.
"""

import sys
import importlib.util
import logging
from pathlib import Path

# Setup paths
project_root = Path(__file__).resolve().parent.parent
src_path = project_root / "src" / "kimchi_gold"
data_dir = project_root / "data"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def load_module_from_file(module_name, file_path):
    """파일에서 직접 모듈을 로드 (패키지 초기화 없이)"""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

if __name__ == "__main__":
    try:
        # Mock configuration module
        import types
        config_mock = types.ModuleType('kimchi_gold.configuration')
        config_mock.DATA_STORAGE_DIRECTORY = data_dir
        config_mock.GOLD_PRICE_DATA_CSV_FILE = data_dir / "kimchi_gold_price_log.csv"
        
        # Constants from configuration.py
        config_mock.REQUEST_HEADERS = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://m.stock.naver.com/",
        }
        config_mock.NAVER_DOMESTIC_GOLD_URL = "https://m.stock.naver.com/marketindex/metals/M04020000"
        config_mock.NAVER_INTERNATIONAL_GOLD_URL = "https://m.stock.naver.com/marketindex/metals/GCcv1"
        config_mock.NAVER_USD_KRW_EXCHANGE_URL = "https://m.stock.naver.com/marketindex/exchange/FX_USDKRW"
        config_mock.CSV_COLUMN_HEADERS = [
            "날짜",
            "국내금(원/g)",
            "국제금(달러/온스)",
            "환율(원/달러)",
            "김치프리미엄(원/g)",
            "김치프리미엄(%)",
        ]
        config_mock.TROY_OUNCE_TO_GRAM_CONVERSION_RATE = 31.1035
        sys.modules['kimchi_gold.configuration'] = config_mock
        
        # Load dependencies in order
        load_module_from_file('kimchi_gold.data_models', src_path / "data_models.py")
        load_module_from_file('kimchi_gold.price_fetcher', src_path / "price_fetcher.py")
        data_collector = load_module_from_file('kimchi_gold.data_collector', src_path / "data_collector.py")
        
        logger.info("금 가격 데이터 수집 시작")
        success = data_collector.collect_and_save_current_gold_market_data()
        
        if success:
            logger.info("데이터 수집 완료")
            print("금 가격 데이터 수집이 성공적으로 완료되었습니다.")
        else:
            logger.info("오늘 날짜의 데이터가 이미 존재합니다.")
            print("오늘 날짜의 데이터가 이미 존재합니다.")
    except Exception as error:
        logger.error(f"데이터 수집 실패: {error}", exc_info=True)
        print(f"데이터 수집 실패: {error}")
        sys.exit(1)

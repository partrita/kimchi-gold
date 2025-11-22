#!/usr/bin/env python
"""
금 가격 데이터 수집 스크립트

이 스크립트는 GitHub Actions에서 순환 import 문제 없이 실행하기 위해 만들어졌습니다.
"""

import sys
from pathlib import Path

# Add src directory to path
project_root = Path(__file__).resolve().parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Now import the data collector
from kimchi_gold.data_collector import collect_and_save_current_gold_market_data
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        logger.info("금 가격 데이터 수집 시작")
        result = collect_and_save_current_gold_market_data()
        
        if result:
            logger.info(
                f"데이터 수집 완료: 김치 프리미엄 {result.kimchi_premium_percent:.2f}%"
            )
            print("금 가격 데이터 수집이 성공적으로 완료되었습니다.")
        else:
            logger.info("오늘 날짜의 데이터가 이미 존재합니다. 수집을 건너뜁니다.")
            print("오늘 날짜의 데이터가 이미 존재합니다.")
    except Exception as error:
        logger.error(f"데이터 수집 실패: {error}", exc_info=True)
        print(f"데이터 수집 실패: {error}")
        sys.exit(1)

#!/usr/bin/env python
"""
김치 프리미엄 이상치 분석 스크립트

이 스크립트는 GitHub Actions에서 순환 import 문제 없이 실행하기 위해 만들어졌습니다.
"""

import sys
from pathlib import Path

# Add src directory to path
project_root = Path(__file__).resolve().parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Now import the outlier analyzer
from kimchi_gold.outlier_analyzer import perform_kimchi_premium_outlier_analysis
from kimchi_gold.configuration import GOLD_PRICE_DATA_CSV_FILE
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        logger.info(f"김치 프리미엄 이상치 분석 시작: {GOLD_PRICE_DATA_CSV_FILE}")
        result = perform_kimchi_premium_outlier_analysis()
        
        # Result can be a dict or boolean depending on implementation
        if isinstance(result, dict):
            is_outlier_detected = result.get('is_outlier', False)
        else:
            is_outlier_detected = result
        
        # Print True/False for GitHub Actions to parse
        print(is_outlier_detected)
        
        if is_outlier_detected:
            print("김치 프리미엄이 이상치입니다!")
            if isinstance(result, dict):
                print(f"최신값: {result.get('latest_value')}, "
                      f"범위: [{result.get('lower_bound'):.2f}, {result.get('upper_bound'):.2f}]")
            logger.warning("이상치 감지!")
        else:
            print("김치 프리미엄이 정상 범위에 있습니다.")
            logger.info("정상 범위")
            
        logger.info(f"분석 완료: 이상치 여부 = {is_outlier_detected}")
    except Exception as error:
        logger.error(f"이상치 분석 실패: {error}", exc_info=True)
        print(f"분석 실패: {error}")
        sys.exit(1)

#!/usr/bin/env python
"""
김치 프리미엄 차트 생성 스크립트

이 스크립트는 GitHub Actions에서 순환 import 문제 없이 실행하기 위해 만들어졌습니다.
"""

import sys
from pathlib import Path

# Add src directory to path
project_root = Path(__file__).resolve().parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Now import the chart generator function
from kimchi_gold.chart_generator import create_comprehensive_gold_price_charts
from kimchi_gold.configuration import (
    DEFAULT_CHART_DISPLAY_MONTHS,
    CHART_OUTPUT_FILE_NAME,
    DATA_STORAGE_DIRECTORY,
)

if __name__ == "__main__":
    try:
        create_comprehensive_gold_price_charts()
        
        display_period_months = DEFAULT_CHART_DISPLAY_MONTHS
        output_chart_file_name = CHART_OUTPUT_FILE_NAME
        data_storage_directory = DATA_STORAGE_DIRECTORY
        output_chart_image_file = data_storage_directory / output_chart_file_name

        print(
            f"{display_period_months}개월 그래프가 "
            f"성공적으로 {output_chart_image_file}에 저장되었습니다"
        )
    except Exception as chart_generation_error:
        print(f"시각화 실패: {chart_generation_error}")
        sys.exit(1)

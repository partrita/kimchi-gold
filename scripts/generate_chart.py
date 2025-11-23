#!/usr/bin/env python
"""
김치 프리미엄 차트 생성 스크립트

이 스크립트는 GitHub Actions에서 순환 import 문제 없이 실행하기 위해 만들어졌습니다.
패키지를 import하지 않고 직접 모듈 파일을 로드합니다.
"""

import sys
import importlib.util
from pathlib import Path
from datetime import datetime, timedelta

# Setup paths
project_root = Path(__file__).resolve().parent.parent
src_path = project_root / "src" / "kimchi_gold"
data_dir = project_root / "data"

# Load configuration values directly without importing package
DEFAULT_CHART_DISPLAY_MONTHS = 12
CHART_OUTPUT_FILE_NAME = f"kimchi_gold_price_recent_{DEFAULT_CHART_DISPLAY_MONTHS}months.png"


def load_module_from_file(module_name, file_path):
    """파일에서 직접 모듈을 로드 (패키지 초기화 없이)"""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


if __name__ == "__main__":
    try:
        # Load chart_generator module directly without package import
        chart_gen_path = src_path / "chart_generator.py"
        
        # We need to mock the configuration imports that chart_generator expects
        import types
        config_mock = types.ModuleType('kimchi_gold.configuration')
        config_mock.DATA_STORAGE_DIRECTORY = data_dir
        config_mock.DEFAULT_CHART_DISPLAY_MONTHS = DEFAULT_CHART_DISPLAY_MONTHS
        config_mock.CHART_OUTPUT_FILE_NAME = CHART_OUTPUT_FILE_NAME
        sys.modules['kimchi_gold.configuration'] = config_mock
        
        # Now load the chart generator
        chart_gen = load_module_from_file('kimchi_gold.chart_generator', chart_gen_path)
        
        # Run the chart generation function
        chart_gen.create_comprehensive_gold_price_charts()
        
        output_chart_image_file = data_dir / CHART_OUTPUT_FILE_NAME
        print(
            f"{DEFAULT_CHART_DISPLAY_MONTHS}개월 그래프가 "
            f"성공적으로 {output_chart_image_file}에 저장되었습니다"
        )
    except Exception as chart_generation_error:
        import traceback
        print(f"시각화 실패: {chart_generation_error}")
        traceback.print_exc()
        sys.exit(1)

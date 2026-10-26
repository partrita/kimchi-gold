"""
kimchi-gold: 한국 금 가격과 김치 프리미엄을 모니터링하는 패키지
"""

# 버전 정보
__version__ = "0.2.0"
__author__ = "kimchi-gold contributors"
__email__ = "developers@kimchi-gold.com"

# 새로운 명확한 이름의 모듈들에서 주요 함수들과 클래스들을 import
from .data_collector import (
    check_if_date_already_logged,
    collect_and_save_current_gold_market_data,
    # 하위 호환성을 위한 레거시 함수들과 별칭들
    collect_current_gold_data,
    collect_data,
    is_today_logged,
    save_gold_price_data_to_csv,
    write_gold_data_to_csv,
    write_to_csv,
)
from .data_models import ChartGenerationConfiguration, GoldPriceData
from .outlier_analyzer import (
    # 하위 호환성을 위한 레거시 함수들과 별칭들
    analyze_kimchi_premium_outlier,
    check_kimchi_premium_outlier,
    determine_if_latest_value_is_outlier,
    is_outlier,
    perform_kimchi_premium_outlier_analysis,
)
from .price_fetcher import (
    calc_kimchi_premium,
    fetch_current_gold_market_data,
    fetch_domestic_gold_price,
    fetch_international_gold_price,
    fetch_usd_krw_exchange_rate,
    # 하위 호환성을 위한 레거시 함수들과 별칭들
    get_current_gold_price_data,
    get_domestic_gold_price,
    get_international_gold_price,
    get_usd_krw,
    get_usd_krw_rate,
)

# Note: chart_generator functions are not imported here to avoid circular imports
# when running modules directly (e.g., python -m kimchi_gold.chart_generator).
# Import them directly from kimchi_gold.chart_generator when needed.

# 주요 기능들
__all__ = [
    "ChartGenerationConfiguration",
    # 데이터 클래스
    "GoldPriceData",
    "analyze_kimchi_premium_outlier",
    "calc_kimchi_premium",
    "check_if_date_already_logged",
    "check_kimchi_premium_outlier",
    # 데이터 수집 및 저장
    "collect_and_save_current_gold_market_data",
    "collect_current_gold_data",
    "collect_data",
    "determine_if_latest_value_is_outlier",
    # 새로운 명확한 이름의 함수들
    # 가격 데이터 가져오기
    "fetch_current_gold_market_data",
    "fetch_domestic_gold_price",
    "fetch_international_gold_price",
    "fetch_usd_krw_exchange_rate",
    # Note: chart_generator functions removed from __all__ to prevent circular imports
    # Import directly from kimchi_gold.chart_generator when needed
    # 하위 호환성을 위한 별칭들
    "get_current_gold_price_data",
    "get_domestic_gold_price",
    "get_international_gold_price",
    "get_usd_krw",
    "get_usd_krw_rate",
    "is_outlier",
    "is_today_logged",
    # 이상치 분석
    "perform_kimchi_premium_outlier_analysis",
    "save_gold_price_data_to_csv",
    "write_gold_data_to_csv",
    "write_to_csv",
]

# 하위 호환성을 위한 별칭들
ChartConfig = ChartGenerationConfiguration

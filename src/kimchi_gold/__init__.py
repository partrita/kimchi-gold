"""
kimchi-gold: 한국 금 가격과 김치 프리미엄을 모니터링하는 패키지
"""

# 버전 정보
__version__ = "0.2.0"
__author__ = "kimchi-gold contributors"
__email__ = "developers@kimchi-gold.com"

# 새로운 명확한 이름의 모듈들에서 주요 함수들과 클래스들을 import
from .data_models import GoldPriceData, ChartGenerationConfiguration
from .price_fetcher import (
    fetch_current_gold_market_data,
    fetch_domestic_gold_price,
    fetch_international_gold_price,
    fetch_usd_krw_exchange_rate,
    # 하위 호환성을 위한 레거시 함수들과 별칭들
    get_current_gold_price_data,
    get_domestic_gold_price, 
    get_international_gold_price,
    get_usd_krw_rate,
    calc_kimchi_premium,
    get_usd_krw,
)
from .data_collector import (
    collect_and_save_current_gold_market_data,
    save_gold_price_data_to_csv,
    check_if_date_already_logged,
    # 하위 호환성을 위한 레거시 함수들과 별칭들
    collect_current_gold_data,
    write_gold_data_to_csv,
    is_today_logged,
    collect_data,
    write_to_csv,
)
from .outlier_analyzer import (
    perform_kimchi_premium_outlier_analysis,
    determine_if_latest_value_is_outlier,
    # 하위 호환성을 위한 레거시 함수들과 별칭들
    analyze_kimchi_premium_outlier,
    is_outlier,
    check_kimchi_premium_outlier,
)
from .chart_generator import (
    create_comprehensive_gold_price_charts,
    generate_kimchi_premium_chart,
    generate_gold_prices_comparison_chart,
    generate_exchange_rate_trend_chart,
)

# 주요 기능들
__all__ = [
    # 데이터 클래스
    "GoldPriceData",
    "ChartGenerationConfiguration",
    
    # 새로운 명확한 이름의 함수들
    # 가격 데이터 가져오기
    "fetch_current_gold_market_data",
    "fetch_domestic_gold_price",
    "fetch_international_gold_price",
    "fetch_usd_krw_exchange_rate",
    
    # 데이터 수집 및 저장
    "collect_and_save_current_gold_market_data",
    "save_gold_price_data_to_csv",
    "check_if_date_already_logged",
    
    # 이상치 분석
    "perform_kimchi_premium_outlier_analysis",
    "determine_if_latest_value_is_outlier",
    
    # 차트 생성
    "create_comprehensive_gold_price_charts",
    "generate_kimchi_premium_chart",
    "generate_gold_prices_comparison_chart",
    "generate_exchange_rate_trend_chart",
    
    # 하위 호환성을 위한 별칭들
    "get_current_gold_price_data",
    "get_domestic_gold_price",
    "get_international_gold_price", 
    "get_usd_krw_rate",
    "collect_current_gold_data",
    "write_gold_data_to_csv",
    "is_today_logged",
    "analyze_kimchi_premium_outlier",
    "is_outlier",
    "calc_kimchi_premium",
    "get_usd_krw", 
    "collect_data",
    "write_to_csv",
    "check_kimchi_premium_outlier",
]

# 하위 호환성을 위한 별칭들
ChartConfig = ChartGenerationConfiguration
